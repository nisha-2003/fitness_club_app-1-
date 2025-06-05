from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from database import get_all_clients, get_purchases_by_client

class SubscriptionManagementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title = Label(text="Управление абонементами клиентов", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title)

        self.scrollview = ScrollView(size_hint=(1, 0.8))
        self.purchase_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.purchase_list.bind(minimum_height=self.purchase_list.setter('height'))
        self.scrollview.add_widget(self.purchase_list)
        self.layout.add_widget(self.scrollview)

        self.btn_back = Button(text="Назад", size_hint=(1, 0.1))
        self.btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_purchase_list()

    def update_purchase_list(self):
        self.purchase_list.clear_widgets()
        clients = get_all_clients()
        if not clients:
            self.purchase_list.add_widget(Label(text="Нет клиентов в базе"))
            return
        for client in clients:
            client_id, name, email = client
            purchases = get_purchases_by_client(client_id)
            client_label = Label(text=f"Клиент: {name} ({email})", font_size=18, size_hint_y=None, height=30)
            self.purchase_list.add_widget(client_label)
            if purchases:
                for pid, sub_name, price, purchase_date, expiry_date in purchases:
                    expiry_text = expiry_date if expiry_date else "Без ограничений"
                    purchase_date_str = purchase_date[:10] if purchase_date else "неизвестна"
                    expiry_text_str = expiry_text[:10] if expiry_date else "Без ограничений"
                    purchase_label = Label(text=f"  {sub_name} — {price} ₽, с {purchase_date_str} по {expiry_text_str}", size_hint_y=None, height=25)
                    self.purchase_list.add_widget(purchase_label)
            else:
                self.purchase_list.add_widget(Label(text="  Нет абонементов", size_hint_y=None, height=25))

    def go_back(self, instance):
        self.manager.current = 'admin'
