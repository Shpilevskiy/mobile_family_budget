import datetime

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from mobile_family_budget.tests.base import BaseCase

from account.models import (
    BudgetGroup,
    RefLink,
    User
)

from account.factorys.user_factory import UserFactory
from account.factorys.budget_group_factory import BudgetGroupFactory

from mobile_family_budget.utils.ulr_kwarg_consts import GROUP_URL_KWARG

from purchaseManager.models import PurchaseList


class AuthTestCase(APITestCase):
    def test_create_new_user(self):
        data = {'username': 'user', 'password': 'user_password', 'first_name': 'John Doe'}
        response = self.client.post('/api-register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'user')
        self.assertEqual(User.objects.get().first_name, 'John Doe')


class BudgetGroupsTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        url = reverse('account:budget-groups')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login(UserFactory().username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_group(self):
        group_name = 'my_group'
        url = reverse('account:budget-groups')

        user = UserFactory()
        self.login(user.username)

        response = self.client.post(url, {"name": group_name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BudgetGroup.objects.get(group_owner=user).name, group_name)

    def test_group_references_creates(self):
        group_name = 'my_group'
        url = reverse('account:budget-groups')

        user = UserFactory()
        self.login(user.username)

        self.client.post(url, {"name": group_name}, format='json')

        budget_group = BudgetGroup.objects.get(group_owner=user, name=group_name)

        self.assertEqual(RefLink.objects.get(budgetgroup=budget_group), budget_group.invite_link)
        self.assertEqual(PurchaseList.objects.get(budget_group=budget_group).budget_group, budget_group)

    def test_group_owner_added_to_group(self):
        group_name = 'my_group'
        url = reverse('account:budget-groups')

        user = UserFactory()
        self.login(user.username)
        self.client.post(url, {"name": group_name}, format='json')
        self.assertEqual(BudgetGroup.objects.get(group_owner=user).group_owner, user)

    def test_group_creator_added_to_group_users(self):
        group_name = 'my_group'
        url = reverse('account:budget-groups')

        user = UserFactory()
        self.login(user.username)
        self.client.post(url, {"name": group_name}, format='json')
        self.assertEqual(BudgetGroup.objects.get(group_owner=user, name=group_name).users.get(), user)

    def test_user_can_get_his_groups(self):
        user = UserFactory()
        groups = BudgetGroupFactory.create_batch(3, group_owner=user, )

        expected_result = [{'id': group.id,
                            'name': group.name,
                            'group_owner': {
                                'username': user.username,
                                'email': user.email,
                                'first_name': user.first_name
                            }} for group in groups]

        url = reverse('account:budget-groups')

        self.login(user.username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = response.json()
        self.assertEqual(json_response['count'], 3)
        self.assertEqual(json_response['results'], expected_result)

    def test_user_can_get_only_his_groups(self):
        url = reverse('account:budget-groups')

        user = UserFactory()
        user_groups = BudgetGroupFactory.create_batch(3, group_owner=user)

        another_user = UserFactory()
        BudgetGroupFactory.create_batch(3, group_owner=another_user)

        expected_result = [{'id': group.id,
                            'name': group.name,
                            'group_owner': {
                                'username': user.username,
                                'email': user.email,
                                'first_name': user.first_name
                            }} for group in user_groups]

        self.login(user.username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 3)
        self.assertEqual(response.json()['results'], expected_result)

    def test_user_can_get_detail_information_about_users_in_group(self):
        url = reverse('account:budget-group-users', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        self.budget_group.users.add(UserFactory(), UserFactory(), UserFactory())

        self.login(self.username)

        response = self.client.get(url)
        json_response = response.json()['results']

        for user in json_response:
            self.assertTrue('first_name' in user)
            self.assertTrue('username' in user)
            self.assertTrue('email' in user)


class BudgetGroupTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        url = reverse('account:budget-group', kwargs={'group_id': self.budget_group.id})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_group_member_can_reach_endpoint(self):
        url = reverse('account:budget-group', kwargs={'group_id': self.budget_group.id})

        self.login(UserFactory().username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login(self.username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_correct_budget_group(self):
        url = reverse('account:budget-group', kwargs={'group_id': self.budget_group.id})

        expected_result = {
            'id': self.budget_group.id,
            'name': self.budget_group.name,
            'group_owner': {
                'username': self.user.username,
                'first_name': self.user.first_name,
                'email': self.user.email
            }
        }

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), expected_result)

    def test_update_is_updating(self):
        url = reverse('account:budget-group', kwargs={'group_id': self.budget_group.id})

        new_name = 'new {}'.format(self.budget_group.name)

        self.login(self.username)
        response = self.client.put(url, data={'name': new_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_name, BudgetGroup.objects.get(id=self.budget_group.id).name)

    def test_update_data_required(self):
        url = reverse('account:budget-group', kwargs={'group_id': self.budget_group.id})

        self.login(self.username)
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RefLinkTestCase(BaseCase):
    def test_ref_link_creates_with_group(self):
        url = reverse('account:budget-groups')
        group_name = 'my_group'

        user = UserFactory()
        self.login(user.username)
        self.client.post(url, {"name": group_name}, format='json')

        budget_group = BudgetGroup.objects.get(name=group_name, group_owner=user)
        self.assertEqual(budget_group.invite_link, RefLink.objects.get(budgetgroup=budget_group))

    def test_user_cant_be_added_to_group_if_he_is_already_in(self):
        pass

    def test_user_cant_be_added_to_group_if_activation_count_is_not_positive(self):
        url = reverse('account:add-user')
        invite_link = self.budget_group.invite_link
        invite_link.activation_count = 0
        invite_link.save()

        self.login(UserFactory().username)
        response = self.client.put(url, {'link': invite_link.link}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(True, 'link was outdated' in response.json()['error'])

    def test_user_cant_be_added_to_group_if_link_expired(self):
        url = reverse('account:add-user')
        invite_link = self.budget_group.invite_link

        invite_link.expire_date = datetime.datetime.now() - datetime.timedelta(days=10)
        invite_link.save()

        self.login(UserFactory().username)
        response = self.client.put(url, {'link': invite_link.link}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(True, 'link was outdated' in response.json()['error'])

    def test_new_users_can_be_added_to_group_by_ref_link(self):
        url = reverse('account:add-user')
        invite_link = self.budget_group.invite_link

        user = UserFactory()
        self.login(user.username)
        response = self.client.put(url, {'link': invite_link.link}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.budget_group.is_member(user))

    def test_only_group_member_can_get_information_about_invite_link(self):
        url = reverse('account:budget-group-invite-link', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        self.login(UserFactory().username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_generate_new_link(self):
        url = reverse('account:budget-group-invite-link', kwargs={GROUP_URL_KWARG: self.budget_group.id})
        old_link = self.budget_group.invite_link.link

        self.login(self.username)
        response = self.client.put(url, {"is_generate_new_link": "true"}, format='json')

        new_link = RefLink.objects.get(budgetgroup=self.budget_group).link
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(old_link, new_link)

    def test_user_can_update_invite_link(self):
        url = reverse('account:budget-group-invite-link', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        new_expire_date = "2025-01-16"
        new_activation_count = self.budget_group.invite_link.activation_count + 5
        data = {"expire_date": new_expire_date, "activation_count": new_activation_count}

        self.login(self.username)
        response = self.client.put(url, data, format='json')

        invite_link = RefLink.objects.get(budgetgroup=self.budget_group)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(invite_link.expire_date, datetime.date(2025, 1, 16))
        self.assertEqual(invite_link.activation_count, new_activation_count)

    def test_user_cant_set_negative_activation_count(self):
        url = reverse('account:budget-group-invite-link', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        self.login(self.username)
        response = self.client.put(url, {"activation_count": -5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Ensure this value is greater than or equal to 0' in response.json()['activation_count'][0])

    def test_user_can_get_detail_information_about_invite_link(self):
        url = reverse('account:budget-group-invite-link', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        self.login(self.username)

        response = self.client.get(url, format='json')

        json_response = response.json()
        invite_link = RefLink.objects.get(budgetgroup=self.budget_group)
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
