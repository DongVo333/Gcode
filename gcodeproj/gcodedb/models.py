from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model, ModelBase
from django.db.models.deletion import CASCADE, PROTECT
from django.forms import ModelForm
from django.db.models import F
from django.forms.fields import CharField

UNITS_CHOICES = (
    ("bộ", "bộ"),
    ("gói", "gói"),
    ("thùng", "thùng"),
    ("m", "m"),
    ("l", "l"),
    ("g", "g"),
    ("kg", "kg"),
    ("pcs", "pcs"),
)
SALES_CHOICES = (
    ("TuanLQ","TuanLQ"),
    ("TuanNT","TuanNT"),
    ("TramNB","TramNB"),
    ("ThuyLH","ThuyLH"),
    ("HungTC","HungTC"),
    ("HungND","HungND"),
)
RESULTS_CHOICES = (
    ("Win","Win"),
    ("Out","Out"),
)
STATUS_CHOICES =(
    ("Open","Open"),
    ("Close","Close"),
)
class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)

class Client(models.Model):
    clientcode = models.CharField(max_length=20, primary_key=True)
    fullname = models.CharField(max_length=200)
    def __str__(self):
        return self.clientcode
    class Meta:
        db_table = "gcodedb_client"
class Supplier (models.Model):
    suppliercode = models.CharField(max_length=20, primary_key=True)
    fullname = models.CharField(max_length=200)
    duyetpomax = models.FloatField()
    def __str__(self):
        return self.suppliercode
class Inquiry (models.Model):
    inquirycode = models.CharField(max_length=50, primary_key=True)
    datesubmitbid = models.DateField()
    clientcode  = models.ForeignKey(Client,on_delete=PROTECT, related_name= "fk_Inquiryclient")
    def __str__(self):
        return self.inquirycode
    class Meta:
        db_table = "gcodedb_inquiry"
class Contract (models.Model):
    contractcode  = models.CharField(max_length=50, primary_key=True)
    contractnoclient = models.CharField(max_length=50)
    datesign  = models.DateField()
    clientcode  = models.ForeignKey(Client,on_delete=PROTECT, related_name= "fk_Contractclient")
    dealine1 = models.DateField()
    dealine2 = models.DateField()
    sellcost = models.FloatField()
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="Open" )
    datedeliverylatest = models.DateField()
    def __str__(self):
        return self.contractcode

class Lydowin(models.Model):
    lydowincode = models.CharField(max_length=100, primary_key=True)
    detail  = models.TextField()
    def __str__(self):
        return self.lydowincode

class Lydoout(models.Model):
    lydooutcode = models.CharField(max_length=100, primary_key= True)
    detail  = models.TextField()
    def __str__(self):
        return self.lydooutcode

class GDV(models.Model):
    gdvcode = models.CharField(max_length=10, primary_key=True)
    fullname = models.CharField(max_length=50)
    def __str__(self):
        return self.gdvcode

class Gcode(models.Model):
    ma = models.CharField(max_length=20, primary_key= True)
    mota = models.TextField()
    markupdinhmuc = models.FloatField()
    class Meta:
        db_table = "gcodedb_gcode"
    def __str__(self):
        return self.ma

class G1code(models.Model):
    g1code = models.CharField(max_length=40)
    gcode = models.ForeignKey(Gcode, on_delete=PROTECT, related_name= "fk_g1codegcode")
    inquiry = models.ForeignKey(Inquiry,on_delete=PROTECT, related_name= "fk_g1codeinquiry")
    kymahieuinq = models.CharField(max_length=100)
    unitinq = models.CharField(max_length = 20,choices = UNITS_CHOICES,default = 'pcs')
    qtyinq = models.FloatField()
    supplier = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fk_g1codesupplier")
    xuatxuinq = models.CharField(max_length=100)
    nsxinq = models.CharField(max_length=50)
    sttitb = models.IntegerField()
    groupitb = models.CharField(max_length=5)
    sales = models.CharField(max_length=10,choices= SALES_CHOICES,default="TuanLQ")
    dongiamuainq = models.FloatField()
    dongiachaoinq = models.FloatField()
    markupinq = models.FloatField()
    resultinq = models.CharField(max_length=10, choices= RESULTS_CHOICES,default="Win", null= True, blank= True)
    lydowin = models.ManyToManyField(Lydowin, related_name='fk_g1codelydowin',null= True, blank= True)
    lydoout = models.ManyToManyField(Lydoout, related_name='fk_g1codelydoout',null= True, blank= True)
    ghichu = models.TextField(null=True,blank= True)
    gdvinq = models.ForeignKey(GDV, on_delete=PROTECT)
    dateupdate  = models.DateField()
    class Meta:
       unique_together = ("gcode", "inquirycode")
    def __str__(self):
        return self.g1code
    @property
    def g1code(self):
        self.g1code = str(self.gcode)+'-'+str(self.inquirycode)
        return self.g1code

class G2code(models.Model):
    contractcode = models.ForeignKey(Contract,to_field='contractcode',on_delete=PROTECT, related_name='fkg2code_contract',null=True)
    dongiachaohdb = models.FloatField(null=True)
    thanhtienchaohdb = models.FloatField(null=True)
    pono = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=30,null=True)
    g1code = models.OneToOneField(G1code,on_delete=PROTECT,related_name='fkg2code_g1code',primary_key=True)
    ghichu = models.TextField(null=True,blank= True)
    gdvhdb = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fkg2code_gdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code)
    @property
    def g2code(self):
        return str(self.g1code.gcode)+'-'+str(self.contractcode)
    def gcode(self):
        return self.g1code.gcode
class POdetail(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fkpo_g2code',primary_key=True)
    motapo = models.TextField(null=True)
    kymahieupo = models.CharField(max_length=100,null=True)
    unitpo = models.CharField(max_length = 20,choices = UNITS_CHOICES,default = 'pcs',null=True)
    qtypo = models.FloatField()
    suppliercodepo = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fkg2code_supplier",null=True)
    xuatxupo = models.CharField(max_length=100,null=True)
    nsxpo = models.CharField(max_length=50,null=True)
    dongiamuapo = models.FloatField(null=True)
    thanhtienmuapo = models.FloatField(null=True)
    ghichu = models.TextField(null=True)
    gdvpo = models.ForeignKey(GDV,to_field='gdvcode',on_delete=PROTECT, related_name='fkpo_gdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code.gcode)+"-"+str(self.pono)
class Kho(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fkkho_g2code',primary_key=True)
    qtykho = models.FloatField(null=True)
    dongiafreight = models.FloatField(null=True)
    ngaynhapkho = models.DateField(null=True)
    gdvkho = models.ForeignKey(GDV, to_field='gdvcode',on_delete=PROTECT,related_name='fkkho_gdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) + "kho"
    @property
    def thanhtienfreight(self):
        return (self.qtykho or 0)*(self.dongiafreight or 0)
    def motahanghoa(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    def donvitinh(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo

class Giaohang(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fkgiaohang_g2code',primary_key=True)
    qtygiaohang = models.FloatField(null=True)
    ngaygiaohang = models.DateField(null=True)
    gdvgiaohang = models.ForeignKey(GDV,to_field='gdvcode',on_delete=PROTECT,related_name='fkgiaohang_gdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) +"giao hang"
    @property
    def motahanghoa(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    def donvitinh(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
class Phat(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fkphat_g2code',primary_key=True)
    qtyphat = models.FloatField(null=True)
    tongphat = models.FloatField(null=True)
    lydophat = models.TextField(null=True)
    gdvphat = models.ForeignKey(GDV,to_field='gdvcode',on_delete=PROTECT,related_name='fkphat_gdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) + "phat"
    @property
    def motahanghoa(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    def donvitinh(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo

class Danhgiacode(models.Model):
    danhgiacode=models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.danhgiacode 

class DanhgiaNSX(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fkdanhgia_g2code',primary_key=True)
    danhgiacode = models.ManyToManyField(Danhgiacode,related_name='fk_danhgiacode',null=True)
    comment = models.TextField(null=True)
    gdvdanhgia = models.ForeignKey(GDV,to_field='gdvcode',on_delete=PROTECT,related_name='fkdanhgia_gdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) + "danh gia"   
    @property
    def motahanghoa(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    def donvitinh(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
    def soluong(self):
        return POdetail.objects.get(g2code = self.g2code).qtypo
    def xuatxu(self):
        return POdetail.objects.get(g2code = self.g2code).xuatxupo
    def supplier(self):
        return POdetail.objects.get(g2code = self.g2code).suppliercodepo
    def dongiamua(self):
        return POdetail.objects.get(g2code = self.g2code).dongiamuapo
    def thanhtienmua(self):
        return POdetail.objects.get(g2code = self.g2code).thanhtienmuapo

class Tienve(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fktienve_g2code',primary_key=True)
    qtytienve = models.FloatField(null=True)
    dongiatienve = models.FloatField(null=True)
    @property
    def tongtienve(self):
        return (self.qtytienve or 0)*(self.dongiatienve or 0)
