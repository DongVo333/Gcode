from datetime import date
import csv
import xlwt
from tablib import Dataset
from .models import Contract, G1code, G2code, GDV, Gcode,Inquiry,Client, Kho, Lydowin,Supplier,Lydoout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse

def exportxls_client(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Client.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Client')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Client', 'Fullname', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Client.objects.all().values_list('clientcode','fullname')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def exportxls_gcode(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Gcode.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Gcode')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Gcode', 'Mô tả', 'Markup định mức']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Gcode.objects.all().values_list('ma','mota','markupdinhmuc')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return 
    
def exportxls_contract(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Contract.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Contract')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Contract', 'Contract No. Client', 'Date Sign','Client','Deadline 1','Deadline 2','Selling Price','Status','Date Delivery Latest']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Contract.objects.all().values_list('contractcode','contractnoclient','datesign','clientcode','dealine1','dealine2','sellcost','status','datedeliverylatest')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportxls_inquiry(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Inquiry.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Inquiry')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ['Inquiry', 'Ngày submit thầu', 'Khách hàng']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Inquiry.objects.all().values_list('inquirycode','datesubmitbid','clientcode')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportxls_gdv(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="GDV.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GDV')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ['Giao dịch viên', 'Tên đầy đủ']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = GDV.objects.all().values_list('gdvcode','fullname')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportxls_supplier(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Supplier.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GDV')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ['Supplier', 'Tên đầy đủ','Duyệt PO (max)']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Supplier.objects.all().values_list('suppliercode','fullname','duyetpomax')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportxls_lydowin(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lydowin.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lydowin')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ['Lý do win', 'Chi tiết']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Lydowin.objects.all().values_list('lydowincode','detail')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportxls_lydoout(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lydoout.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lydoout')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ['Lý do out', 'Chi tiết']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Lydoout.objects.all().values_list('lydooutcode','detail')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def exportxls_kho(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Kho.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Kho')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True    
    columns = ['Gcode-HDB', 'Số lượng về kho','Đơn giá Freight','Ngày nhập kho','Giao Dịch Viên','Ngày cập nhật']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Kho.objects.all().values_list('g2code','qtykho','dongiafreight','ngaynhapkho','gdvkho','dateupdate')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
