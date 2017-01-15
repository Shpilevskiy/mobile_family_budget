import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from mobile_family_budget.tests.base import BaseCase
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
            self.assertTrue(group['name'] in first_user_groups)
            self.assertTrue('id' in group)
            self.assertTrue('group_owner' in group)

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

    def test_user_can_get_detail_information_about_group(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get(name=group_name)
        response = self.client.get(self.ENDPOINT_URL + f'/{budget_group.id}/users/')
        json_response = response.json()[0]
        self.assertTrue('id' in json_response)
        self.assertTrue('name' in json_response)
        self.assertTrue('group_owner' in json_response)
        self.assertTrue('username' in json_response['group_owner'])
        self.assertTrue('email' in json_response['group_owner'])
        self.assertEqual(budget_group.name, json_response['name'])


class RefLinkTestCase(BaseCase):
    @classmethod
    def setUpClass(cls):
        cls.ENDPOINT_URL = '/account/budget-groups/'
        super().setUpClass()

    def test_ref_link_creates_with_group(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get(name=group_name)
        self.assertEqual(budget_group.invite_link, RefLink.objects.get())

    def test_user_cant_be_added_to_group_if_activation_count_is_not_positive(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get()
        invite_link = budget_group.invite_link
        self.create_user(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        self.login(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)

        invite_link.activation_count = 0
        invite_link.save()

        data = {'link': invite_link.link}
        response = self.client.put(self.ENDPOINT_URL + 'add-user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(True, 'link was outdated' in response.json()['error'])

    def test_user_cant_be_added_to_group_if_link_expired(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get()
        invite_link = budget_group.invite_link
        self.create_user(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        self.login(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)

        invite_link.expire_date = datetime.datetime.now() - datetime.timedelta(days=10)
        invite_link.save()

        data = {'link': invite_link.link}
        response = self.client.put(self.ENDPOINT_URL + 'add-user/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(True, 'link was outdated' in response.json()['error'])

    def test_new_users_can_be_added_to_group_by_ref_link(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')
        self.logout()

        budget_group = BudgetGroup.objects.get()
        invite_link = budget_group.invite_link.link
        self.create_user(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        self.login(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)

        data = {'link': invite_link}
        response = self.client.put(self.ENDPOINT_URL + 'add-user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(budget_group.is_member(User.objects.get(username=self.SECOND_USER_USERNAME)))

    def test_only_group_member_can_get_information_about_invite_link(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')
        self.logout()

        self.create_user(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        self.login(self.SECOND_USER_USERNAME, self.SECOND_USER_PASSWORD)
        budget_group = BudgetGroup.objects.get()

        response = self.client.get(self.ENDPOINT_URL + f'{budget_group.id}/invite_link/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(self.ENDPOINT_URL + f'{budget_group.id}/invite_link/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_generate_new_link(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get()
        old_link = budget_group.invite_link.link
        data = {"is_generate_new_link": "true"}

        response = self.client.put(self.ENDPOINT_URL + f'{budget_group.id}/invite_link/', data, fromat='json')

        new_link = BudgetGroup.objects.get().invite_link.link
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_link, new_link)

    def test_user_can_update_invite_link(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get()
        invite_link = budget_group.invite_link

        new_expire_date = "2025-01-16"
        new_activation_count = invite_link.activation_count + 5
        data = {"expire_date": new_expire_date, "activation_count": new_activation_count}
        response = self.client.put(self.ENDPOINT_URL + f'{budget_group.id}/invite_link/', data, fromat='json')

        invite_link = BudgetGroup.objects.get().invite_link
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(invite_link.expire_date, datetime.date(2025, 1, 16))
        self.assertEqual(invite_link.activation_count, new_activation_count)

    def test_user_cant_set_negative_activation_count(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get()

        new_activation_count = -5
        data = {"expire_date": '2025-01-16', "activation_count": new_activation_count}
        response = self.client.put(self.ENDPOINT_URL + f'{budget_group.id}/invite_link/', data, fromat='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Ensure this value is greater than or equal to 0' in response.json()['activation_count'][0])

    def test_user_can_get_detail_information_about_invite_link(self):
        group_name = 'my_group'
        data = {"name": group_name}

        self.login()
        self.client.post(self.ENDPOINT_URL, data, format='json')

        budget_group = BudgetGroup.objects.get()
        response = self.client.get(self.ENDPOINT_URL + f'{budget_group.id}/invite_link/', data, fromat='json')

        json_response = response.json()
        invite_link = RefLink.objects.get()
        creation_date = invite_link.creation_date
        expire_date = invite_link.expire_date

        self.assertTrue('creation_date' in json_response)
        self.assertEqual(json_response['creation_date'],
                         f"{creation_date.year}-{creation_date.strftime('%m')}-{creation_date.strftime('%d')}")

        self.assertTrue('link' in json_response)
        self.assertEqual(json_response['link'], invite_link.link)

        self.assertTrue('expire_date' in json_response)
        self.assertEqual(json_response['expire_date'],
                         f"{expire_date.year}-{expire_date.strftime('%m')}-{expire_date.strftime('%d')}")

        self.assertTrue('activation_count' in json_response)
        self.assertEqual(json_response['activation_count'], invite_link.activation_count)
