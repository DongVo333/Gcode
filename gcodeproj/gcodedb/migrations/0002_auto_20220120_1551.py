# Generated by Django 3.2.4 on 2022-01-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcodedb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='contractnoclient',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='datedeliverylatest',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='sellcost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]