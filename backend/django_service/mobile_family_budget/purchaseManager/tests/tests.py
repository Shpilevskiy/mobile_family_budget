from rest_framework import status
from rest_framework.reverse import reverse

from mobile_family_budget.tests.base import BaseCase

from account.factorys.user_factory import UserFactory

from purchaseManager.factorys.purchases_list_factory import PurchasesListFactory
from purchaseManager.models import PurchaseList


class PurchasesListsTestCase(BaseCase):
    def test_only_authorized_user_can_reach_endpoint(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={'group_id': self.budget_group.id})
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
        url = reverse('purchase-manager:purchases-lists', kwargs={'group_id': self.budget_group.id})
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
        url = reverse('purchase-manager:purchases-lists', kwargs={'group_id': self.budget_group.id})
        PurchasesListFactory.create_batch(4, budget_group=self.budget_group)

        expected_response = [{'id': purchase_list.id, 'name': purchase_list.name}
                             for purchase_list in PurchaseList.objects.filter(budget_group=self.budget_group)]

        self.login(self.username)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], expected_response)

    def test_user_can_create_new_purchase_list(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={'group_id': self.budget_group.id})

        new_list_name = "my_new_list"
        expected_response = {'id': 1, 'name': 'my_new_list'}

        self.login(self.username)
        response = self.client.post(url, {"name": new_list_name})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_response)
        self.assertTrue(PurchaseList.objects.get(budget_group=self.budget_group, name=new_list_name))

    def test_data_is_required(self):
        url = reverse('purchase-manager:purchases-lists', kwargs={'group_id': self.budget_group.id})

        expected_response = {'name': ['This field is required.']}

        self.login(self.username)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expected_response)
    