from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

User = get_user_model()

DEFAULT_PASSWORD = "very_secret_password"


class BaseCase(APITestCase):
    def create_user(self, username, password):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def login(self, username='first_user', password='password_1'):
        self.client.login(username=username,
                          password=password)

    def logout(self):
        self.client.logout()

    @classmethod
    def setUpClass(cls):
        cls.FIRST_USER_USERNAME = 'first_user'
        cls.SECOND_USER_USERNAME = 'second_user'
        cls.FIRST_USER_PASSWORD = 'password_1'
        cls.SECOND_USER_PASSWORD = 'password_2'
        super().setUpClass()

    def setUp(self):
        self.user = self.create_user(username=self.FIRST_USER_USERNAME,
                                     password=self.FIRST_USER_PASSWORD)
        super().setUp()

    def tearDown(self):
        self.logout()
        self.user.delete()
        super().tearDown()
