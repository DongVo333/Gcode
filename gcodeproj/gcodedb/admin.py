from django.contrib import admin
from .models import Baocaogiaohang, Contract, Danhgiagcode, G1code, Nhaplieuban, GDV, Gcode,Inquiry,Client, Nhaplieunhapkhau, Nhaplieumua, PAMHop, Phat, Sales,Supplier,Lydowin,Lydoout, Tienve, Tinhtrangiaiquyetkhokhan, Unit, Yearcode
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Permission)
admin.site.register(Unit)
admin.site.register(Sales)
admin.site.register(Baocaogiaohang)
admin.site.register(Tinhtrangiaiquyetkhokhan)
admin.site.register(PAMHop)
admin.site.register(GDV)
admin.site.register(Yearcode)
