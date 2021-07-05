from django import forms
from .models import Client, G1code
import django_filters

class ClientFilter(django_filters.FilterSet):
    clientcode = django_filters.CharFilter(lookup_expr='icontains')
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Client
        fields = ['clientcode', 'fullname', ]

class G1codeFilter(django_filters.FilterSet):
    inquirycode = django_filters.CharFilter()
    class Meta:
        model = G1code
        fields = ['inquirycode',]


class InquiryFilter(forms.Form):
    inquiryfilter = forms.CharField(max_length=40)