from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from database import get_purchases_by_client

class PurchasedSubscriptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(text="Мои абонементы", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(title)

        self.scrollview = ScrollView(size_hint=(1, 0.8))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scrollview.add_widget(self.list_layout)
        self.layout.add_widget(self.scrollview)

        btn_back = Button(text="Назад", size_hint=(1, 0.1))
        btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

        self.client_id = None  # Нужно передавать ID клиента

    def on_enter(self):
        self.update_list()

    def update_list(self):
        self.list_layout.clear_widgets()
        if not self.client_id:
            self.list_layout.add_widget(Label(text="Пользователь не авторизован"))
            return

        purchases = get_purchases_by_client(self.client_id)
        if not purchases:
            self.list_layout.add_widget(Label(text="У вас пока нет купленных абонементов"))
            return

        for purchase in purchases:
            purchase_id, name, price, purchase_date, expiry_date = purchase
            expiry_text = expiry_date if expiry_date else "Без ограничений"
            text = f"{name} — {price} ₽, с {purchase_date[:10]} по {expiry_text[:10] if expiry_date else 'Без ограничений'}"
            self.list_layout.add_widget(Label(text=text, size_hint_y=None, height=30))

    def buy_subscription(self, instance):
        if not self.client_id:
            self.show_popup("Ошибка", "Пожалуйста, войдите в систему для покупки абонемента.")
            return
        if self.subscription:
            add_purchase(self.client_id, self.subscription[0])
            self.show_popup("Успех", "Спасибо за покупку!")
            self.manager.current = 'subscriptions'  # Можно возвращать обратно

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()
    def go_back(self, instance):
        self.manager.current = 'client'
