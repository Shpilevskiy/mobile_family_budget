from rest_framework.test import APITestCase
from rest_framework import status

from account.tests.base import BaseCase
from account.models import (
    BudgetGroup,
    RefLink,
    User
)

from purchaseManager.models import (
    PurchaseList
)


class AuthTestCase(APITestCase):
    def test_create_new_user(self):
        data = {'username': 'user', 'password': 'user_password', 'first_name': 'John Doe'}
        response = self.client.post('/account/api-register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user')
        self.assertEqual(User.objects.get().first_name, 'John Doe')


class BudgetGroupTestCase(BaseCase):
    @classmethod
    def setUpClass(cls):
        cls.ENDPOINT_URL = '/account/budget-groups/'
        super().setUpClass()

    def test_only_authorized_user_can_reach_endpoint(self):
        response = self.client.post(self.ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(self.ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login()
        response = self.client.get(self.ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_group(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        response = self.client.post(self.ENDPOINT_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BudgetGroup.objects.get().name, group_name)

    def test_group_references_create(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')
        self.assertEqual(RefLink.objects.get(), BudgetGroup.objects.get().invite_link)
        self.assertEqual(PurchaseList.objects.get().budget_group, BudgetGroup.objects.get())

    def test_group_owner_added_to_group(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')
        self.assertEqual(BudgetGroup.objects.get().group_owner, User.objects.get(username=self.FIRST_USER_USERNAME))

    def test_group_creator_added_to_group_users(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')
        self.assertEqual(BudgetGroup.objects.get().users.get(), User.objects.get(username=self.FIRST_USER_USERNAME))

    def test_user_can_get_his_groups(self):
        first_user_groups = ['my_group', 'another_my_group', 'more_groups_for_me']

        self.login()
        [self.client.post(self.ENDPOINT_URL, {'name': group}, format='json') for group in first_user_groups]
        response = self.client.get(self.ENDPOINT_URL)
        for group in response.json():
            self.assertEqual(True, group['name'] in first_user_groups)
            self.assertEqual(True, 'id' in group)
            self.assertEqual(True, 'group_owner' in group)

    def test_user_can_get_only_his_groups(self):
        first_user_groups = ['my_group', 'another_my_group', 'more_groups_for_me']
        second_user_groups = ['not_my_group', 'and this group', 'and that group']

        self.create_user(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        self.login(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        [self.client.post(self.ENDPOINT_URL, {'name': group}, format='json') for group in second_user_groups]
        self.logout()

        self.login()
        [self.client.post(self.ENDPOINT_URL, {'name': group}, format='json') for group in first_user_groups]

        response = self.client.get(self.ENDPOINT_URL)
        resp_groups = [group.get('name') for group in response.json()]
        self.assertEqual(first_user_groups, resp_groups)



