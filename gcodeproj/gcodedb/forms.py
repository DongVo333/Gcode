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
            'gcode':'Gcode',
            'descriptionban':'Mô tả',
            'PNban':'Part Number',
            'markupdinhmuc':'Markup định mức',
            'ngaywin':'Ngày Win gần nhất',
            'ngayout':'Ngày Out gần nhất',
        }
        widgets = {
            'descriptionban':forms.Textarea(attrs={'cols':30,'rows':1, 'id':'autosize'}),
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
            'deadlineghnlb',
            'deadlineghnlm',
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
            'deadlineghnlb':'Deadline giao hàng NLB',
            'deadlineghnlm':'Deadline giao hàng NLM',
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
        fields = [
            'g2code',
            'nlhrkksupplier',
            'ntthcmtkvam',
            'qtykho',
            'ttkh',
            'dgnk',
            'nghttckh',
            'qtygh',
            'bcgh',
            'ghichu',
        ]
        labels = {
            'g2code':'ID item Gcode-Contract',
            'nlhrkksupplier':'Ngày lấy hàng ra khỏi kho Supplier',
            'ntthcmtkvam':'Ngày thực tế hàng có mặt tại kho VAM',
            'qtykho':'Quantity nhập kho',
            'ttkh':'Tình trạng kiểm hàng',
            'dgnk':'Đơn giá nhập kho',
            'nghttckh':'Ngày giao hàng thực tế cho KH',
            'qtygh':'Quantity giao hàng',
            'bcgh':'Báo cáo giao hàng',
            'ghichu':'Ghi chú cho giao hàng',
        }
        widgets = {
            'nghttckh':InputDate(),
            'nlhrkksupplier':InputDate(),
            'ntthcmtkvam':InputDate(),
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
        fields = [
            'gcodeban',
            'contractno',
            'dongiachaohdb',
            'status',
            'descriptionban',
            'MNFban',
            'qtyban',
            'unitban',
        ]
        labels = {
            'gcodeban':'ID Gcode',
            'contractno':'Contract No.',
            'dongiachaohdb':'Unit Price (VND)',
            'status':'Status',
            'descriptionban':'Description',
            'MNFban':'MNF',
            'qtyban':'Quantity bán',
            'unitban': 'Unit',
        }

        widgets = {
            'deadlinegh':InputDate(),
        }
class NlmForm(forms.ModelForm):
    class Meta:
        model = Nhaplieumua
        fields = [
            'g2code',
            'pono',
            'supplier',
            'datesignpo',
            'deliveryterm',
            'qhxk',
            'deadlinegatvam',
            'pamhvamts',
            'nttd1',
            'stttd1',
            'nttd2',
            'stttd2',
            'nttdn',
            'stttdn',
            'descriptionmua',
            'MNFmua',
            'origin',
            'PNmua',
            'unitmua',
            'qtymua',
            'currency',
            'unitprice',
            'thueVAT',
            'certificate',
            'danhgiagcode',
            'reasondelay',
            'ctrrkt',
            'vdkk',
            'ykcpal',
            'ykcsales',
            'ttgqkk',
            'datesignpoplan',
            'budget',
        ]
        labels = {
            'g2code':'ID Item Gcode-Contract',
            'pono':'PO No.',
            'supplier':'Supplier',
            'datesignpo':'Ngày ký PO',
            'deliveryterm':'Delivery term',
            'qhxk':'Quốc gia xuất khẩu',
            'deadlinegatvam':'Deadline hàng có mặt tại kho Vam',
            'pamhvamts':'PAMH (Vam / TS)',
            'nttd1':'Ngày thanh toán đợt 1',
            'stttd1':'Số tiền thanh toán đợt 1 (currency bao gồm VAT / GST)',
            'nttd2':'Ngày thanh toán đợt 2',
            'stttd2':'Số tiền thanh toán đợt 2 (currency bao gồm VAT / GST)',
            'nttdn':'Ngày thanh toán đợt n',
            'stttdn':'Số tiền thanh toán đợt n (currency bao gồm VAT / GST)',
            'descriptionmua':'Description',
            'MNFmua':'MNF',
            'origin':'Origin',
            'PNmua':'Part Number',
            'unitmua':'Unit',
            'qtymua':'Quantity',
            'currency':'Currency',
            'dongiaban':'Unit pirce (currency)',
            'thueVAT':'Thuế VAT / GST (currency)',
            'certificate':'Certificate',
            'danhgiagcode':'Đánh giá Gcode',
            'reasondelay':'Lý do hàng trễ so với deadline',
            'ctrrkt': 'Chi tiết rủi ro kỹ thuật',
            'vdkk':'Vấn đề khó khăn',
            'ykcpal':'Ý kiến của Pal',
            'ykcsales':'Ý kiến của Sales',
            'ttgqkk':'Tình trạng giải quyết khó khăn',
            'datesignpoplan':'Ngày ký PO (plan)',
            'budget':'Budget (VND)',
        }
        widgets = {
            'datesignpo':InputDate(),
            'deadlinegatvam':InputDate(),
            'nttd1':InputDate(),
            'nttd2':InputDate(),
            'nttdn':InputDate(),
            'datesignpoplan':InputDate(),
			'descriptionmua': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'reasondelay': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'ctrrkt': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'vdkk': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'ykcpal': Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),
            'ykcsales':Textarea(attrs={'cols':30, 'rows':1, 'id':'autosize'}),

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