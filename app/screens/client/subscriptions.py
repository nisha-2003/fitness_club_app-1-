from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label

from database import get_all_subscriptions

class SubscriptionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(text="Доступные абонементы", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(title)

        self.scrollview = ScrollView(size_hint=(1, 0.9))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))

        self.scrollview.add_widget(self.list_layout)
        self.layout.add_widget(self.scrollview)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_list()

    def update_list(self):
        self.list_layout.clear_widgets()
        subscriptions = get_all_subscriptions()
        if not subscriptions:
            self.list_layout.add_widget(Label(text="Абонементы не найдены"))
        else:
            for sub in subscriptions:
                sub_id, name, price, duration = sub
                duration_text = f"{duration} дней" if duration else "Без ограничений"
                btn = Button(
                    text=f"{name} — {price} ₽ ({duration_text})",
                    size_hint_y=None,
                    height=48,
                    background_normal='',
                    background_color=(0.2, 0.6, 0.8, 1),
                    border=(12, 12, 12, 12),
                    # Для лучшего закругления можно использовать .kv с radius
                )
                btn.bind(on_release=lambda btn, sub_id=sub_id: self.show_detail(sub_id))
                self.list_layout.add_widget(btn)

    def show_detail(self, subscription_id):
        detail_screen = self.manager.get_screen('subscription_detail')
        detail_screen.set_subscription_by_id(subscription_id)
        self.manager.current = 'subscription_detail'
