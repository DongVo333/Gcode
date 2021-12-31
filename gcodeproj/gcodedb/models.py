from django.db import models
from django.db.models.base import ModelState
from django.db.models.deletion import PROTECT
from django.db.models.fields import IntegerField
from numpy import integer



RESULTS_CHOICES = (
    ("Win","Win"),
    ("Out","Out"),
)
STATUS_CHOICES =(
    ("Open","Open"),
    ("Close","Close"),
)

class Yearcode(models.Model):
    nowyear = models.IntegerField()
    yearcode = models.CharField(max_length=3)

class Currency (models.Model):
    Tenngoaite = models.CharField(max_length=50)
    Mangoaite = models.CharField(max_length=10)
    Tygia  = models.FloatField()
    dateupdate  = models.DateField()

class PAMHop(models.Model):
    pamhop = models.CharField(max_length=10)
    def __str__(self):
        return self.pamhop

class Tinhtrangiaiquyetkhokhan (models.Model):
    ttgqkk = models.CharField(max_length=50)
    def __str__(self):
        return self.ttgqkk
class Baocaogiaohang(models.Model):
    bcgh = models.CharField(max_length=100)
    def __str__(self):
        return self.bcgh

class Client(models.Model):
    clientcode = models.CharField(max_length=20)
    fullname = models.CharField(max_length=200)
    def __str__(self):
        return self.clientcode

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

class Sales(models.Model):
    salescode = models.CharField(max_length=20)
    fullname = models.CharField(max_length=70)
    def __str__(self):
        return self.salescode

class Unit(models.Model):
    unit = models.CharField(max_length=10)
    def __str__(self):
        return self.unit

class Contract (models.Model):
    contractcode  = models.CharField(max_length=50)
    contractnoclient = models.CharField(max_length=50)
    datesign  = models.DateField()
    client  = models.ForeignKey(Client,on_delete=PROTECT, related_name= "fk_contractclient")
    sales = models.ForeignKey(Sales,on_delete=PROTECT, related_name= "fk_contractsales")
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
class Danhgiagcode(models.Model):
    danhgiagcode=models.CharField(max_length=100)
    def __str__(self):
        return self.danhgiagcode 
class Gcode(models.Model):
    gcode = models.CharField(max_length=20)
    descriptionban = models.TextField()
    descriptionmua = models.TextField()
    PNban = models.CharField(max_length=100,null=True,blank=True)
    PNmua = models.CharField(max_length=100,null=True,blank=True)
    markupdinhmuc = models.FloatField(null=True,blank=True)
    ngaywin = models.DateField(null=True, blank=True)
    ngayout = models.DateField(null=True, blank= True)
    class Meta:
        db_table = "gcodedb_gcode"
    def __str__(self):
        return self.gcode
        
class G1code(models.Model):
    gcode = models.ForeignKey(Gcode, on_delete=PROTECT, related_name= "fk_g1codegcode")
    inquiry = models.ForeignKey(Inquiry,on_delete=PROTECT, related_name= "fk_g1codeinquiry")
    unitinq = models.CharField(max_length = 20,default = 'pcs')
    qtyinq = models.FloatField()
    supplier = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fk_g1codesupplier")
    xuatxuinq = models.CharField(max_length=100)
    nsxinq = models.CharField(max_length=50)
    sttitb = models.IntegerField()
    groupitb = models.CharField(max_length=5)
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
class Nhaplieuban(models.Model):
    gcodeban = models.CharField(max_length= 20, null=True)
    contractno = models.ForeignKey(Contract,on_delete=PROTECT, related_name='fk_nlbcontract',null=True)
    dongiachaohdb = models.FloatField(null=True)
    status = models.CharField(max_length=30,null=True)
    deadlinegh = models.DateField()
    descriptionban = models.TextField()
    MNFban = models.CharField(max_length=30,null=True)
    qtyban = models.FloatField()
    unitban = models.ForeignKey(Unit,on_delete=PROTECT, related_name='fk_nlbunit',null=True)
    gdvhdb = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_nlbgdv',null=True)
    dateupdate  = models.DateField()
    def __str__(self):
        return str(self.g2code)
    @property
    def thanhtienchaohdb(self):
        return (self.g1code.qtyban or 0)*(self.dongiachaohdb or 0)
            
class Nhaplieumua(models.Model):
    g2code = models.OneToOneField(Nhaplieuban,on_delete=PROTECT,related_name='fk_nlmnlb')
    pono = models.CharField(max_length=50,null= True)
    gdvpo = models.ForeignKey(GDV,on_delete=PROTECT, related_name='fk_pogdv',null=True)
    supplier = models.ForeignKey(Supplier,on_delete=PROTECT, related_name= "fk_nlmsupplier",null=True)
    datesignpo = models.DateField()
    deliveryterm = models.CharField(max_length=10, null =True)
    qhxk = models.CharField(max_length=10, null =True)
    deadlinegatvam = models.DateField()
    pamhvamts = models.ForeignKey(PAMHop,on_delete=PROTECT, related_name= "fk_nlmpamhop")
    nttd1 = models.DateField()
    stttd1 = models.FloatField()
    nttd2 = models.DateField()
    stttd2 = models.FloatField()
    nttdn = models.DateField()
    stttdn = models.FloatField()
    descriptionmua = models.TextField(null=True)
    MNFmua = models.CharField(max_length=50,null=True)
    origin = models.CharField(max_length=100,null=True)
    PNmua = models.CharField(max_length=100,null=True)
    unitmua =models.ForeignKey(Unit,on_delete=PROTECT, related_name='fk_nlmunit',null=True)
    qtymua = models.FloatField()
    currency = models.ForeignKey(Currency,on_delete=PROTECT, related_name='fk_nlmcurrency',null=True)
    unitprice = models.FloatField(null=True)
    thueVAT = models.FloatField()
    certificate = models.CharField(max_length=100,null = True)
    danhgiagcode = models.ForeignKey(Danhgiagcode,on_delete=PROTECT, related_name='fk_nlmunit',null=True)
    reasondelay = models.TextField(null=True,blank=True)
    ctrrkt = models.TextField(null=True,blank=True)
    vdkk = models.TextField(null=True,blank=True)
    ykcpal = models.TextField(null=True,blank=True)
    ykcsales = models.TextField(null=True, blank= True)
    ttgqkk = models.ForeignKey(Tinhtrangiaiquyetkhokhan,on_delete=PROTECT, related_name='fk_nlmttgqkk',null=True)
    datesignpoplan = models.DateField(null=True)
    budget = models.FloatField()
    dateupdate  = models.DateField()

class Nhaplieunhapkhau(models.Model):
    g2code = models.OneToOneField(Nhaplieuban,on_delete=PROTECT,related_name='fk_nlnknlb')
    nlhrkksupplier = models.DateField()	
    ntthcmtkvam = models.DateField()
    qtykho = models.FloatField(null=True)
    ttkh =models.CharField(max_length=100,null=True)	
    dgnk = models.FloatField(null=True)
    nghttckh = models.DateField(null=True)
    qtygh = models.FloatField()
    bcgh = models.ForeignKey(Baocaogiaohang,on_delete=PROTECT,related_name='fk_nlnkbcgh')
    ghichu = models.TextField(null=True,blank= True)
    gdvnlnk = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_nlnkgdv',null=True)
    dateupdate  = models.DateField()


class Phat(models.Model):
    g2code = models.OneToOneField(Nhaplieuban,on_delete=PROTECT,related_name='fk_phatg2code')
    qtyphat = models.FloatField(null=True)
    tongphat = models.FloatField(null=True)
    lydophat = models.TextField(null=True)
    ghichu = models.TextField(null=True,blank= True)
    gdvphat = models.ForeignKey(GDV,on_delete=PROTECT,related_name='fk_phatgdv',null=True)
    dateupdate  = models.DateField()

class Tienve(models.Model):
    g2code = models.OneToOneField(Nhaplieuban,on_delete=PROTECT,related_name='fk_tienveg2code')
    qtytienve = models.FloatField(null=True)
    dongiatienve = models.FloatField(null=True)
    ghichu = models.TextField(null=True,blank= True)

    @property
    def tongtienve(self):
        return (self.qtytienve or 0)*(self.dongiatienve or 0)
    
class ScanOrder(models.Model):
    gcode = models.ManyToManyField(Nhaplieuban,related_name='fk_scanordergcode',null=True)
