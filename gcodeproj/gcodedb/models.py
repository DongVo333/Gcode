from django.db import models
from django.forms import ModelForm

class Gcode(models.Model):
    ma = models.CharField(max_length=20)
    mota = models.TextField()
    xuatxu = models.TextField(max_length=100)
    markupdinhmuc = models.FloatField()
    class Meta:
        db_table = "gcodedb_gcode"