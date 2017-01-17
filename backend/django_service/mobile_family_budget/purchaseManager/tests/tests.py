from rest_framework import status
from rest_framework.reverse import reverse

from mobile_family_budget.tests.base import BaseCase
from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG
)

from account.factorys.user_factory import UserFactory

from purchaseManager.factorys.purchases_list_factory import PurchasesListFactory
from purchaseManager.factorys.purchase_factory import PurchaseFactory
from purchaseManager.models import (
    PurchaseList,
    Purchase
)


class PurchasesListsTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={GROUP_URL_KWARG: self.budget_group.id})
        expected_error_message = {'detail': 'Authentication credentials were not provided.'}

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_group_member_can_reach_endpoint(self):
        user = UserFactory()
        url = reverse('purchase-manager:purchases-lists', kwargs={GROUP_URL_KWARG: self.budget_group.id})
        expected_error_message = {'detail': 'You do not have permission to perform this action.'}

        self.login(user.username)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_get_all_purchases_lists(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={GROUP_URL_KWARG: self.budget_group.id})
        PurchasesListFactory.create_batch(4, budget_group=self.budget_group)

        expected_response = [{'id': purchase_list.id, 'name': purchase_list.name}
                             for purchase_list in PurchaseList.objects.filter(budget_group=self.budget_group)]

        self.login(self.username)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], expected_response)

    def test_user_can_create_new_purchase_list(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        new_list_name = "my_new_list"
        expected_response = {'id': 2, 'name': 'my_new_list'}

        self.login(self.username)
        response = self.client.post(url, {"name": new_list_name})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_response)
        self.assertTrue(PurchaseList.objects.get(budget_group=self.budget_group, name=new_list_name))

    def test_data_is_required(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={GROUP_URL_KWARG: self.budget_group.id})

        expected_response = {'name': ['This field is required.']}

        self.login(self.username)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)


class PurchasesListTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        purchase_list = PurchasesListFactory(budget_group=self.budget_group)
        url = reverse('purchase-manager:purchases-list', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: purchase_list.id
        })
        expected_error_message = {'detail': 'Authentication credentials were not provided.'}

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_group_member_can_reach_endpoint(self):
        user = UserFactory()
        purchase_list = PurchasesListFactory(budget_group=self.budget_group)

        url = reverse('purchase-manager:purchases-list', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: purchase_list.id
        })

        expected_error_message = {'detail': 'You do not have permission to perform this action.'}

        self.login(user.username)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_purchase_list_information(self):
        expected_result = {'id': 1, 'name': self.purchase_list.name}

        url = reverse('purchase-manager:purchases-list', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })
        self.login(self.username)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result)

    def test_purchase_list_could_be_renamed(self):
        new_name = "my new name"
        expected_result = {'id': 1, 'name': 'my new name'}

        url = reverse('purchase-manager:purchases-list', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })
        self.login(self.username)
        response = self.client.put(url, {'name': new_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result)
        self.assertEqual(new_name, PurchaseList.objects.get(budget_group=self.budget_group).name)

    def test_data_is_required(self):
        purchase_list = PurchasesListFactory(budget_group=self.budget_group)

        url = reverse('purchase-manager:purchases-list', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: purchase_list.id
        })

        expected_response = {'name': ['This field is required.']}

        self.login(self.username)
        response = self.client.put(url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)


class PurchasesTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        purchase_list = PurchasesListFactory(budget_group=self.budget_group)
        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: purchase_list.id
        })
        expected_error_message = {'detail': 'Authentication credentials were not provided.'}

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_group_member_can_reach_endpoint(self):
        user = UserFactory()

        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })

        expected_error_message = {'detail': 'You do not have permission to perform this action.'}

        self.login(user.username)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(response.json(), expected_error_message)

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_purchases_information(self):
        PurchaseFactory.create_batch(3, price=3.45, purchase_list=self.purchase_list)
        expected_data = [{'count': 1,
                          'current_count': 0,
                          'id': 1,
                          'name': 'purchase №0',
                          'price': 3.45,
                          'status': False},
                         {'count': 1,
                          'current_count': 0,
                          'id': 2,
                          'name': 'purchase №1',
                          'price': 3.45,
                          'status': False},
                         {'count': 1,
                          'current_count': 0,
                          'id': 3,
                          'name': 'purchase №2',
                          'price': 3.45,
                          'status': False}]

        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 3)
        self.assertEqual(response.json()['results'], expected_data)

    def test_create_new_purchase(self):
        name = 'first purchase'
        count = 2
        current_count = 1
        price = 26.5
        expected_data = []

        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })

        self.login(self.username)

        data = {
            'name': name,
            'count': count,
            'current_count': current_count,
            'price': price
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_purchase = Purchase.objects.get(purchase_list=self.purchase_list)
        self.assertEqual(created_purchase.name, name)
        self.assertEqual(created_purchase.count, count)
        self.assertEqual(created_purchase.current_count, current_count)
        self.assertEqual(created_purchase.price, price)
        self.assertEqual(created_purchase.status, False)

    def test_create_data_is_required(self):
        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })

        expected_data = {'name': ['This field is required.']}

        self.login(self.username)
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_data)

    def test_create_data_is_validated(self):
        name = 'first purchase'
        count = -1
        current_count = 1.25
        price = -6

        expected_data = {
            'count': ['Ensure this value is greater than or equal to 1.'],
            'current_count': ['A valid integer is required.'],
            'price': ['Ensure this value is greater than or equal to 0.']
        }

        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })

        self.login(self.username)

        data = {
            'name': name,
            'count': count,
            'current_count': current_count,
            'price': price
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), expected_data)
