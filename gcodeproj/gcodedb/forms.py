from django import forms
from django import forms
from django.db.models import fields
from .models import Gcode

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