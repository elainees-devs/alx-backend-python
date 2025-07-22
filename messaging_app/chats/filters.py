import  django_filters
from .models import Message


class MessageFilters(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='sender_id')
    created_after = django_filters.DateFilter(field_name='sent_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='sent_at', lookup_expr='lte')


class Meta:
    model = Message
    fields = ['user', 'created_at', 'created_before']

