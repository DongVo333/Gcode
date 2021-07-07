from datetime import date, datetime
from re import split
import xlrd
from .models import Contract, DanhgiaNSX, Danhgiacode, G1code, G2code, GDV,Gcode,Inquiry,Client,Kho,POdetail,Phat,Supplier,Lydowin,Lydoout,Giaohang,Sales, Tienve
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse
from django.utils.dateparse import parse_date

def readdate(inputdate,workbook):
    if inputdate == "":
        return None
    else:
        return xlrd.xldate.xldate_as_datetime(inputdate,workbook.datemode).strftime("%Y-%m-%d")
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
                g2codekho.gdvkho = GDV.objects.get(clientcode=sheet.cell(r,5).value)
                g2codekho.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d")
                g2codekho.save()
            else:
                g2codekho = Kho(
        		    g2code = g2code_,
        		    qtykho=sheet.cell(r,2).value,
                    dongiafreight=sheet.cell(r,3).value,
                    ngaynhapkho=xlrd.xldate.xldate_as_datetime(sheet.cell(r,4).value,workbook.datemode).strftime("%Y-%m-%d"),
                    gdvkho=GDV.objects.get(clientcode=sheet.cell(r,5).value),
                    dateupdate=xlrd.xldate.xldate_as_datetime(sheet.cell(r,6).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g2codekho.save()  
        return redirect('/kho/')     
    return render(request, 'gcodedb/kho_list.html')

def importxls_offer(request):
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
                g1code.gcode = Gcode.objects.get(gcode=sheet.cell(r,2).value)
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
                g1code.markupinq = sheet.cell(r,15).value
                g1code.resultinq = sheet.cell(r,16).value
                strlydowin = split(sheet.cell(r,17).value,",")
                for item in strlydowin:
                    itemstrip = item.strip()
                    if Lydowin.objects.filter(lydowincode=itemstrip).count<=0:
                        lydowin = Lydowin(lydowincode = itemstrip, detail = 'Null')
                        lydowin.save()
                    lydowin_ = Lydowin.objects.get(lydowincode=itemstrip)
                    g1code.lydowin.add(lydowin_)
                strlydoout = split(sheet.cell(r,18).value,",")
                for item in strlydoout:
                    itemstrip = item.strip()
                    if Lydoout.objects.filter(lydooutcode=itemstrip).count<=0:
                        lydoout = Lydoout(lydooutcode = itemstrip, detail = 'Null')
                        lydoout.save()
                    lydoout_ = Lydoout.objects.get(lydooutcode=itemstrip)
                    g1code.lydoout.add(lydoout_)
                g1code.ghichu = sheet.cell(r,19).value
                g1code.gdvinq = GDV.objects.get(gdvcode = sheet.cell(r,20).value)
                g1code.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,21).value,workbook.datemode).strftime("%Y-%m-%d")

                g1code.save()
            else:
                g1code = G1code(
                    g1code=sheet.cell(r,1).value,
                    gcode = Gcode.objects.get(gcode=sheet.cell(r,2).value),
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
                    markupinq = sheet.cell(r,15).value,
                    resultinq = sheet.cell(r,16).value,
                    ghichu = sheet.cell(r,19).value,
                    gdvinq = GDV.objects.get(gdvcode = sheet.cell(r,20).value),
                    dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,21).value,workbook.datemode).strftime("%Y-%m-%d"),
        		    )
                g1code.save()  
                for item in strlydowin:
                    itemstrip = item.strip()
                    if Lydowin.objects.filter(lydowincode=itemstrip).count<=0:
                        lydowin = Lydowin(lydowincode = itemstrip, detail = 'Null')
                        lydowin.save()
                    lydowin_ = Lydowin.objects.get(lydowincode=itemstrip)
                    g1code.lydowin.add(lydowin_)
                strlydoout = split(sheet.cell(r,18).value,",")
                for item in strlydoout:
                    itemstrip = item.strip()
                    if Lydoout.objects.filter(lydooutcode=itemstrip).count<=0:
                        lydoout = Lydoout(lydooutcode = itemstrip, detail = 'Null')
                        lydoout.save()
                    lydoout_ = Lydoout.objects.get(lydooutcode=itemstrip)
                    g1code.lydoout.add(lydoout_)
        return redirect('/offer/')     
    return render(request, 'gcodedb/offer_list.html')

def importxls_hdb(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        workbook = xlrd.open_workbook(file_contents=new_persons.read())
        sheet = workbook.sheet_by_name("Gcode-Contract")
        norow = sheet.nrows
        for r in range(1, norow):
            counter = G2code.objects.filter(g2code=sheet.cell(r,1).value).count
            g2code = G2code()
            if counter>0:
                g2code = G2code.objects.get(g2code=sheet.cell(r,1).value)
                g2code.contract = Contract.object.get(contractcode=sheet.cell(r,2).value)
                g2code.dongiachaohdb = sheet.cell(r,3).value
                g2code.pono = sheet.cell(r,4).value
                g2code.status = sheet.cell(r,5).value
                g2code.g1code = G1code.objects.get(g1code=sheet.cell(r,6).value)
                g2code.ghichu = sheet.cell(r,7).value
                g2code.gdvhdb = GDV.objects.get(clientcode=sheet.cell(r,8).value)
                g2code.dateupdate = xlrd.xldate.xldate_as_datetime(sheet.cell(r,9).value,workbook.datemode).strftime("%Y-%m-%d")
                g2code.save()
            else:
                g2codekho = G2code(
        		    g2code = sheet.cell(r,1).value,
                    contract = Contract.object.get(contractcode=sheet.cell(r,2).value),
                    dongiachaohdb = sheet.cell(r,3).value,
                    pono = sheet.cell(r,4).value,
                    status = sheet.cell(r,5).value,
                    g1code = G1code.objects.get(g1code=sheet.cell(r,6).value),
                    ghichu = sheet.cell(r,7).value,
                    gdvhdb = GDV.objects.get(clientcode=sheet.cell(r,8).value),
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
                strdanhgia = split(sheet.cell(r,2).value,",")
                for item in strdanhgia:
                    itemstrip = item.strip()
                    if Danhgiacode.objects.filter(danhgiacode=itemstrip).count<=0:
                        danhgia = Danhgiacode(danhgiacode = itemstrip)
                        danhgia.save()
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
                strdanhgia = split(sheet.cell(r,2).value,",")
                for item in strdanhgia:
                    itemstrip = item.strip()
                    if Danhgiacode.objects.filter(danhgiacode=itemstrip).count<=0:
                        danhgia = Danhgiacode(danhgiacode = itemstrip)
                        danhgia.save()
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