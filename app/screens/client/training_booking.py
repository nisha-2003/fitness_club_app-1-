from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from database import add_training

class TrainingBookingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Добавляем поле photo к каждому тренеру
        self.trainers = [
            {"id": 1, "name": "Иван Иванов", "photo": "assets/trainers/ivan.png"},
            {"id": 2, "name": "Мария Петрова", "photo": "assets/trainers/maria.png"},
            {"id": 3, "name": "Алексей Сидоров", "photo": "assets/trainers/alexey.png"},
        ]

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        title = Label(text="Запись на тренировку", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(title)

        scrollview = ScrollView(size_hint=(1, 0.6))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scrollview.add_widget(self.list_layout)
        self.layout.add_widget(scrollview)

        for trainer in self.trainers:
            item = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)

            # Фото тренера
            img = Image(source=trainer['photo'], size_hint=(None, 1), width=60)

            # Кнопка с именем тренера
            btn = Button(text=trainer['name'], size_hint=(1, 1))
            btn.bind(on_release=lambda btn, tr=trainer: self.select_trainer(tr))

            item.add_widget(img)
            item.add_widget(btn)

            self.list_layout.add_widget(item)

        self.time_input = TextInput(hint_text="Введите время тренировки (например, 18:00)", size_hint=(1, 0.1))
        self.layout.add_widget(self.time_input)

        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        btn_book = Button(text="Записаться")
        btn_back = Button(text="Назад")
        btn_book.bind(on_release=self.book_training)
        btn_back.bind(on_release=self.go_back)
        btn_layout.add_widget(btn_book)
        btn_layout.add_widget(btn_back)
        self.layout.add_widget(btn_layout)

        self.selected_trainer = None
        self.client_id = None  # передавать при входе

        self.add_widget(self.layout)

    def select_trainer(self, trainer):
        self.selected_trainer = trainer
        popup = Popup(title="Тренер выбран",
                      content=Label(text=f"Вы выбрали тренера: {trainer['name']}"),
                      size_hint=(0.6, 0.4))
        popup.open()

    def book_training(self, instance):
        if not self.selected_trainer:
            popup = Popup(title="Ошибка", content=Label(text="Выберите тренера"), size_hint=(0.6, 0.4))
            popup.open()
            return
        time = self.time_input.text.strip()
        if not time:
            popup = Popup(title="Ошибка", content=Label(text="Введите время тренировки"), size_hint=(0.6, 0.4))
            popup.open()
            return
        if not self.client_id:
            popup = Popup(title="Ошибка", content=Label(text="Пользователь не авторизован"), size_hint=(0.6, 0.4))
            popup.open()
            return

        add_training(self.client_id, self.selected_trainer['name'], time)
        popup = Popup(title="Успех",
                      content=Label(text=f"Вы записались к тренеру {self.selected_trainer['name']} на {time}"),
                      size_hint=(0.6, 0.4))
        popup.open()
        self.time_input.text = ""
        self.selected_trainer = None

    def go_back(self, instance):
        self.manager.current = 'client'
