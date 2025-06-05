from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Фон с изображением
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(source='assets/2.png', pos=self.pos, size=self.size)

        self.bind(pos=self.update_bg, size=self.update_bg)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        title = Label(
            text="Администратор: Панель управления",
            font_size=24,
            size_hint=(1, 0.2),
            bold=True,
            color=(0, 0, 0, 1)  # RGBA для черного
        )
        layout.add_widget(title)

        btn_subs_mgmt = Button(text="Управление абонементами клиентов", size_hint=(1, 0.15))
        btn_training_sched = Button(text="Расписание тренировок", size_hint=(1, 0.15))
        btn_reports = Button(text="Отчёты и статистика", size_hint=(1, 0.15))
        btn_cancel_subs = Button(text="Расторжение абонементов", size_hint=(1, 0.15))
        btn_logout = Button(text="Выйти", size_hint=(1, 0.15))

        btn_subs_mgmt.bind(on_release=lambda x: self.go_to('subscription_management'))
        btn_training_sched.bind(on_release=lambda x: self.go_to('training_schedule'))
        btn_reports.bind(on_release=lambda x: self.go_to('reports'))
        btn_cancel_subs.bind(on_release=lambda x: self.go_to('subscription_cancellation'))
        btn_logout.bind(on_release=lambda x: self.go_back())

        layout.add_widget(btn_subs_mgmt)
        layout.add_widget(btn_training_sched)
        layout.add_widget(btn_reports)
        layout.add_widget(btn_cancel_subs)
        layout.add_widget(btn_logout)

        self.add_widget(layout)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_to(self, screen_name):
        self.manager.current = screen_name

    def go_back(self):
        self.manager.current = 'role_selection'
