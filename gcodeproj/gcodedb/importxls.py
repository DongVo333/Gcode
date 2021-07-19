from datetime import date, datetime
from re import split
from numpy import NaN, empty
from pandas.core.frame import DataFrame
import xlrd
from xlrd.formula import dump_formula
from .models import Contract, DanhgiaNSX, Danhgiacode, G1code, G2code, GDV,Gcode,Inquiry,Client,Kho,POdetail,Phat,Supplier,Lydowin,Lydoout,Giaohang,Sales, Tienve
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse
from django.utils.dateparse import parse_date
import pandas as pd
import numpy as np
import json
from django.utils.html import format_html

pd.options.display.float_format = '{:,.2f}'.format

def readdate(inputdate,workbook):
    if inputdate == "":
        return None
    else:
        return xlrd.xldate.xldate_as_datetime(inputdate,workbook.datemode).strftime("%Y-%m-%d")
def msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date):
    messages=[]
    if df.empty:
        messages.append("Data Import is empty! Please re-check again")
    elif not all([item in df.columns for item in list_column]): 
        for item in list_column:
            if not item in df.columns:
                message = format_html("Data Import doesn't has columns <b>{}</b>",item)
                messages.append(message)
    elif df[list_column_required].isna().sum().sum()>0:
        for i,j in zip(*np.where(pd.isnull(df[list_column_required]))):
            message = format_html("Data Import is empty at <b>index STT {}: column {}</b>",df.loc[i,'STT'],list_column_required[j])
            messages.append(message)
    elif len(list_column_float):
        if any(df[item].dtype == "object" for item in list_column_float):
            for item in list_column_float:
                for i1,i2 in zip(df['STT'],df[item].map(type)):
                    if i2==str:
                        message = format_html("Data Import is formated wrong at <b>index STT {}: column {}</b>",i1,item)
                        messages.append(message) 
    elif len(list_column_date):
        if any(df[item].dtype == "object" for item in list_column_date):
            for item in list_column_date:
                for i1,i2 in zip(df['STT'],df[item].map(type)):
                    if i2==date:
                        message = format_html("Data Import is formated wrong at <b>index STT {}: column {}</b>",i1,item)
                        messages.append(message)
    return messages

def importxls_client(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Client")
        for r in range(1, sheet.nrows):
            counter = Client.objects.filter(clientcode=sheet.cell(r,1).value).count()
            client = Client()
            if counter>0:
                client = Client.objects.get(clientcode=sheet.cell(r,1).value)
                client.fullname = sheet.cell(r,2).value
                client.save()
            else:
                client = Client(
        		    clientcode= sheet.cell(r,1).value,
                    fullname=sheet.cell(r,2).value,
        		    )
                client.save()  
        return redirect('/client/')     
    return render(request, 'gcodedb/client_list.html')

def importxls_gcode(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Gcode")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Gcode.objects.filter(ma=str(sheet.cell(r,1).value)).count()
            gcode = Gcode()
            if counter>0:
                gcode = Gcode.objects.get(ma=str(sheet.cell(r,1).value))
                gcode.mota = sheet.cell(r,2).value
                gcode.markupdinhmuc = float(sheet.cell(r,3).value)
                gcode.ngaywin = readdate(sheet.cell(r,4).value,workbook)
                gcode.ngayout = readdate(sheet.cell(r,5).value,workbook)
                gcode.save()
            else:
                gcode = Gcode(
        		    ma=sheet.cell(r,1).value,
        		    mota=sheet.cell(r,2).value,
                    markupdinhmuc=float(sheet.cell(r,3).value),
                    ngaywin = readdate(sheet.cell(r,4).value,workbook),
                    ngayout = readdate(sheet.cell(r,5).value,workbook),
        		    )
                gcode.save()  
        return redirect('/gcode/')     
    return render(request, 'gcodedb/gcode_list.html')

def importxls_contract(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Contract")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Contract.objects.filter(contractcode=str(sheet.cell(r,1).value)).count()
            contract = Contract()
            if counter>0:
                contract = Contract.objects.get(contractcode=str(sheet.cell(r,1).value))
                contract.contractnoclient = sheet.cell(r,2).value
                ngayky = xlrd.xldate.xldate_as_datetime(sheet.cell(r,3).value,workbook.datemode).strftime("%Y-%m-%d")
                contract.datesign = ngayky
                contract.client =Client.objects.get(clientcode=sheet.cell(r,4).value) 
                deadline1 = xlrd.xldate.xldate_as_datetime(sheet.cell(r,5).value,workbook.datemode).strftime("%Y-%m-%d")
                contract.dealine1 = deadline1
                deadline2 = xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d")
                contract.dealine2 = deadline2
                contract.sellcost = float(sheet.cell(r,7).value)
                contract.status = sheet.cell(r,8).value
                datedeliverylatest = xlrd.xldate.xldate_as_datetime(sheet.cell(r,9).value,workbook.datemode).strftime("%Y-%m-%d")
                contract.datedeliverylatest = datedeliverylatest
                contract.save()
            else:
                contract = Contract(
        		    contractcode=str(sheet.cell(r,1).value),
        		    contractnoclient=sheet.cell(r,2).value,
                    datesign=xlrd.xldate.xldate_as_datetime(sheet.cell(r,3).value,0).strftime("%Y-%m-%d"),
        		    client=Client.objects.get(clientcode=sheet.cell(r,4).value),
                    dealine1=xlrd.xldate.xldate_as_datetime(sheet.cell(r,5).value,0).strftime("%Y-%m-%d"),
                    dealine2=xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,0).strftime("%Y-%m-%d"),
                    sellcost=float(sheet.cell(r,7).value),
                    status=sheet.cell(r,8).value,
                    datedeliverylatest=xlrd.xldate.xldate_as_datetime(sheet.cell(r,9).value,0).strftime("%Y-%m-%d"),
        		    )
                contract.save()
        return redirect('/contract/')     
    return render(request, 'gcodedb/contract_list.html')

def importxls_inquiry(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Inquiry")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Inquiry.objects.filter(inquirycode=str(sheet.cell(r,1).value)).count()
            inquiry = Inquiry()
            if counter>0:
                inquiry = Inquiry.objects.get(inquirycode=str(sheet.cell(r,1).value))
                inquiry.datesubmitbid = xlrd.xldate.xldate_as_datetime(sheet.cell(r,2).value,workbook.datemode).strftime("%Y-%m-%d")
                inquiry.client = Client.objects.get(clientcode=sheet.cell(r,3).value)
                inquiry.save()
            else:
                inquiry = Inquiry(
        		    inquirycode=str(sheet.cell(r,1).value),
        		    datesubmitbid=xlrd.xldate.xldate_as_datetime(sheet.cell(r,2).value,workbook.datemode).strftime("%Y-%m-%d"),
                    client=Client.objects.get(clientcode=sheet.cell(r,3).value),
        		    )
                inquiry.save()  
        return redirect('/inquiry/')     
    return render(request, 'gcodedb/inquiry_list.html')

def importxls_gdv(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("GDV")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = GDV.objects.filter(gdvcode=str(sheet.cell(r,1).value)).count()
            gdv = GDV()
            if counter>0:
                gdv = GDV.objects.get(gdvcode=str(sheet.cell(r,1).value))
                gdv.fullname = sheet.cell(r,2).value
                gdv.save()
            else:
                gdv = GDV(
        		    gdvcode = sheet.cell(r,1).value,
        		    fullname = sheet.cell(r,2).value,
        		    )
                gdv.save()  
        return redirect('/gdv/')     
    return render(request, 'gcodedb/gdv_list.html')

def importxls_supplier(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Supplier")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Supplier.objects.filter(suppliercode=str(sheet.cell(r,1).value)).count()
            supplier = Supplier()
            if counter>0:
                supplier = Supplier.objects.get(suppliercode=str(sheet.cell(r,1).value))
                supplier.fullname = sheet.cell(r,2).value
                supplier.duyetpomax = sheet.cell(r,3).value
                supplier.save()
            else:
                supplier = Supplier(
        		    suppliercode = sheet.cell(r,1).value,
        		    fullname=sheet.cell(r,2).value,
                    duyetpomax=sheet.cell(r,3).value,
        		    )
                supplier.save()  
        return redirect('/supplier/')     
    return render(request, 'gcodedb/supplier_list.html')

def importxls_lydowin(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Lydowin")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Lydowin.objects.filter(lydowincode=str(sheet.cell(r,1).value)).count()
            lydowin = Lydowin()
            if counter>0:
                lydowin = Lydowin.objects.get(lydowincode=str(sheet.cell(r,1).value))
                lydowin.detail = sheet.cell(r,2).value
                lydowin.save()
            else:
                lydowin = Lydowin(
        		    lydowincode=sheet.cell(r,1).value,
        		    detail=sheet.cell(r,2).value,
        		    )
                lydowin.save()  
        return redirect('/lydowin/')     
    return render(request, 'gcodedb/lydowin_list.html')

def importxls_lydoout(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Lydoout")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Lydoout.objects.filter(lydooutcode=str(sheet.cell(r,1).value)).count()
            lydoout = Lydoout()
            if counter>0:
                lydoout = Lydoout.objects.get(lydooutcode=str(sheet.cell(r,1).value))
                lydoout.detail = sheet.cell(r,2).value
                lydoout.save()
            else:
                lydoout = Lydoout(
        		    lydooutcode=sheet.cell(r,1).value,
        		    detail=sheet.cell(r,2).value,
        		    )
                lydoout.save()  
        return redirect('/lydoout/')     
    return render(request, 'gcodedb/lydoout_list.html')

def importxls_danhgiacode(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Đánh giá code")
        norow = sheet.nrows
        for r in range(1, norow):
            strdanhgiacode = sheet.cell(r,1).value.strip()
            counter = Danhgiacode.objects.filter(danhgiacode=strdanhgiacode).count()
            danhgiacode_ = Danhgiacode()
            if counter<=0:
                danhgiacode_ = Danhgiacode(
        		    danhgiacode=sheet.cell(r,1).value,
        		    )
                danhgiacode_.save()  
        return redirect('/danhgiacode/')     
    return render(request, 'gcodedb/danhgiacode_list.html')

def importxls_kho(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Kho")
        norow = sheet.nrows
        for r in range(1, norow):
            g2code_ = G2code.objects.get(g2code=sheet.cell(r,1).value)
            counter = Kho.objects.filter(g2code=g2code_).count()
            g2codekho = Kho()
            if counter>0:
                g2codekho = Kho.objects.get(g2code=g2code_)
                g2codekho.qtykho = sheet.cell(r,2).value
                g2codekho.dongiafreight = sheet.cell(r,3).value
                g2codekho.ngaynhapkho = xlrd.xldate.xldate_as_datetime(sheet.cell(r,4).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codekho.gdvkho = GDV.objects.get(gdvcode=sheet.cell(r,5).value)
                g2codekho.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codekho.save()
            else:
                g2codekho = Kho(
        		    g2code = g2code_,
        		    qtykho=sheet.cell(r,2).value,
                    dongiafreight=sheet.cell(r,3).value,
                    ngaynhapkho=xlrd.xldate.xldate_as_datetime(sheet.cell(r,4).value,workbook.datemode).strftime("%Y-%m-%d"),
                    gdvkho=GDV.objects.get(gdvcode=sheet.cell(r,5).value),
                    dateupdate=xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codekho.save()  
        return redirect('/kho/')     
    return render(request, 'gcodedb/kho_list.html')

def importxls_offer_(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Offer")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = G1code.objects.filter(g1code=sheet.cell(r,1).value).count()
            g1code = G1code()
            if counter>0:
                g1code = G1code.objects.get(g1code=sheet.cell(r,1).value)
                g1code.gcode = Gcode.objects.get(ma=str(sheet.cell(r,2).value))
                g1code.inquiry = Inquiry.objects.get(inquirycode=sheet.cell(r,3).value)
                g1code.kymahieuinq = sheet.cell(r,4).value
                g1code.unitinq = sheet.cell(r,5).value
                g1code.qtyinq = sheet.cell(r,6).value
                g1code.supplier = Supplier.objects.get(suppliercode=sheet.cell(r,7).value)
                g1code.xuatxuinq = sheet.cell(r,8).value
                g1code.nsxinq = sheet.cell(r,9).value
                g1code.sttitb = sheet.cell(r,10).value
                g1code.groupitb = sheet.cell(r,11).value
                g1code.sales = Sales.objects.get(salescode=sheet.cell(r,12).value)
                g1code.dongiamuainq = sheet.cell(r,13).value
                g1code.dongiachaoinq = sheet.cell(r,14).value
                g1code.markupinq = float('{:.2f}'.format(sheet.cell(r,15).value))
                g1code.resultinq = sheet.cell(r,16).value
                strlydowin = sheet.cell(r,17).value.split(",")
                for item in strlydowin:
                    itemstrip = item.strip()
                    if Lydowin.objects.filter(lydowincode=itemstrip).count() > 0:
                        lydowin_ = Lydowin.objects.get(lydowincode=itemstrip)
                        g1code.lydowin.add(lydowin_)
                strlydoout = sheet.cell(r,18).value.split(",")
                for item in strlydoout:
                    itemstrip = item.strip()
                    if Lydoout.objects.filter(lydooutcode=itemstrip).count() > 0:
                        lydoout_ = Lydoout.objects.get(lydooutcode=itemstrip)
                        g1code.lydoout.add(lydoout_)
                g1code.ghichu = sheet.cell(r,19).value
                g1code.gdvinq = GDV.objects.get(gdvcode = sheet.cell(r,20).value)
                g1code.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,21).value,workbook.datemode).strftime("%Y-%m-%d")

                g1code.save()
            else:
                g1code = G1code(
                    g1code=sheet.cell(r,1).value,
                    gcode = Gcode.objects.get(ma=str(sheet.cell(r,2).value)),
                    inquiry = Inquiry.objects.get(inquirycode=sheet.cell(r,3).value),
                    kymahieuinq = sheet.cell(r,4).value,
                    unitinq = sheet.cell(r,5).value,
                    qtyinq = sheet.cell(r,6).value,
                    supplier = Supplier.objects.get(suppliercode=sheet.cell(r,7).value),
                    xuatxuinq = sheet.cell(r,8).value,
                    nsxinq = sheet.cell(r,9).value,
                    sttitb = sheet.cell(r,10).value,
                    groupitb = sheet.cell(r,11).value,
                    sales = Sales.objects.get(salescode=sheet.cell(r,12).value),
                    dongiamuainq = sheet.cell(r,13).value,
                    dongiachaoinq = sheet.cell(r,14).value,
                    markupinq = float('{:.2f}'.format(sheet.cell(r,15).value)),
                    resultinq = sheet.cell(r,16).value,
                    ghichu = sheet.cell(r,19).value,
                    gdvinq = GDV.objects.get(gdvcode = sheet.cell(r,20).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,21).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g1code.save()  
                strlydowin = sheet.cell(r,17).value.split(",")
                for item in strlydowin:
                    itemstrip = item.strip()
                    if Lydowin.objects.filter(lydowincode=itemstrip).count()>0:
                        lydowin_ = Lydowin.objects.get(lydowincode=itemstrip)
                        g1code.lydowin.add(lydowin_)
                strlydoout = sheet.cell(r,18).value.split(",")
                for item in strlydoout:
                    itemstrip = item.strip()
                    if Lydoout.objects.filter(lydooutcode=itemstrip).count()>0:
                        lydoout_ = Lydoout.objects.get(lydooutcode=itemstrip)
                        g1code.lydoout.add(lydoout_)
        return redirect('/offer/')     
    return render(request, 'gcodedb/offer_list.html')

def importxls_offer_1(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        df = pd.read_excel(new_persons, sheet_name='Offer')
        print(list(df.columns))
        norow = df.shape[0] 
        for r in range(0, norow):
            counter = G1code.objects.filter(g1code=df.loc[r,'Gcode-Inquiry']).count()
            g1code = G1code()
            if counter>0:
                g1code = G1code.objects.get(g1code=df.loc[r,'Gcode-Inquiry'])
                g1code.gcode = Gcode.objects.get(ma=df.loc[r,'Gcode'])
                g1code.inquiry = Inquiry.objects.get(inquirycode=df.loc[r,'Inquiry'])
                g1code.kymahieuinq = df.loc[r,'Ký mã hiệu']
                g1code.unitinq = df.loc[r,'Đơn vị']
                g1code.qtyinq = df.loc[r,'Số lượng']
                g1code.supplier = Supplier.objects.get(suppliercode=df.loc[r,'Supplier'])
                g1code.xuatxuinq = df.loc[r,'Xuất xứ']
                g1code.nsxinq = df.loc[r,'NSX']
                g1code.sttitb = df.loc[r,'STT in ITB']
                g1code.groupitb = df.loc[r,'Group in ITB']
                g1code.sales = Sales.objects.get(salescode=df.loc[r,'Sale'])
                g1code.dongiamuainq = df.loc[r,'Đơn giá mua']
                g1code.dongiachaoinq = df.loc[r,'Đơn giá chào']
                g1code.markupinq = float('{:.2f}'.format(df.loc[r,'Markup']))
                g1code.resultinq = df.loc[r,'Result']
                if df.loc[r,'Uy tín'] == 'Yes':
                        lydowin_ = Lydowin.objects.get(lydowincode='Uy tín')
                        g1code.lydowin.add(lydowin_)
                if df.loc[r,'Giá tốt'] == 'Yes':
                        lydowin_ = Lydowin.objects.get(lydowincode='Giá tốt')
                        g1code.lydowin.add(lydowin_)
                if df.loc[r,'Giá chào cao'] == 'Yes':
                        lydoout_ = Lydoout.objects.get(lydooutcode='Giá chào cao')
                        g1code.lydoout.add(lydoout_)
                if df.loc[r,'Không tìm được NCC'] == 'Yes':
                        lydoout_ = Lydoout.objects.get(lydooutcode='Không tìm được NCC')
                        g1code.lydoout.add(lydoout_)
                g1code.ghichu = df.loc[r,'Ghi Chú']
                g1code.gdvinq = GDV.objects.get(gdvcode = df.loc[r,'Giao dịch viên'])
                g1code.dateupdate = date.today()

                g1code.save()
            else:
                g1code = G1code(
                    g1code=df.loc[r,'Gcode-Inquiry'],
                    gcode = Gcode.objects.get(ma=df.loc[r,'Gcode']),
                    inquiry = Inquiry.objects.get(inquirycode=df.loc[r,'Inquiry']),
                    kymahieuinq = df.loc[r,'Ký mã hiệu'],
                    unitinq = df.loc[r,'Đơn vị'],
                    qtyinq = df.loc[r,'Số lượng'],
                    supplier = Supplier.objects.get(suppliercode=df.loc[r,'Supplier']),
                    xuatxuinq = df.loc[r,'Xuất xứ'],
                    nsxinq = df.loc[r,'NSX'],
                    sttitb = df.loc[r,'STT in ITB'],
                    groupitb = df.loc[r,'Group in ITB'],
                    sales = Sales.objects.get(salescode=df.loc[r,'Sale']),
                    dongiamuainq = df.loc[r,'Đơn giá mua'],
                    dongiachaoinq = df.loc[r,'Đơn giá chào'],
                    markupinq = float('{:.2f}'.format(df.loc[r,'Markup'])),
                    resultinq = df.loc[r,'Result'],
                    ghichu = df.loc[r,'Ghi Chú'],
                    gdvinq = GDV.objects.get(gdvcode = df.loc[r,'Giao dịch viên']),
                    dateupdate = date.today(),
        		    )
                g1code.save()  
                if df.loc[r,'Uy tín'] == 'Yes':
                        lydowin_ = Lydowin.objects.get(lydowincode='Uy tín')
                        g1code.lydowin.add(lydowin_)
                if df.loc[r,'Giá tốt'] == 'Yes':
                        lydowin_ = Lydowin.objects.get(lydowincode='Giá tốt')
                        g1code.lydowin.add(lydowin_)
                if df.loc[r,'Giá chào cao'] == 'Yes':
                        lydoout_ = Lydoout.objects.get(lydooutcode='Giá chào cao')
                        g1code.lydoout.add(lydoout_)
                if df.loc[r,'Không tìm được NCC'] == 'Yes':
                        lydoout_ = Lydoout.objects.get(lydooutcode='Không tìm được NCC')
                        g1code.lydoout.add(lydoout_)
        return redirect('/offer/')     
    return render(request, 'gcodedb/offer_list.html')

def importxls_offer(request):
    messages=  []
    df = pd.read_excel(r'C:\Users\IDMD\Desktop\Tổng hợp_1.xls', sheet_name='Offer1')
    list_column = ['Gcode', 'Inquiry', 'Ký mã hiệu', 'Đơn vị',
       'Số lượng', 'Supplier', 'Xuất xứ', 'NSX', 'STT in ITB', 'Group in ITB',
       'Sale', 'Đơn giá mua', 'Đơn giá chào', 'Giao dịch viên', 'Ghi Chú', 'Result', 'Uy tín', 'Giá tốt',
       'Giá chào cao', 'Không tìm được NCC']
    list_column_required = ['Gcode', 'Inquiry', 'Ký mã hiệu', 'Đơn vị',
       'Số lượng', 'Supplier', 'Xuất xứ', 'NSX', 'STT in ITB', 'Group in ITB',
       'Sale', 'Đơn giá mua', 'Đơn giá chào', 'Giao dịch viên', 'Result']
    list_column_float = ["Đơn giá chào","Đơn giá mua","Số lượng"]
    list_column_date = []
    messages.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
    if len(messages) <=0:
        duplicateRowsDF = df[df.duplicated(subset=['Gcode','Inquiry'],keep=False)]
        if duplicateRowsDF.shape[0]:
            message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
            messages.append(message)
        else:
            for index,row in df.iterrows():
                if G1code.objects.filter(gcode__ma__icontains=row['Gcode'],inquiry__inquirycode__icontains=row['Inquiry']).count()>0:
                    message = format_html("Gcode-Inquiry '{}-{}' is existed at <b>index STT {}</b>",row['Gcode'],row['Inquiry'],row['STT'])
                    messages.append(message)
                if Gcode.objects.filter(ma=row['Gcode']).count()<=0:
                    Url_gcode = "gcodedb:gcode_list"
                    Href_gcode = "\{% url '{0}' %\}".format(Url_gcode)
                    message = format_html("Gcode '{}' doesn't exist at <b>index STT {}</b>, you shall be import Gcode before importing again at link: <a href='{href_gcode}'>Create Gcode</a>".format(href_gcode=Href_gcode),row['Gcode'],row['STT'])
                    messages.append(message)
                if Inquiry.objects.filter(inquirycode=row['Inquiry']).count()<=0:
                    message = format_html("Inquiry '{}' doesn't exist at <b>index STT {}</b>, you should be import Inquiry before importing again at link: <a href=''>Create Inquiry</a>",row['Inquiry'],row['STT'])
                    messages.append(message)
                if GDV.objects.filter(gdvcode=row['Giao dịch viên']).count()<=0:
                    message = format_html("Seller '{}' doesn't exist at <b>index STT {}</b>, you should be import Seller before importing again at link: <a href=''>Create Seller</a>",row['Giao dịch viên'],row['STT'])
                    messages.append(message)
    if len(messages) <=0:
        df[list_column_float]= df[list_column_float].astype('float64')
        df_obj = df.select_dtypes(['object'])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        #df[['Số lượng','Đơn giá mua','Đơn giá chào','Markup']] = df[['Số lượng','Đơn giá mua','Đơn giá chào','Markup']].round(decimals=2)
        """ df=df1.style.format({'value':'{:.2f}'}) """
        df['Thành tiền mua'] = df['Số lượng']*df['Đơn giá mua']
        df['Thành tiền chào'] = df['Số lượng']*df['Đơn giá chào']
        df['Markup'] = df['Đơn giá chào']/df['Đơn giá mua']
        for i in range(0,df.shape[0]):
            df.loc[i,'Gcode-Inquiry'] = str(df.loc[i,'Gcode']) + '-' + df.loc[i,'Inquiry']
        #Check dữ liệu trống
        #Check dữ liệu định dạng chưa đúng 
        #Check bổ sung dữ liệu
        #Check markup vượt quá định mức
    html = df.to_html(index=False,justify='center')
    context = {'offer_list': html,'messages':messages}
    return render(request, 'gcodedb/offer_list.html', context)

def importxls_hdb(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Gcode-Contract")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = G2code.objects.filter(g2code=sheet.cell(r,1).value).count()
            g2code = G2code()
            if counter>0:
                g2code = G2code.objects.get(g2code=sheet.cell(r,1).value)
                g2code.contract = Contract.objects.get(contractcode=sheet.cell(r,2).value)
                g2code.dongiachaohdb = sheet.cell(r,3).value
                g2code.pono = sheet.cell(r,4).value
                g2code.status = sheet.cell(r,5).value
                g2code.g1code = G1code.objects.get(g1code=sheet.cell(r,6).value)
                g2code.ghichu = sheet.cell(r,7).value
                g2code.gdvhdb = GDV.objects.get(gdvcode=sheet.cell(r,8).value)
                g2code.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,9).value,workbook.datemode).strftime("%Y-%m-%d")
                g2code.save()
            else:
                g2codekho = G2code(
        		    g2code = sheet.cell(r,1).value,
                    contract = Contract.objects.get(contractcode=sheet.cell(r,2).value),
                    dongiachaohdb = sheet.cell(r,3).value,
                    pono = sheet.cell(r,4).value,
                    status = sheet.cell(r,5).value,
                    g1code = G1code.objects.get(g1code=sheet.cell(r,6).value),
                    ghichu = sheet.cell(r,7).value,
                    gdvhdb = GDV.objects.get(gdvcode=sheet.cell(r,8).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,9).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codekho.save()  
        return redirect('/hdb/')     
    return render(request, 'gcodedb/hdb_list.html')

def importxls_po(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Purchase Order")
        norow = sheet.nrows
        for r in range(1, norow):
            g2code_ = G2code.objects.get(g2code=sheet.cell(r,1).value)
            counter = POdetail.objects.filter(g2code=g2code_).count()
            g2codepo = POdetail()
            if counter>0:
                g2codepo = POdetail.objects.get(g2code=g2code_)
                g2codepo.motapo = sheet.cell(r,2).value
                g2codepo.kymahieupo = sheet.cell(r,3).value
                g2codepo.unitpo = sheet.cell(r,4).value
                g2codepo.qtypo = sheet.cell(r,5).value
                g2codepo.supplier = Supplier.objects.get(suppliercode=sheet.cell(r,6).value) 
                g2codepo.xuatxupo = sheet.cell(r,7).value
                g2codepo.nsxpo = sheet.cell(r,8).value
                g2codepo.dongiamuapo = sheet.cell(r,9).value
                g2codepo.ghichu = sheet.cell(r,10).value
                g2codepo.gdvpo = GDV.objects.get(gdvcode=sheet.cell(r,11).value)
                g2codepo.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,12).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codepo.save()
            else:
                g2codepo = POdetail(
        		    g2code = g2code_,
        		    motapo = sheet.cell(r,2).value,
                    kymahieupo = sheet.cell(r,3).value,
                    unitpo = sheet.cell(r,4).value,
                    qtypo = sheet.cell(r,5).value,
                    supplier = Supplier.objects.get(suppliercode=sheet.cell(r,6).value), 
                    xuatxupo = sheet.cell(r,7).value,
                    nsxpo = sheet.cell(r,8).value,
                    dongiamuapo = sheet.cell(r,9).value,
                    ghichu = sheet.cell(r,10).value,
                    gdvpo = GDV.objects.get(gdvcode=sheet.cell(r,11).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,12).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codepo.save()  
        return redirect('/po/')     
    return render(request, 'gcodedb/po_list.html')

def importxls_giaohang(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Giao hàng")
        norow = sheet.nrows
        for r in range(1, norow):
            g2code_ = G2code.objects.get(g2code=sheet.cell(r,1).value)
            counter = Giaohang.objects.filter(g2code=g2code_).count()
            g2codegh = Giaohang()
            if counter>0:
                g2codegh = Giaohang.objects.get(g2code=g2code_)
                g2codegh.qtygiaohang = sheet.cell(r,2).value
                g2codegh.ngaygiaohang = xlrd.xldate.xldate_as_datetime(sheet.cell(r,3).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codegh.gdvgiaohang = GDV.objects.get(gdvcode=sheet.cell(r,4).value)
                g2codegh.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,5).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codegh.save()
            else:
                g2codegh = Giaohang(
        		    g2code = g2code_,
                    qtygiaohang = sheet.cell(r,2).value,
                    ngaygiaohang = xlrd.xldate.xldate_as_datetime(sheet.cell(r,3).value,workbook.datemode).strftime("%Y-%m-%d"),
                    gdvgiaohang = GDV.objects.get(gdvcode=sheet.cell(r,4).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,5).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codegh.save()  
        return redirect('/giaohang/')     
    return render(request, 'gcodedb/giaohang_list.html')

def importxls_phat(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Phạt")
        norow = sheet.nrows
        for r in range(1, norow):
            g2code_ = G2code.objects.get(g2code=sheet.cell(r,1).value)
            counter = Phat.objects.filter(g2code=g2code_).count()
            g2codephat = Phat()
            if counter>0:
                g2codephat = Phat.objects.get(g2code=g2code_)
                g2codephat.qtyphat = sheet.cell(r,2).value
                g2codephat.tongphat = sheet.cell(r,3).value
                g2codephat.lydophat = sheet.cell(r,4).value
                g2codephat.gdvphat = GDV.objects.get(gdvcode=sheet.cell(r,5).value)
                g2codephat.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codephat.save()
            else:
                g2codephat = Phat(
        		    g2code = g2code_,
                    qtyphat = sheet.cell(r,2).value,
                    tongphat = sheet.cell(r,3).value,
                    lydophat = sheet.cell(r,4).value,
                    gdvphat = GDV.objects.get(gdvcode=sheet.cell(r,5).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codephat.save()  
        return redirect('/phat/')     
    return render(request, 'gcodedb/phat_list.html')

def importxls_danhgiansx(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Đánh giá NSX")
        norow = sheet.nrows
        for r in range(1, norow):
            g2code_ = G2code.objects.get(g2code=sheet.cell(r,1).value)
            counter = DanhgiaNSX.objects.filter(g2code=g2code_).count()
            g2codedg = DanhgiaNSX()
            if counter>0:
                g2codedg = DanhgiaNSX.objects.get(g2code=g2code_)
                strdanhgia = sheet.cell(r,2).value.split(",")
                for item in strdanhgia:
                    itemstrip = item.strip()
                    if Danhgiacode.objects.filter(danhgiacode=itemstrip).count()>0:
                        danhgia_ = Danhgiacode.objects.get(danhgiacode=itemstrip)
                        g2codedg.danhgiacode.add(danhgia_)
                g2codedg.comment = sheet.cell(r,3).value
                g2codedg.gdvdanhgia = GDV.objects.get(gdvcode=sheet.cell(r,4).value)
                g2codedg.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,5).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codedg.save()
            else:
                g2codedg = DanhgiaNSX(
        		    g2code = g2code_,
                    comment = sheet.cell(r,3).value,
                    gdvdanhgia = GDV.objects.get(gdvcode=sheet.cell(r,4).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,5).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codedg.save() 
                strdanhgia = sheet.cell(r,2).value.split(",")
                for item in strdanhgia:
                    itemstrip = item.strip()
                    if Danhgiacode.objects.filter(danhgiacode=itemstrip).count()>0:
                        danhgia_ = Danhgiacode.objects.get(danhgiacode=itemstrip)
                        g2codedg.danhgiacode.add(danhgia_)
        return redirect('/danhgia/')     
    return render(request, 'gcodedb/danhgia_list.html')

def importxls_tienve(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Tiền về")
        norow = sheet.nrows
        for r in range(1, norow):
            g2code_ = G2code.objects.get(g2code=sheet.cell(r,1).value)
            counter = Tienve.objects.filter(g2code=g2code_).count()
            g2codetienve = Tienve()
            if counter>0:
                g2codetienve = Tienve.objects.get(g2code=g2code_)
                g2codetienve.qtytienve = sheet.cell(r,2).value
                g2codetienve.dongiatienve = sheet.cell(r,3).value
                g2codetienve.save()
            else:
                g2codetienve = Tienve(
        		    g2code = g2code_,
                    qtytienve = sheet.cell(r,2).value,
                    dongiatienve = sheet.cell(r,3).value,
        		    )
                g2codetienve.save()  
        return redirect('/tienve/')     
    return render(request, 'gcodedb/tienve_list.html')

def importxls_sales(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Sales")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Sales.objects.filter(salescode=sheet.cell(r,1).value).count()
            sales = Sales()
            if counter>0:
                sales = Sales.objects.get(salescode=sheet.cell(r,1).value)
                sales.fullname = sheet.cell(r,2).value
                sales.save()
            else:
                sales = Sales(
        		    salescode = sheet.cell(r,1).value,
                    fullname = sheet.cell(r,2).value,
        		    )
                sales.save()  
        return redirect('/sales/')     
    return render(request, 'gcodedb/sales_list.html')