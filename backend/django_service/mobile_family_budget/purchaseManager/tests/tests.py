from rest_framework import status
from rest_framework.reverse import reverse

from mobile_family_budget.tests.base import BaseCase
from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG,
    PURCHASE_URL_KWARG
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

    def test_correct_response_for_not_exists_purchase_list(self):
        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: PurchaseList.objects.latest('id').id + 1
        })
        expected_response = {"detail": "Purchases list is not found."}

        self.login(self.username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), expected_response)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), expected_response)

    def test_get_purchases_information(self):
        purchases = PurchaseFactory.create_batch(size=9, purchase_list=self.purchase_list)
        expected_data = [{'count': purchase.count,
                          'current_count': purchase.current_count,
                          'id': purchase.id,
                          'name': purchase.name,
                          'price': purchase.price,
                          'status': purchase.status} for purchase in purchases]

        url = reverse('purchase-manager:purchases', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id
        })

        self.login(self.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], len(expected_data))
        self.assertEqual(response.json()['results'], expected_data)

    def test_create_new_purchase(self):
        name = 'first purchase'
        count = 2
        current_count = 1
        price = 26.5

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


class PurchaseTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        purchase = PurchaseFactory(purchase_list=self.purchase_list)
        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: purchase.id
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
        purchase = PurchaseFactory(purchase_list=self.purchase_list)

        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: purchase.id
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

    def test_get_returns_correct_purchase(self):
        purchases = PurchaseFactory.create_batch(5, purchase_list=self.purchase_list)
        purchase = purchases[2]
        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: purchase.id
        })

        self.login(self.username)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json(), {'id': purchase.id,
                                                      'count': purchase.count,
                                                      'name': purchase.name,
                                                      'current_count': purchase.current_count,
                                                      'price': purchase.price,
                                                      'status': purchase.status,
                                                      })

    def test_update_is_updating(self):
        old_purchase = PurchaseFactory(purchase_list=self.purchase_list)

        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: old_purchase.id
        })

        self.login(self.username)
        data = {
            'id': old_purchase.id,
            'name': 'new {}'.format(old_purchase.name),
            'count': old_purchase.count+1,
            'current_count': old_purchase.count+1,
            'price': old_purchase.price+105.42,
            'status': True
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

        new_purchase = Purchase.objects.get(id=old_purchase.id)
        self.assertEqual(new_purchase.name, data['name'])
        self.assertEqual(new_purchase.count, data['count'])
        self.assertEqual(new_purchase.current_count, data['current_count'])
        self.assertEqual(new_purchase.price, data['price'])
        self.assertEqual(new_purchase.status, data['status'])

    def test_data_for_update_is_required(self):
        purchase = PurchaseFactory(purchase_list=self.purchase_list)

        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: purchase.id
        })

        self.login(self.username)
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detail': 'at least one field is required'})

    def test_data_for_update_is_validated(self):
        purchase = PurchaseFactory(purchase_list=self.purchase_list)

        data = {
            'name': 'first purchase',
            'count': -1,
            'current_count': 1.25,
            'price': -6,
            'status': 123
        }

        expected_response = {
            'count': ['Ensure this value is greater than or equal to 1.'],
            'current_count': ['A valid integer is required.'],
            'price': ['Ensure this value is greater than or equal to 0.'],
            "status": ['\"123\" is not a valid boolean.']
        }

        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: purchase.id
        })

        self.login(self.username)

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), expected_response)

    def test_404_for_wrong_purchase_list_id(self):
        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: PurchaseList.objects.latest('id').id + 1,
            PURCHASE_URL_KWARG: self.purchase_list.id
        })
        expected_response = {"detail": "Not found."}

        self.login(self.username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), expected_response)

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), expected_response)

    def test_404_for_wrong_purchase_id(self):
        PurchaseFactory(purchase_list=self.purchase_list)

        url = reverse('purchase-manager:purchase', kwargs={
            GROUP_URL_KWARG: self.budget_group.id,
            PURCHASE_LIST_URL_KWARG: self.purchase_list.id,
            PURCHASE_URL_KWARG: Purchase.objects.latest('id').id + 1
        })
        expected_response = {"detail": "Not found."}

        self.login(self.username)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), expected_response)

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), expected_response)