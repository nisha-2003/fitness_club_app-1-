from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from database import get_client_by_email, add_client

class ClientRegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(text="Введите Email для регистрации", font_size=20, size_hint=(1, 0.2)))
        self.email_input = TextInput(multiline=False, hint_text="Email", size_hint=(1, 0.2))
        layout.add_widget(self.email_input)

        layout.add_widget(Label(text="Введите имя", font_size=20, size_hint=(1, 0.2)))
        self.name_input = TextInput(multiline=False, hint_text="Имя", size_hint=(1, 0.2))
        layout.add_widget(self.name_input)

        btn_register = Button(text="Зарегистрироваться", size_hint=(1, 0.2))
        btn_register.bind(on_release=self.register)
        layout.add_widget(btn_register)

        btn_to_login = Button(text="Назад к входу", size_hint=(1, 0.2))
        btn_to_login.bind(on_release=self.go_to_login)
        layout.add_widget(btn_to_login)

        self.add_widget(layout)

    def register(self, instance):
        email = self.email_input.text.strip()
        name = self.name_input.text.strip()

        if not email or not name:
            self.show_popup("Ошибка", "Пожалуйста, заполните все поля")
            return

        if get_client_by_email(email):
            self.show_popup("Ошибка", "Пользователь с таким email уже существует")
            return

        client_id = add_client(name, email)
        client_screen = self.manager.get_screen('client')
        client_screen.client_id = client_id
        client_screen.client_name = name
        self.manager.current = 'client'

    def go_to_login(self, instance):
        self.manager.current = 'client_login'

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()
