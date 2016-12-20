from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class AuthorizationTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test User",
                            email="user@test.com",
                            password="pwdpwdpwd")

    def testUserCanLogIn(self):
        c = Client()
        response = c.post('/account/api-auth/login/', {'username': 'test User',
                                                       'password': 'pwdpwdpwd'})

        self.assertEqual(response.status_code, 200)
        print(self.client.session)
