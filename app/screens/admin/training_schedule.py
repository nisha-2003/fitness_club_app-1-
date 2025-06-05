from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

from database import get_all_clients, get_trainings_by_client

class TrainingScheduleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title = Label(text="Расписание тренировок клиентов", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title)

        self.scrollview = ScrollView(size_hint=(1, 0.8))
        self.training_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.training_list.bind(minimum_height=self.training_list.setter('height'))
        self.scrollview.add_widget(self.training_list)
        self.layout.add_widget(self.scrollview)

        self.btn_back = Button(text="Назад", size_hint=(1, 0.1))
        self.btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(self.btn_back)

        self.add_widget(self.layout)

    def on_enter(self):
        self.update_training_list()

    def update_training_list(self):
        self.training_list.clear_widgets()
        clients = get_all_clients()
        if not clients:
            self.training_list.add_widget(Label(text="Нет клиентов в базе"))
            return
        for client in clients:
            client_id, name, email = client
            trainings = get_trainings_by_client(client_id)
            client_label = Label(text=f"Клиент: {name} ({email})", font_size=18, size_hint_y=None, height=30)
            self.training_list.add_widget(client_label)
            if trainings:
                for trainer_name, training_time in trainings:
                    training_label = Label(text=f"  Тренер: {trainer_name}, время: {training_time}", size_hint_y=None, height=25)
                    self.training_list.add_widget(training_label)
            else:
                self.training_list.add_widget(Label(text="  Нет записей на тренировки", size_hint_y=None, height=25))

    def go_back(self, instance):
        self.manager.current = 'admin'
