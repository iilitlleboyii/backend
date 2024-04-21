from .models import User, Role
from django_filters.rest_framework import FilterSet, CharFilter


class UserFilterSet(FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains')
    nickname = CharFilter(field_name='nickname', lookup_expr='icontains')

    class Meta:
        model = User
        fields = [
            'username', 'nickname', 'is_active', 'is_staff', 'is_superuser'
        ]


class RoleFilterSet(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    code = CharFilter(field_name='code', lookup_expr='icontains')

    class Meta:
        model = Role
        fields = ['name', 'code', 'is_active']
