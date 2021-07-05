# Generated by Django 3.2.4 on 2021-07-05 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('clientcode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'gcodedb_client',
            },
        ),
        migrations.CreateModel(
            name='Danhgiacode',
            fields=[
                ('danhgiacode', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='G1code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kymahieuinq', models.CharField(max_length=100)),
                ('unit', models.CharField(choices=[('bộ', 'bộ'), ('gói', 'gói'), ('thùng', 'thùng'), ('m', 'm'), ('l', 'l'), ('g', 'g'), ('kg', 'kg'), ('pcs', 'pcs')], default='pcs', max_length=20)),
                ('qtyinq', models.FloatField()),
                ('xuatxuinq', models.CharField(max_length=100)),
                ('nsxinq', models.CharField(max_length=50)),
                ('sttitb', models.IntegerField()),
                ('groupitb', models.CharField(max_length=5)),
                ('sales', models.CharField(choices=[('TuanLQ', 'TuanLQ'), ('TuanNT', 'TuanNT'), ('TramNB', 'TramNB'), ('ThuyLH', 'ThuyLH'), ('HungTC', 'HungTC'), ('HungND', 'HungND')], default='TuanLQ', max_length=10)),
                ('dongiamuainq', models.FloatField()),
                ('thanhtienmuainq', models.FloatField()),
                ('dongiachaoinq', models.FloatField()),
                ('thanhtienchaoinq', models.FloatField()),
                ('markupinq', models.FloatField()),
                ('resultinq', models.CharField(blank=True, choices=[('Win', 'Win'), ('Out', 'Out')], default='Win', max_length=10, null=True)),
                ('ngaywin', models.DateField(blank=True, null=True)),
                ('ngayout', models.DateField(blank=True, null=True)),
                ('ghichu', models.TextField(blank=True, null=True)),
                ('dateupdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Gcode',
            fields=[
                ('ma', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('mota', models.TextField()),
                ('markupdinhmuc', models.FloatField()),
            ],
            options={
                'db_table': 'gcodedb_gcode',
            },
        ),
        migrations.CreateModel(
            name='GDV',
            fields=[
                ('gdvcode', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='lydoout',
            fields=[
                ('lydooutcode', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('detail', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='lydowin',
            fields=[
                ('lydowincode', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('detail', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('suppliercode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=200)),
                ('duyetpomax', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='G2code',
            fields=[
                ('dongiachaohdb', models.FloatField(null=True)),
                ('thanhtienchaohdb', models.FloatField(null=True)),
                ('pono', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=30, null=True)),
                ('g1code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fkg2code_g1code', serialize=False, to='gcodedb.g1code')),
                ('ghichu', models.TextField(blank=True, null=True)),
                ('dateupdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('inquirycode', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('datesubmitbid', models.DateField()),
                ('clientcode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_Inquiryclient', to='gcodedb.client')),
            ],
            options={
                'db_table': 'gcodedb_inquiry',
            },
        ),
        migrations.AddField(
            model_name='g1code',
            name='gcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_g1codegcode', to='gcodedb.gcode'),
        ),
        migrations.AddField(
            model_name='g1code',
            name='gdvinq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gcodedb.gdv'),
        ),
        migrations.AddField(
            model_name='g1code',
            name='inquirycode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_g1codeinquiry', to='gcodedb.inquiry'),
        ),
        migrations.AddField(
            model_name='g1code',
            name='lydooutcode',
            field=models.ManyToManyField(blank=True, null=True, related_name='fk_g1codelydoout', to='gcodedb.lydoout'),
        ),
        migrations.AddField(
            model_name='g1code',
            name='lydowincode',
            field=models.ManyToManyField(blank=True, null=True, related_name='fk_g1codelydowin', to='gcodedb.lydowin'),
        ),
        migrations.AddField(
            model_name='g1code',
            name='suppliercode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_g1codesupplier', to='gcodedb.supplier'),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contractcode', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('contractnoclient', models.CharField(max_length=50)),
                ('datesign', models.DateField()),
                ('dealine1', models.DateField()),
                ('dealine2', models.DateField()),
                ('sellcost', models.FloatField()),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Close', 'Close')], default='Open', max_length=5)),
                ('datedeliverylatest', models.DateField()),
                ('clientcode', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fk_Contractclient', to='gcodedb.client')),
            ],
        ),
        migrations.CreateModel(
            name='Tienve',
            fields=[
                ('g2code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fktienve_g2code', serialize=False, to='gcodedb.g2code')),
                ('qtytienve', models.FloatField(null=True)),
                ('dongiatienve', models.FloatField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='g2code',
            name='contractcode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkg2code_contract', to='gcodedb.contract'),
        ),
        migrations.AddField(
            model_name='g2code',
            name='gdvhdb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkg2code_gdv', to='gcodedb.gdv'),
        ),
        migrations.AlterUniqueTogether(
            name='g1code',
            unique_together={('gcode', 'inquirycode')},
        ),
        migrations.CreateModel(
            name='POdetail',
            fields=[
                ('g2code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fkpo_g2code', serialize=False, to='gcodedb.g2code')),
                ('motapo', models.TextField(null=True)),
                ('kymahieupo', models.CharField(max_length=100, null=True)),
                ('unitpo', models.CharField(choices=[('bộ', 'bộ'), ('gói', 'gói'), ('thùng', 'thùng'), ('m', 'm'), ('l', 'l'), ('g', 'g'), ('kg', 'kg'), ('pcs', 'pcs')], default='pcs', max_length=20, null=True)),
                ('qtypo', models.FloatField()),
                ('xuatxupo', models.CharField(max_length=100, null=True)),
                ('nsxpo', models.CharField(max_length=50, null=True)),
                ('dongiamuapo', models.FloatField(null=True)),
                ('thanhtienmuapo', models.FloatField(null=True)),
                ('ghichu', models.TextField(null=True)),
                ('dateupdate', models.DateField()),
                ('gdvpo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkpo_gdv', to='gcodedb.gdv')),
                ('suppliercodepo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkg2code_supplier', to='gcodedb.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Phat',
            fields=[
                ('g2code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fkphat_g2code', serialize=False, to='gcodedb.g2code')),
                ('qtyphat', models.FloatField(null=True)),
                ('tongphat', models.FloatField(null=True)),
                ('lydophat', models.TextField(null=True)),
                ('dateupdate', models.DateField()),
                ('gdvphat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkphat_gdv', to='gcodedb.gdv')),
            ],
        ),
        migrations.CreateModel(
            name='Kho',
            fields=[
                ('g2code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fkkho_g2code', serialize=False, to='gcodedb.g2code')),
                ('qtykho', models.FloatField(null=True)),
                ('dongiafreight', models.FloatField(null=True)),
                ('ngaynhapkho', models.DateField(null=True)),
                ('dateupdate', models.DateField()),
                ('gdvkho', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkkho_gdv', to='gcodedb.gdv')),
            ],
        ),
        migrations.CreateModel(
            name='Giaohang',
            fields=[
                ('g2code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fkgiaohang_g2code', serialize=False, to='gcodedb.g2code')),
                ('qtygiaohang', models.FloatField(null=True)),
                ('ngaygiaohang', models.DateField(null=True)),
                ('dateupdate', models.DateField()),
                ('gdvgiaohang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkgiaohang_gdv', to='gcodedb.gdv')),
            ],
        ),
        migrations.CreateModel(
            name='DanhgiaNSX',
            fields=[
                ('g2code', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='fkdanhgia_g2code', serialize=False, to='gcodedb.g2code')),
                ('comment', models.TextField(null=True)),
                ('dateupdate', models.DateField()),
                ('danhgiacode', models.ManyToManyField(null=True, related_name='fk_danhgiacode', to='gcodedb.Danhgiacode')),
                ('gdvdanhgia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fkdanhgia_gdv', to='gcodedb.gdv')),
            ],
        ),
    ]
