from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.forms import ModelForm
from django.db.models import F

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

class lydowin(models.Model):
    lydowincode = models.CharField(max_length=100, primary_key=True)
    detail  = models.TextField()
    def __str__(self):
        return self.lydowincode

class lydoout(models.Model):
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
    _g1code = None
    gcode = models.ForeignKey(Gcode, on_delete=PROTECT, related_name= "fk_g1codegcode")
    inquirycode = models.ForeignKey(Inquiry,on_delete=PROTECT, related_name= "fk_g1codeinquiry")
    kymahieuinq = models.CharField(max_length=100)
    unit = models.CharField(max_length = 20,choices = UNITS_CHOICES,default = 'pcs')
    qtyinq = models.FloatField()
    suppliercode = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fk_g1codesupplier")
    nsxinq = models.CharField(max_length=10)
    sttitb = models.IntegerField()
    groupitb = models.CharField(max_length=5)
    sales = models.CharField(max_length=10,choices= SALES_CHOICES,default="TuanLQ")
    dongiamuainq = models.FloatField()
    thanhtienmuainq = models.FloatField()
    dongiachaoinq = models.FloatField()
    thanhtienchaoinq = models.FloatField()
    markupinq = models.FloatField()
    resultinq = models.CharField(max_length=10, choices= RESULTS_CHOICES,default="Win", null= True, blank= True)
    lydowincode = models.ManyToManyField(lydowin, related_name='fk_g1codelydowin')
    lydooutcode = models.ManyToManyField(lydoout, related_name='fk_g1codelydoout')
    ngaywin = models.DateField(null=True, blank=True)
    ngayout = models.DateField(null=True, blank= True)
    ghichu = models.TextField(null=True,blank= True)
    gdvinq = models.ForeignKey(GDV, on_delete=PROTECT)
    dateupdate  = models.DateField()
    class Meta:
       unique_together = ("gcode", "inquirycode")
    def __str__(self):
        return self.g1code