from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from database import get_all_clients, get_all_subscriptions, get_all_purchases, get_all_trainings

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.title = Label(text="Отчёты и статистика", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title)

        self.report_label = Label(text="", font_size=18, size_hint=(1, 0.7))
        self.layout.add_widget(self.report_label)

        btn_refresh = Button(text="Обновить", size_hint=(1, 0.1))
        btn_refresh.bind(on_release=self.update_report)
        self.layout.add_widget(btn_refresh)

        btn_back = Button(text="Назад", size_hint=(1, 0.1))
        btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_report()

    def update_report(self, *args):
        clients = get_all_clients()
        subscriptions = get_all_subscriptions()
        purchases = get_all_purchases()
        trainings = get_all_trainings()

        report_text = (
            f"Всего клиентов: {len(clients)}\n"
            f"Всего видов абонементов: {len(subscriptions)}\n"
            f"Всего купленных абонементов: {len(purchases)}\n"
            f"Всего записей на тренировки: {len(trainings)}\n"
        )
        self.report_label.text = report_text

    def go_back(self, instance):
        self.manager.current = 'admin'
