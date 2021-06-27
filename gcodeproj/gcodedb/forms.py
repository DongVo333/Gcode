from django import forms
from django import forms
from django.db.models import fields
from .models import Gcode, Client, Inquiry
from django.conf import settings

class GcodeForm(forms.ModelForm):
    class Meta:
        model=Gcode
        fields="__all__"
        labels = {
            'ma':'Gcode',
            'mota':'Mô tả',
            'markupdinhmuc':'Markup định mức'
        }
        widgets = {
            'mota':forms.Textarea(attrs={'cols':30, 'rows':4})
        }
"""     ma = forms.CharField(max_length=50, label='Gcode')
    mota = forms.CharField(max_length=100, label='Mô tả')
    markupdinhmuc = forms.FloatField(label='Markup định mức') """
class SearchQueryForm(forms.Form):
    query_field = forms.ChoiceField(
        choices=(
            ('clientcode', 'Client'),
            ('fullname', 'Full Name')
        ),
        widget=forms.Select()
    )

    lookup = forms.ChoiceField(
        choices=(
            ('iexact', 'Equals'),
            ('icontains', 'Contains')
        ),
        widget=forms.Select()
    )

    query = forms.CharField(widget=forms.TextInput())
class ClientForm(forms.ModelForm):
	class Meta:
		model = Client

		fields = [
			'clientcode',
			'fullname',
		]

		labels = {
			'clientcode': 'Tên viết tắt',
			'fullname':'Tên đầy đủ',
		}


class InquiryForm(forms.ModelForm):
	class Meta:
		model = Inquiry

		fields = [
			'inquirycode',
			'datesubmitbid',
		]

		widgets = {
			'inquirycode': forms.TextInput(attrs={'class': 'formset-field'}),
			'datesubmitbid': forms.DateInput()
		}