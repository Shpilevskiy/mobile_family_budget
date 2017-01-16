from rest_framework.test import APITestCase

from account.factorys.budget_group_factory import BudgetGroupFactory

from mobile_family_budget.tests.test_consts import DEFAULT_PASSWORD


class BaseCase(APITestCase):
    def login(self, username):
        self.client.login(username=username,
                          password=DEFAULT_PASSWORD)

    def logout(self):
        self.client.logout()

    def setUp(self):
        self.budget_group = BudgetGroupFactory()
        self.user = self.budget_group.group_owner
        self.username = self.user.username
        super().setUp()

    def tearDown(self):
        self.logout()
        self.budget_group.delete()
        super().tearDown()
