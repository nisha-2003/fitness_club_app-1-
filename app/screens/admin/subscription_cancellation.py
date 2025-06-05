from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from database import get_all_purchases, cancel_purchase  # cancel_purchase — функция удаления покупки

class SubscriptionCancellationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title = Label(text="Расторжение абонементов", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title)

        self.scrollview = ScrollView(size_hint=(1, 0.75))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scrollview.add_widget(self.list_layout)
        self.layout.add_widget(self.scrollview)

        btn_refresh = Button(text="Обновить список", size_hint=(1, 0.1))
        btn_refresh.bind(on_release=self.update_list)
        self.layout.add_widget(btn_refresh)

        btn_back = Button(text="Назад", size_hint=(1, 0.1))
        btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_list()

    def update_list(self, *args):
        self.list_layout.clear_widgets()
        purchases = get_all_purchases()
        if not purchases:
            self.list_layout.add_widget(Label(text="Покупки отсутствуют"))
            return

        for purchase in purchases:
            purchase_id, client_id, subscription_id, purchase_date, expiry_date = purchase
            # Получаем дополнительную информацию из БД (например, названия)
            # Для простоты выведем id клиента и подписки:
            item_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)

            label = Label(text=f"ID покупки: {purchase_id}, Клиент ID: {client_id}, Подписка ID: {subscription_id}")
            btn_cancel = Button(text="Расторгнуть", size_hint_x=0.3)
            btn_cancel.bind(on_release=lambda btn, pid=purchase_id: self.cancel_purchase_confirm(pid))
            item_layout.add_widget(label)
            item_layout.add_widget(btn_cancel)

            self.list_layout.add_widget(item_layout)

    def cancel_purchase_confirm(self, purchase_id):
        popup = Popup(title="Подтверждение",
                      content=Label(text="Вы действительно хотите расторгнуть этот абонемент?"),
                      size_hint=(0.6, 0.4),
                      auto_dismiss=False)
        btn_yes = Button(text="Да", size_hint=(1, 0.3))
        btn_no = Button(text="Нет", size_hint=(1, 0.3))

        content_layout = BoxLayout(orientation='vertical')
        content_layout.add_widget(Label(text="Вы действительно хотите расторгнуть этот абонемент?"))
        btn_layout = BoxLayout(size_hint=(1, 0.3))
        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content_layout.add_widget(btn_layout)

        popup.content = content_layout

        def confirm(instance):
            cancel_purchase(purchase_id)
            popup.dismiss()
            self.update_list()

        def decline(instance):
            popup.dismiss()

        btn_yes.bind(on_release=confirm)
        btn_no.bind(on_release=decline)

        popup.open()

    def go_back(self, instance):
        self.manager.current = 'admin'
