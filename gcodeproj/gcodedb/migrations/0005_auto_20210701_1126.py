# Generated by Django 3.2.4 on 2021-07-01 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcodedb', '0004_rename_clientcode_client_clientcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='g1code',
            name='dateupdate',
            field=models.DateField(),
        ),
        migrations.AlterModelTable(
            name='client',
            table='gcodedb_client',
        ),
        migrations.AlterModelTable(
            name='inquiry',
            table='gcodedb_inquiry',
        ),
    ]
