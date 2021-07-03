from django import forms
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import NumberInput, Textarea, Widget
from .models import G1code, Gcode, Client, Inquiry,GDV, Supplier,Contract,lydowin,lydoout
from django.conf import settings

class InputDate(forms.DateInput):
    input_type = 'date'

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
            'mota':forms.Textarea(attrs={'cols':30,'rows':1, 'id':'autosize'})
        }

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
            'clientcode',
		]
        widgets = {
            'datesubmitbid':InputDate()
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = G1code
        fields = [
            'gcode',
            'kymahieuinq',
            'unit',
            'qtyinq',
            'suppliercode',
            'nsxinq',
            'sttitb',
            'groupitb',
            'sales',
            'dongiamuainq',
            'thanhtienmuainq',
            'dongiachaoinq',
            'thanhtienchaoinq',
            'markupinq',
            'resultinq',
            'ghichu',
            'gdvinq',
        ]
        widgets = {
			'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'dongiamuainq': NumberInput(attrs={'class':'dgm'}),
            'thanhtienmuainq': NumberInput(attrs={'class':'ttm'}),
            'dongiachaoinq': NumberInput(attrs={'class':'dgc'}),
            'thanhtienchaoinq': NumberInput(attrs={'class':'ttc'}),
            'qtyinq':NumberInput(attrs={'class':'qty'}),
		}

class GDVForm(forms.ModelForm):
    class Meta:
        model = GDV
        fields = [
            'gdvcode',
            'fullname',
		]

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'suppliercode',
            'fullname',
            'duyetpomax',
        ]
        labels = {
			'suppliercode': 'Supplier',
			'fullname':'Tên đầy đủ',
            'duyetpomax':'Duyệt PO (Max)',
        }
        widgets = {
            'duyetpomax': NumberInput(attrs={'type':'currency'})
        }

class ContractForm(forms.ModelForm):
    class Meta:
        model= Contract
        fields = [
            'contractcode',
            'contractnoclient',
            'datesign',
            'clientcode',
            'dealine1',
            'dealine2', 
            'sellcost',
            'status',
            'datedeliverylatest',
        ]
        widgets = {
            'datedeliverylatest':InputDate(),
            'datesign':InputDate(),
            'dealine1':InputDate(),
            'dealine2':InputDate(),
        }

class LydowinForm(forms.ModelForm):
    class Meta:
        model = lydowin
        fields = [
            'lydowincode',
            'detail',
        ]
        widgets = {
			'detail': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }

class LydooutForm(forms.ModelForm):
    class Meta:
        model = lydoout
        fields = [
            'lydooutcode',
            'detail',
        ]
        widgets = {
			'detail': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }