from django import forms
from django import forms
from django.db.models import fields
from .models import Gcode

class GcodeForm(forms.ModelForm):
    class Meta:
        model=Gcode
        fields="__all__"
"""     ma = forms.CharField(max_length=50, label='Gcode')
    mota = forms.CharField(max_length=100, label='Mô tả')
    xuatxu = forms.CharField(max_length=100, label='Xuất xứ')
    markupdinhmuc = forms.FloatField(label='Markup định mức') """
