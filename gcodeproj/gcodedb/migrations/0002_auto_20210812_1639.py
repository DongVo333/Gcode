# Generated by Django 3.2.4 on 2021-08-12 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcodedb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcode',
            name='kymahieuinq',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='gcode',
            name='markupdinhmuc',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
