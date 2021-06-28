from .models import Client
import django_filters

class ClientFilter(django_filters.FilterSet):
    clientcode = django_filters.CharFilter(lookup_expr='icontains')
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Client
        fields = ['clientcode', 'fullname', ]