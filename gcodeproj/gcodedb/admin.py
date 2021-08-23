from django.contrib import admin
from .models import Contract, DanhgiaNCC, Danhgiacode, G1code, G2code, GDV, Gcode, Giaohang,Inquiry,Client, Kho, POdetail, Phat, Sales,Supplier,Lydowin,Lydoout, Tienve
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Permission)