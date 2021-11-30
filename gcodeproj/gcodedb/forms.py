from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import NumberInput, Textarea, Widget
from .models import G1code, Nhaplieuban, Gcode, Client, Inquiry,GDV, Nhaplieunhapkhau, Nhaplieumua, Phat, Sales, Supplier,Contract,Lydowin,Lydoout, Tienve, Danhgiagcode
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple

""" class ProjectPersonnelForm(forms.Form):
    class Media:
        # Django also includes a few javascript files necessary
        # for the operation of this form element. You need to
        # include <script src="/admin/jsi18n"></script>
        # in the template.
        css = {
            'all': ('admin/css/widgets.css',)
        }

    def __init__(self, *args, **kwargs):
        pid = kwargs.pop('pid')

        r = super(ProjectPersonnelForm, self).__init__(
            *args, **kwargs)

        p = G1code.objects.get(pk=pid)
        qs = Lydowin.objects.filter(
            pk__in=[u.pk for u in p.all_lydowin_not_in_g1code()]
        ).order_by('lydowincode')

        self.fields['personnel'] = \
            forms.ModelMultipleChoiceField(
                queryset=qs,
                widget=FilteredSelectMultiple(
                    'Personnel', is_stacked=False),
                label='')

        return r """

class MyForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(queryset=Lydowin.objects.all(),
                                        required=True,
                                        widget=FilteredSelectMultiple("Lydowin",is_stacked=False))
    class Media:
        css = {'all':('/admin/css/widgets.css', 'admin/css/overrides.css'),}
        js = ('/admin/jquery.js','/admin/jsi18n/')

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
            'sales',
            'sellcost',
            'status',
            'datedeliverylatest',
        ]
        labels = {
            'contractcode':'Contract No.',
            'contractnoclient':'Contract No. (Client)',
            'datesign':'Ngày ký kết',
            'client':'Khách hàng',
            'sales': 'Sales', 
            'sellcost': 'Giá bán',
            'status':'Trạng thái',
            'datedeliverylatest': 'Ngày giao hàng cuối cùng',
        }
        widgets = {
            'datedeliverylatest':InputDate(),
            'datesign':InputDate(),
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

class NlnkForm(forms.ModelForm):
    class Meta:
        model = Nhaplieunhapkhau
        exclude = ['dateupdate',
        ]
        widgets = {
            'ngaynhapkho':InputDate(),
            'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }

class SalesForm(forms.ModelForm):
    class Meta:
        model=Sales
        fields = '__all__'
        labels ={
            'salescode':'Tên viết tắt',
            'fullname':'Tên đầy đủ',
        }

class NlbForm(forms.ModelForm):
    class Meta:
        model = Nhaplieuban
        exclude = [
            'dateupdate',
            'g2code',
        ]
        widgets = {
            'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }
class NlmForm(forms.ModelForm):
    class Meta:
        model = Nhaplieumua
        exclude = [
            'dateupdate',
        ]
        widgets = {
			'motapo': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }


class TienveForm(forms.ModelForm):
    class Meta:
        model = Tienve
        fields ='__all__'
        widgets = {
            'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }

class DanhgiagcodeForm(forms.ModelForm):
    class Meta:
        model = Danhgiagcode
        fields = '__all__'

class PhatForm(forms.ModelForm):
    class Meta:
        model = Phat
        exclude = [
            'dateupdate',
        ]
        widgets = {
            'lydophat':Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'ghichu': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
        }