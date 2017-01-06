from rest_framework.permissions import BasePermission

from .models import BudgetGroup

GROUP_URL_KWARG = 'group_id'


class IsGroupMember(BasePermission):
    def has_permission(self, request, view):
        group_id = request.parser_context['kwargs'].get(GROUP_URL_KWARG)
        if group_id is None:
            return False
        try:
            group = BudgetGroup.objects.get(id=group_id)
            return group.is_member(request.user)
        except BudgetGroup.DoesNotExist:
            return False
