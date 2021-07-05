from datetime import date
import xlrd
from .models import Contract, G1code, G2code, GDV, Gcode,Inquiry,Client, Kho,Supplier,Lydowin,Lydoout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse


def importxls_client(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Client")
        for r in range(1, sheet.nrows):
            counter = Client.objects.filter(clientcode=sheet.cell(r,0).value).count()
            client = Client()
            if counter>0:
                client = Client.objects.get(clientcode=sheet.cell(r,0).value)
                client.fullname = sheet.cell(r,1).value
                client.save()
            else:
                client = Client(
        		    sheet.cell(r,0).value,
        		    sheet.cell(r,1).value,
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
            counter = Gcode.objects.filter(ma=str(sheet.cell(r,0).value)).count()
            gcode = Gcode()
            if counter>0:
                gcode = Gcode.objects.get(ma=str(sheet.cell(r,0).value))
                gcode.mota = sheet.cell(r,1).value
                gcode.markupdinhmuc = float(sheet.cell(r,2).value)
                gcode.save()
            else:
                gcode = Gcode(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
                    float(sheet.cell(r,2).value),
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
            counter = Contract.objects.filter(contractcode=str(sheet.cell(r,0).value)).count()
            contract = Contract()
            if counter>0:
                contract = Contract.objects.get(contractcode=str(sheet.cell(r,0).value))
                contract.contractnoclient = sheet.cell(r,1).value
                contract.datesign = sheet.cell(r,2).value
                contract.clientcode = sheet.cell(r,3).value
                contract.dealine1 = sheet.cell(r,4).value
                contract.dealine2 = sheet.cell(r,5).value
                contract.sellcost = float(sheet.cell(r,6).value)
                contract.status = sheet.cell(r,7).value
                contract.datedeliverylatest = sheet.cell(r,8).value
                contract.save()
            else:
                contract = Contract(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
                    sheet.cell(r,2).value,
        		    sheet.cell(r,3).value,
                    sheet.cell(r,4).value,
                    sheet.cell(r,5).value,
                    float(sheet.cell(r,6).value),
                    sheet.cell(r,7).value,
                    sheet.cell(r,8).value,
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
            counter = Inquiry.objects.filter(inquirycode=str(sheet.cell(r,0).value)).count()
            inquiry = Inquiry()
            if counter>0:
                inquiry = Inquiry.objects.get(inquirycode=str(sheet.cell(r,0).value))
                inquiry.datesubmitbid = sheet.cell(r,1).value
                inquiry.clientcode = Client.objects.get(clientcode=sheet.cell(r,2).value)
                print (Client.objects.get(clientcode=sheet.cell(r,2).value).clientcode)
                inquiry.save()
            else:
                inquiry = Inquiry(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
                    Client.objects.get(clientcode=sheet.cell(r,2).value),
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
            counter = GDV.objects.filter(gdvcode=str(sheet.cell(r,0).value)).count()
            gdv = GDV()
            if counter>0:
                gdv = GDV.objects.get(gdvcode=str(sheet.cell(r,0).value))
                gdv.fullname = sheet.cell(r,1).value
                gdv.save()
            else:
                gdv = GDV(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
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
            counter = Supplier.objects.filter(suppliercode=str(sheet.cell(r,0).value)).count()
            supplier = Supplier()
            if counter>0:
                supplier = Supplier.objects.get(suppliercode=str(sheet.cell(r,0).value))
                supplier.fullname = sheet.cell(r,1).value
                supplier.duyetpomax = sheet.cell(r,2).value
                supplier.save()
            else:
                supplier = Supplier(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
                    sheet.cell(r,2).value,
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
            counter = Lydowin.objects.filter(lydowincode=str(sheet.cell(r,0).value)).count()
            lydowin = Lydowin()
            if counter>0:
                lydowin = Lydowin.objects.get(lydowincode=str(sheet.cell(r,0).value))
                lydowin.detail = sheet.cell(r,1).value
                lydowin.save()
            else:
                lydowin = Lydowin(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
        		    )
                lydowin.save()  
        return redirect('/lydowin/')     
    return render(request, 'gcodedb/lydowin_list.html')

def importxls_lydoout(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Lydowin")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Lydowin.objects.filter(lydooutcode=str(sheet.cell(r,0).value)).count()
            lydoout = Lydowin()
            if counter>0:
                lydoout = Lydowin.objects.get(lydooutcode=str(sheet.cell(r,0).value))
                lydoout.detail = sheet.cell(r,1).value
                lydoout.save()
            else:
                lydoout = Lydowin(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
        		    )
                lydoout.save()  
        return redirect('/lydoout/')     
    return render(request, 'gcodedb/lydoout_list.html')

def importxls_kho(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Kho")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = Kho.objects.filter(g2code=str(sheet.cell(r,0).value)).count()
            g2codekho = Kho()
            if counter>0:
                g2codekho = Kho.objects.get(g2code=str(sheet.cell(r,0).value))
                g2codekho.detail = sheet.cell(r,1).value
                g2codekho.save()
            else:
                g2codekho = Lydowin(
        		    str(sheet.cell(r,0).value),
        		    sheet.cell(r,1).value,
        		    )
                g2codekho.save()  
        return redirect('/kho/')     
    return render(request, 'gcodedb/kho_list.html')