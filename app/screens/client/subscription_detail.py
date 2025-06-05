from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from database import add_purchase

class SubscriptionDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subscription = None
        self.client_id = None  # будет устанавливаться при входе клиента

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.label_name = Label(text="", font_size=24, size_hint=(1, 0.2))
        self.label_price = Label(text="", font_size=20, size_hint=(1, 0.1))
        self.label_duration = Label(text="", font_size=20, size_hint=(1, 0.1))
        self.btn_buy = Button(text="Купить", size_hint=(1, 0.15), background_normal='', background_color=(0.2, 0.6, 0.8, 1), border=(12,12,12,12))
        self.btn_back = Button(text="Назад", size_hint=(1, 0.15), background_normal='', background_color=(0.6, 0.6, 0.6, 1), border=(12,12,12,12))

        self.btn_buy.bind(on_release=self.buy_subscription)
        self.btn_back.bind(on_release=self.go_back)

        self.layout.add_widget(self.label_name)
        self.layout.add_widget(self.label_price)
        self.layout.add_widget(self.label_duration)
        self.layout.add_widget(self.btn_buy)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def set_subscription_by_id(self, subscription_id):
        from database import get_all_subscriptions
        subs = get_all_subscriptions()
        for sub in subs:
            if sub[0] == subscription_id:
                self.subscription = sub
                break
        if self.subscription:
            _, name, price, duration = self.subscription
            self.label_name.text = name
            self.label_price.text = f"Цена: {price} ₽"
            self.label_duration.text = f"Длительность: {duration} дней" if duration else "Без ограничений"
        else:
            self.label_name.text = "Абонемент не найден"
            self.label_price.text = ""
            self.label_duration.text = ""

    def buy_subscription(self, instance):
        if not self.client_id:
            self.show_popup("Ошибка", "Пожалуйста, войдите в систему для покупки абонемента.")
            return
        if self.subscription:
            add_purchase(self.client_id, self.subscription[0])
            self.show_popup("Успех", "Спасибо за покупку!")
            # Очистить отображение или обновить
            self.label_name.text = ""
            self.label_price.text = ""
            self.label_duration.text = ""

    def go_back(self, instance):
        self.manager.current = 'subscriptions'

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()

    def on_pre_enter(self):
        # Получаем client_id из главного клиентского экрана
        client_screen = self.manager.get_screen('client')
        self.client_id = client_screen.client_id