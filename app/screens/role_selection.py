from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class RoleSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)

        label = Label(text="Выберите вашу роль", font_size=24, size_hint=(1, 0.3))
        btn_client = Button(text="Клиент", size_hint=(1, 0.20))
        btn_admin = Button(text="Администратор", size_hint=(1, 0.20))

        btn_client.bind(on_release=self.go_to_client)
        btn_admin.bind(on_release=self.go_to_admin)

        layout.add_widget(label)
        layout.add_widget(btn_client)
        layout.add_widget(btn_admin)

        self.add_widget(layout)

    def go_to_client(self, instance):
        self.manager.current = 'client_login'

    def go_to_admin(self, instance):
        self.manager.current = 'admin'
