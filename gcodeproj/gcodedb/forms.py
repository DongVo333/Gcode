from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import NumberInput, Textarea, Widget
from .models import DanhgiaNSX, G1code, G2code, Gcode, Client, Giaohang, Inquiry,GDV, Kho, POdetail, Phat, Sales, Supplier,Contract,Lydowin,Lydoout, Tienve, Danhgiacode
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
            'markupdinhmuc':'Markup định mức',
            'ngaywin':'Ngày Win gần nhất',
            'ngayout':'Ngày Out gần nhất',
        }
        widgets = {
            'mota':forms.Textarea(attrs={'cols':30,'rows':1, 'id':'autosize'}),
            'ngaywin':InputDate(),
            'ngayout':InputDate(),
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
            'client',
		]
        widgets = {
            'datesubmitbid':InputDate()
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = G1code
        exclude = [
            'dateupdate',
            'g1code',
        ]
        widgets = {
			'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'dongiamuainq': NumberInput(attrs={'class':'dgm'}),
            'dongiachaoinq': NumberInput(attrs={'class':'dgc'}),
            'qtyinq':NumberInput(attrs={'class':'qty'}),
            'lydowin': forms.CheckboxSelectMultiple,
            'lydoout': forms.CheckboxSelectMultiple,
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
            'client',
            'dealine1',
            'dealine2', 
            'sellcost',
            'status',
            'datedeliverylatest',
        ]
        labels = {
            'contractcode':'Contract',
            'contractnoclient':'Contract No. (Client)',
            'datesign':'Ngày ký kết',
            'client':'Khách hàng',
            'dealine1':'Deadline 1',
            'dealine2':'Deadline 2', 
            'sellcost': 'Giá bán',
            'status':'Trạng thái',
            'datedeliverylatest': 'Ngày giao hàng cuối cùng',
        }
        widgets = {
            'datedeliverylatest':InputDate(),
            'datesign':InputDate(),
            'dealine1':InputDate(),
            'dealine2':InputDate(),
        }

class LydowinForm(forms.ModelForm):
    class Meta:
        model = Lydowin
        fields = [
            'lydowincode',
            'detail',
        ]
        widgets = {
			'detail': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }

class LydooutForm(forms.ModelForm):
    class Meta:
        model = Lydoout
        fields = [
            'lydooutcode',
            'detail',
        ]
        widgets = {
			'detail': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }

class OfferResultForm(forms.ModelForm):
    class Meta:
        model = G1code
        fields = [
            'gcode',
            'inquiry',
            'resultinq',
            'lydowin',
            'lydoout',
        ]
        labels = {
            'gcode':'Gcode',
            'inquiry':'Inquiry',
            'resultinq':'Result',
            'lydowin':'Lý do win',
            'lydoout':'Lý do out',
        }
        widgets = {
            'lydowin': forms.CheckboxSelectMultiple,
            'lydoout': forms.CheckboxSelectMultiple,
        }

class KhoForm(forms.ModelForm):
    class Meta:
        model = Kho
        exclude = ['dateupdate',
        ]
        widgets = {
            'ngaynhapkho':InputDate(),
        }

class SalesForm(forms.ModelForm):
    class Meta:
        model=Sales
        fields = '__all__'
        labels ={
            'salescode':'Tên viết tắt',
            'fullname':'Tên đầy đủ',
        }

class HDBForm(forms.ModelForm):
    class Meta:
        model = G2code
        exclude = [
            'dateupdate',
            'g2code',
        ]

class POForm(forms.ModelForm):
    class Meta:
        model = POdetail
        exclude = [
            'dateupdate',
        ]
        widgets = {
			'motapo': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }

class GiaohangForm(forms.ModelForm):
    class Meta:
        model = Giaohang
        exclude = [
            'dateupdate',
        ]
        widgets = {
            'ngaygiaohang':InputDate,
        }

class TienveForm(forms.ModelForm):
    class Meta:
        model = Tienve
        fields ='__all__'

class DanhgiaNSXForm(forms.ModelForm):
    class Meta:
        model = DanhgiaNSX
        exclude = [
            'dateupdate',
        ]
        labels ={
            'g2code':'Gcode-Contract',
            'danhgiacode':'Đánh giá code',
            'comment':'Comment',
            'gdvdanhgia':'Giao dịch viên',
        }
        widgets = {
            'comment':Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'danhgiacode':forms.CheckboxSelectMultiple,
        }

class DanhgiacodeForm(forms.ModelForm):
    class Meta:
        model = Danhgiacode
        fields = '__all__'

class PhatForm(forms.ModelForm):
    class Meta:
        model = Phat
        exclude = [
            'dateupdate',
        ]
        widgets = {
            'lydophat':Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }