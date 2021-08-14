from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model, ModelBase
from django.db.models.deletion import PROTECT, PROTECT
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
    clientcode = models.CharField(max_length=20)
    fullname = models.CharField(max_length=200)
    def __str__(self):
        return self.clientcode
    class Meta:
        db_table = "gcodedb_client"
class Supplier (models.Model):
    suppliercode = models.CharField(max_length=20)
    fullname = models.CharField(max_length=200)
    duyetpomax = models.FloatField()
    def __str__(self):
        return self.suppliercode
class Inquiry (models.Model):
    inquirycode = models.CharField(max_length=50)
    datesubmitbid = models.DateField()
    client  = models.ForeignKey(Client,on_delete=PROTECT, related_name= "fk_Inquiryclient")
    def __str__(self):
        return self.inquirycode
    class Meta:
        db_table = "gcodedb_inquiry"
class Contract (models.Model):
    contractcode  = models.CharField(max_length=50)
    contractnoclient = models.CharField(max_length=50)
    datesign  = models.DateField()
    client  = models.ForeignKey(Client,on_delete=PROTECT, related_name= "fk_Contractclient")
    dealine1 = models.DateField()
    dealine2 = models.DateField()
    sellcost = models.FloatField()
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="Open" )
    datedeliverylatest = models.DateField()
    def __str__(self):
        return self.contractcode

class Lydowin(models.Model):
    lydowincode = models.CharField(max_length=100)
    detail  = models.TextField()
    def __str__(self):
        return self.lydowincode

class Lydoout(models.Model):
    lydooutcode = models.CharField(max_length=100)
    detail  = models.TextField()
    def __str__(self):
        return self.lydooutcode

class GDV(models.Model):
    gdvcode = models.CharField(max_length=10)
    fullname = models.CharField(max_length=50)
    def __str__(self):
        return self.gdvcode

class Gcode(models.Model):
    ma = models.CharField(max_length=20)
    mota = models.TextField()
    kymahieuinq = models.CharField(max_length=100,null=True,blank=True)
    markupdinhmuc = models.FloatField(null=True,blank=True)
    ngaywin = models.DateField(null=True, blank=True)
    ngayout = models.DateField(null=True, blank= True)
    class Meta:
        db_table = "gcodedb_gcode"
    def __str__(self):
        return self.ma

class Sales(models.Model):
    salescode = models.CharField(max_length=20)
    fullname = models.CharField(max_length=70)
    def __str__(self):
        return self.salescode
        
class G1code(models.Model):
    g1code = models.CharField(max_length=40)
    gcode = models.ForeignKey(Gcode, on_delete=PROTECT, related_name= "fk_g1codegcode")
    inquiry = models.ForeignKey(Inquiry,on_delete=PROTECT, related_name= "fk_g1codeinquiry")
    unitinq = models.CharField(max_length = 20,choices = UNITS_CHOICES,default = 'pcs')
    qtyinq = models.FloatField()
    supplier = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fk_g1codesupplier")
    xuatxuinq = models.CharField(max_length=100)
    nsxinq = models.CharField(max_length=50)
    sttitb = models.IntegerField()
    groupitb = models.CharField(max_length=5)
    sales = models.ForeignKey(Sales,on_delete=PROTECT, related_name= "fk_g1codesales")
    dongiamuainq = models.FloatField()
    dongiachaoinq = models.FloatField()
    resultinq = models.CharField(max_length=10, choices= RESULTS_CHOICES,default="Win", null= True, blank= True)
    lydowin = models.ManyToManyField(Lydowin, related_name='fk_g1codelydowin',null= True, blank= True)
    lydoout = models.ManyToManyField(Lydoout, related_name='fk_g1codelydoout',null= True, blank= True)
    ghichu = models.TextField(null=True,blank= True)
    gdvinq = models.ForeignKey(GDV, on_delete=PROTECT)
    dateupdate  = models.DateField()
    class Meta:
       unique_together = ("gcode", "inquiry")
    def __str__(self):
        return self.g1code
    @property
    def thanhtienmua(self):
        return (self.qtyinq or 0)*(self.dongiamuainq or 0)
    @property
    def thanhtienchao(self):
        return (self.qtyinq or 0)*(self.dongiachaoinq or 0)
    @property
    def mota(self):
        return self.gcode.mota
    @property
    def markupinq(self):
        if self.dongiamuainq > 0:
            return (self.dongiachaoinq or 0)/(self.dongiamuainq)
        else:
            return None
class G2code(models.Model):
    g2code = models.CharField(max_length=40)
    contract = models.ForeignKey(Contract,on_delete=PROTECT, related_name='fk_g2codecontract',null=True)
    dongiachaohdb = models.FloatField(null=True)
    pono = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=30,null=True)
    g1code = models.OneToOneField(G1code,on_delete=PROTECT,related_name='fk_g2codeg1code',limit_choices_to={'resultinq': 'Win'})
    ghichu = models.TextField(null=True,blank= True)
    gdvhdb = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_g2codegdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code)
    @property
    def thanhtienchaohdb(self):
        return (self.g1code.qtyinq or 0)*(self.dongiachaohdb or 0)
    @property
    def mota(self):
        return (self.g1code.gcode.mota)
    @property
    def unit(self):
        return self.g1code.unitinq 
    @property
    def qty(self):
        return self.g1code.qtyinq
    @property
    def inquiry(self):
        return self.g1code.inquiry.inquirycode
    @property
    def supplier(self):
        return self.g1code.supplier.suppliercode
    @property
    def kymahieu(self):
        return self.g1code.gcode.kymahieuinq
    @property
    def nsx(self):
        return self.g1code.nsxinq
    @property
    def xuatxu(self):
        return self.g1code.xuatxuinq
    @property
    def gcode(self):
        return self.g1code.gcode.ma
    @property
    def qtychuadat(self):
        if POdetail.objects.filter(g2code=self).count()>0:
            return self.qty-POdetail.objects.get(g2code=self).qtypo
        else:
            return self.qty
    @property
    def qtychuanhapkho(self):
        if POdetail.objects.filter(g2code=self).count()>0:
            if Kho.objects.filter(g2code=self).count()>0:
                return POdetail.objects.get(g2code=self).qtypo-Kho.objects.get(g2code=self).qtykho
            else:
                return POdetail.objects.get(g2code=self).qtypo
        else:
            return 0
    @property
    def qtychuagiao(self):
        if Kho.objects.filter(g2code=self).count()>0:
            if Giaohang.objects.filter(g2code=self).count()>0:
                return Kho.objects.get(g2code=self).qtykho - Giaohang.objects.get(g2code=self).qtygiaohang
            else:
                return Kho.objects.get(g2code=self).qtykho
        else:
            return 0
    @property
    def qtypo(self):
        if POdetail.objects.filter(g2code=self).count()>0:
            return POdetail.objects.get(g2code=self).qtypo
        else:
            return 0
    @property
    def qtykho(self):
        if Kho.objects.filter(g2code=self).count()>0:
            return Kho.objects.get(g2code=self).qtykho
        else:
            return 0
    @property
    def qtygiaohang(self):
        if Giaohang.objects.filter(g2code=self).count()>0:
            return Giaohang.objects.get(g2code=self).qtygiaohang
        else:
            return 0
    @property
    def qtyphat(self):
        if Phat.objects.filter(g2code=self).count()>0:
            return Phat.objects.get(g2code=self).qtyphat
        else:
            return 0
    @property
    def qtytienve(self):
        if Tienve.objects.filter(g2code=self).count()>0:
            return Tienve.objects.get(g2code=self).qtytienve
        else:
            return 0
    @property
    def dongiamuapo(self):
        if POdetail.objects.filter(g2code=self).count()>0:
            return POdetail.objects.get(g2code=self).dongiamuapo
        else:
            return 0
    @property
    def dongiamuainq(self):
        return self.g1code.dongiamuainq
    @property
    def dongiafreight(self):
        if Kho.objects.filter(g2code=self).count()>0:
            return Kho.objects.get(g2code=self).dongiafreight
        else:
            return 0
    @property
    def tongphat(self):
        if Phat.objects.filter(g2code=self).count()>0:
            return Phat.objects.get(g2code=self).tongphat
        else:
            return 0
    @property
    def tongtienve(self):
        if Tienve.objects.filter(g2code=self).count()>0:
            return Tienve.objects.get(g2code=self).dongiatienve * Tienve.objects.get(g2code=self).qtytienve
        else:
            return 0
            
class POdetail(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fk_pog2code')
    motapo = models.TextField(null=True)
    kymahieupo = models.CharField(max_length=100,null=True)
    unitpo = models.CharField(max_length = 20,choices = UNITS_CHOICES,default = 'pcs',null=True)
    qtypo = models.FloatField()
    supplier = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fk_g2codesupplier",null=True)
    xuatxupo = models.CharField(max_length=100,null=True)
    nsxpo = models.CharField(max_length=50,null=True)
    dongiamuapo = models.FloatField(null=True)
    ghichu = models.TextField(null=True,blank=True)
    gdvpo = models.ForeignKey(GDV,on_delete=PROTECT, related_name='fk_pogdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code.g1code.gcode)+"-"+str(self.pono)
    @property
    def thanhtienmuapo(self):
        return (self.qtypo or 0)*(self.dongiamuapo or 0)
    @property
    def gcode(self):
        return (self.g2code.g1code.gcode.ma)
    @property
    def pono(self):
        return (self.g2code.pono)
class Kho(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fk_khog2code')
    qtykho = models.FloatField(null=True)
    dongiafreight = models.FloatField(null=True)
    ngaynhapkho = models.DateField(null=True)
    ghichu = models.TextField(null=True,blank= True)
    gdvkho = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_khogdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) + "kho"
    @property
    def thanhtienfreight(self):
        return (self.qtykho or 0)*(self.dongiafreight or 0)
    @property
    def mota(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    @property
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    @property
    def unit(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
    @property
    def gcode(self):
        return self.g2code.g1code.gcode.ma

class Giaohang(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fk_giaohangg2code')
    qtygiaohang = models.FloatField(null=True)
    ngaygiaohang = models.DateField(null=True)
    ghichu = models.TextField(null=True,blank= True)
    gdvgiaohang = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_giaohanggdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) +"giao hang"
    @property
    def mota(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    @property
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    @property
    def unit(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
    @property
    def gcode(self):
        return self.g2code.g1code.gcode.ma
    @property
    def contract(self):
        return self.g2code.contract.contractcode
class Phat(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fk_phatg2code')
    qtyphat = models.FloatField(null=True)
    tongphat = models.FloatField(null=True)
    lydophat = models.TextField(null=True)
    ghichu = models.TextField(null=True,blank= True)
    gdvphat = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_phatgdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) + "phat"
    @property
    def mota(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    @property
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    @property
    def unit(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
    @property
    def dongiaphat(self):
        if self.qtyphat > 0:
            return (self.tongphat or 0)/(self.qtyphat)
        else:
            return None
    @property
    def gcode(self):
        return  self.g2code.g1code.gcode.ma
    @property
    def contract(self):
        return self.g2code.contract.contractcode
    @property
    def client(self):
        return self.g2code.contract.client.clientcode
    @property
    def nsx(self):
        return POdetail.objects.get(g2code = self.g2code).nsxpo
    @property
    def xuatxu(self):
        return POdetail.objects.get(g2code = self.g2code).xuatxupo
    
class Danhgiacode(models.Model):
    danhgiacode=models.CharField(max_length=100)
    def __str__(self):
        return self.danhgiacode 

class DanhgiaNCC(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fk_danhgiag2code')
    danhgiacode = models.ManyToManyField(Danhgiacode,related_name='fk_danhgiacode',null=True)
    comment = models.TextField(null=True,blank=True)
    gdvdanhgia = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_danhgiagdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code) + "danh gia"   
    @property
    def mota(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    @property
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    @property
    def unit(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
    @property
    def qty(self):
        return POdetail.objects.get(g2code = self.g2code).qtypo
    @property
    def xuatxu(self):
        return POdetail.objects.get(g2code = self.g2code).xuatxupo
    @property
    def supplier(self):
        return POdetail.objects.get(g2code = self.g2code).supplier
    @property
    def dongiamua(self):
        return POdetail.objects.get(g2code = self.g2code).dongiamuapo
    @property
    def thanhtienmua(self):
        return POdetail.objects.get(g2code = self.g2code).thanhtienmuapo
    @property
    def gcode(self):
        return (self.g2code.g1code.gcode.ma)
    @property
    def pono(self):
        return (self.g2code.pono)
    @property
    def nsx(self):
        return POdetail.objects.get(g2code = self.g2code).nsxpo

class Tienve(models.Model):
    g2code = models.OneToOneField(G2code,on_delete=PROTECT,related_name='fk_tienveg2code')
    qtytienve = models.FloatField(null=True)
    dongiatienve = models.FloatField(null=True)
    ghichu = models.TextField(null=True,blank= True)
    def __str__(self):
        return str(self.g2code) + "tien ve"   
    @property
    def tongtienve(self):
        return (self.qtytienve or 0)*(self.dongiatienve or 0)
    @property
    def mota(self):
        return POdetail.objects.get(g2code = self.g2code).motapo
    @property
    def kymahieu(self):
        return POdetail.objects.get(g2code = self.g2code).kymahieupo
    @property
    def unit(self):
        return POdetail.objects.get(g2code = self.g2code).unitpo
    @property
    def soluong(self):
        return POdetail.objects.get(g2code = self.g2code).qtypo
    @property
    def xuatxu(self):
        return POdetail.objects.get(g2code = self.g2code).xuatxupo
    @property
    def gcode(self):
        return self.g2code.g1code.gcode.ma
    @property
    def contract(self):
        return self.g2code.contract.contractcode
    @property
    def client(self):
        return self.g2code.contract.client.clientcode
    @property
    def nsx(self):
        return POdetail.objects.get(g2code = self.g2code).nsxpo
    @property
    def supplier(self):
        return POdetail.objects.get(g2code = self.g2code).supplier

class ScanOrder(models.Model):
    gcode = models.ManyToManyField(Gcode,related_name='fk_scanordergcode',null=True)