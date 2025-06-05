from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from database import get_client_by_email

class ClientLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(text="Введите ваш Email для входа", font_size=20, size_hint=(1, 0.2)))
        self.email_input = TextInput(multiline=False, hint_text="Email", size_hint=(1, 0.2))
        layout.add_widget(self.email_input)

        btn_login = Button(text="Войти", size_hint=(1, 0.2))
        btn_login.bind(on_release=self.login)
        layout.add_widget(btn_login)

        btn_to_register = Button(text="Зарегистрироваться", size_hint=(1, 0.2))
        btn_to_register.bind(on_release=self.go_to_register)
        layout.add_widget(btn_to_register)

        self.add_widget(layout)

    def login(self, instance):
        email = self.email_input.text.strip()
        if not email:
            self.show_popup("Ошибка", "Введите email")
            return

        client = get_client_by_email(email)
        if client:
            client_id, name, email = client
            client_screen = self.manager.get_screen('client')
            client_screen.client_id = client_id
            client_screen.client_name = name
            self.manager.current = 'client'
        else:
            self.show_popup("Ошибка", "Пользователь не найден. Пожалуйста, зарегистрируйтесь.")

    def go_to_register(self, instance):
        self.manager.current = 'client_register'

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()
