from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.role_selection import RoleSelectionScreen
from screens.client.client_login import ClientLoginScreen
from screens.client.client_register import ClientRegisterScreen  # Импорт регистрации
from screens.client.client_main import ClientScreen
from screens.client.subscriptions import SubscriptionsScreen
from screens.client.subscription_detail import SubscriptionDetailScreen
from screens.client.purchased_subscriptions import PurchasedSubscriptionsScreen
from screens.client.training_booking import TrainingBookingScreen
from screens.admin.admin_main import AdminScreen
from screens.admin.subscription_management import SubscriptionManagementScreen
from screens.admin.training_schedule import TrainingScheduleScreen
from screens.admin.reports import ReportsScreen
from screens.admin.subscription_cancellation import SubscriptionCancellationScreen
from database import init_db


class FitnessClubApp(App):
    def build(self):
        init_db()

        sm = ScreenManager()
        sm.add_widget(RoleSelectionScreen(name='role_selection'))
        sm.add_widget(ClientLoginScreen(name='client_login'))
        sm.add_widget(ClientRegisterScreen(name='client_register'))  # Регистрация
        sm.add_widget(ClientScreen(name='client'))
        sm.add_widget(SubscriptionsScreen(name='subscriptions'))
        sm.add_widget(SubscriptionDetailScreen(name='subscription_detail'))
        sm.add_widget(PurchasedSubscriptionsScreen(name='purchased_subscriptions'))
        sm.add_widget(TrainingBookingScreen(name='training_booking'))

        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(SubscriptionManagementScreen(name='subscription_management'))
        sm.add_widget(TrainingScheduleScreen(name='training_schedule'))
        sm.add_widget(ReportsScreen(name='reports'))
        sm.add_widget(SubscriptionCancellationScreen(name='subscription_cancellation'))

        sm.current = 'role_selection'
        return sm


if __name__ == '__main__':
    FitnessClubApp().run()
