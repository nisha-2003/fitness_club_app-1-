from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color

class ClientScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.client_id = None
        self.client_name = None

        # Создаем фон
        with self.canvas.before:
            self.bg_rect_color = Color(1, 1, 1, 1)  # белый фон (можно не ставить, если изображение)
            self.bg_rect = Rectangle(source='assets/1.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.greeting_label = Label(text="Добро пожаловать!", font_size=24, size_hint=(1, 0.2))
        self.layout.add_widget(self.greeting_label)

        btn_subscriptions = Button(
            text="Просмотреть абонементы",
            size_hint=(1, 0.15),
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            border=(12, 12, 12, 12),
        )
        btn_training = Button(
            text="Записаться на тренировку",
            size_hint=(1, 0.15),
            background_normal='',
            background_color=(0.2, 0.6, 0.8, 1),
            border=(12, 12, 12, 12),
        )
        btn_logout = Button(
            text="Выйти",
            size_hint=(1, 0.15),
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            border=(12, 12, 12, 12),
        )

        btn_subscriptions.bind(on_release=self.go_to_subscriptions)
        btn_training.bind(on_release=self.go_to_training)
        btn_logout.bind(on_release=self.logout)

        self.layout.add_widget(btn_subscriptions)
        self.layout.add_widget(btn_training)
        self.layout.add_widget(btn_logout)

        self.add_widget(self.layout)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_pre_enter(self):
        if self.client_name:
            self.greeting_label.text = f"Добро пожаловать, {self.client_name}!"
        else:
            self.greeting_label.text = "Добро пожаловать!"

    def go_to_subscriptions(self, instance):
        self.manager.current = 'subscriptions'

    def go_to_training(self, instance):
        self.manager.current = 'training_booking'

    def logout(self, instance):
        self.client_id = None
        self.client_name = None
        self.manager.current = 'role_selection'
