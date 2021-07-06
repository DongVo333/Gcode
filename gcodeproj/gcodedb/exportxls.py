from datetime import date
import csv
import xlwt
from tablib import Dataset
from .models import Contract, G1code, G2code, GDV, Gcode,Inquiry,Client, Kho, Lydowin,Supplier,Lydoout
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse

style_head_row = xlwt.easyxf(" align:wrap off,vert center,horiz center;borders:left THIN,right THIN,top THIN,bottom THIN;font:name Arial,colour_index white,bold on,height 0xA0;pattern:pattern solid,fore-colour ocean_blue;") 
style_number_row = xlwt.easyxf(" align: wrap on,vert center,horiz left; font: name Arial,bold off,height 0XA0;borders:left THIN,right THIN,top THIN,bottom THIN;")
style_date_row = xlwt.easyxf(" align: wrap on,vert center,horiz left; font: name Arial,bold off,height 0XA0;borders:left THIN,right THIN,top THIN,bottom THIN;")
style_data_row = xlwt.easyxf(" align: wrap on,vert center,horiz left; font: name Arial,bold off,height 0XA0;borders:left THIN,right THIN,top THIN,bottom THIN;")
style_green_row = xlwt.easyxf(" align: wrap on,vert center,horiz center; font: name Arial,bold off,height 0XA0;borders:left THIN,right THIN,top THIN,bottom THIN;pattern: fore-colour bright_green, pattern solid;")
style_red_row = xlwt.easyxf(" align: wrap on,vert center,horiz center; font: name Arial,bold off,height 0XA0;borders:left THIN,right THIN,top THIN,bottom THIN;pattern: fore-colour 0x0A, pattern solid;")
fmts = [
    'dd/mm/yyyy',
    '#,##0.00',
]
style_number_row.num_format_str = fmts[1]
style_date_row.num_format_str = fmts[0]

def exportxls_client(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Client.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Client')
    row_num = 0
    columns = ['ID','Client', 'Fullname', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    font_style = xlwt.XFStyle()
    rows = Client.objects.all().values_list('id','clientcode','fullname')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style_data_row)
    wb.save(response)
    return response

def exportxls_gcode(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Gcode.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Gcode')
    row_num = 0
    columns = ['ID','Gcode', 'Mô tả', 'Markup định mức']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for gcode in Gcode.objects.all():
        row_num += 1
        ws.write(row_num, col_num, gcode.id, style_data_row)
        ws.write(row_num, col_num, gcode.ma, style_data_row)
        ws.write(row_num, col_num, gcode.mota, style_data_row)
        ws.write(row_num, col_num, gcode.markupdinhmuc, style_number_row)
    wb.save(response)
    return 
    
def exportxls_contract(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Contract.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Contract')
    row_num = 0
    columns = ['ID','Contract', 'Contract No. Client', 'Date Sign','Client','Deadline 1','Deadline 2','Selling Price','Status','Date Delivery Latest']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for contract in Contract.objects.all():
        row_num += 1
        ws.write(row_num, 0, contract.id, style_data_row)
        ws.write(row_num, 1, contract.contractcode, style_data_row)
        ws.write(row_num, 2, contract.contractnoclient, style_data_row)
        ws.write(row_num, 3, contract.datesign, style_date_row)
        ws.write(row_num, 4, contract.client.clientcode, style_data_row)
        ws.write(row_num, 5, contract.dealine1, style_date_row)
        ws.write(row_num, 6, contract.dealine2, style_date_row)
        ws.write(row_num, 7, contract.sellcost, style_number_row)
        if contract.status == "Close":
            ws.write(row_num, 8, contract.status, style_red_row)
        else:
            ws.write(row_num, 8, contract.status, style_green_row)
        ws.write(row_num, 9, contract.datedeliverylatest, style_date_row)
    wb.save(response)
    return response

def exportxls_inquiry(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Inquiry.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Inquiry')
    row_num = 0   
    columns = ['ID','Inquiry', 'Ngày submit thầu', 'Khách hàng']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for inquiry in Inquiry.objects.all():
        row_num += 1
        ws.write(row_num, 0, inquiry.id, style_data_row)
        ws.write(row_num, 1, inquiry.inquirycode, style_data_row)
        ws.write(row_num, 2, inquiry.datesubmitbid, style_date_row)
        ws.write(row_num, 3, inquiry.client.clientcode, style_data_row)
    wb.save(response)
    return response

def exportxls_gdv(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="GDV.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GDV')
    row_num = 0
    columns = ['ID','Giao dịch viên', 'Tên đầy đủ']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for gdv in GDV.objects.all():
        row_num += 1
        ws.write(row_num, 0, gdv.id, style_data_row)
        ws.write(row_num, 1, gdv.gdvcode, style_data_row)
        ws.write(row_num, 2, gdv.fullname, style_data_row)
    wb.save(response)
    return response

def exportxls_supplier(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Supplier.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GDV')
    row_num = 0  
    columns = ['ID','Supplier', 'Tên đầy đủ','Duyệt PO (max)']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for supplier in Supplier.objects.all():
        row_num += 1
        ws.write(row_num, 0, supplier.id, style_data_row)
        ws.write(row_num, 1, supplier.suppliercode, style_data_row)
        ws.write(row_num, 2, supplier.fullname, style_data_row)
        ws.write(row_num, 3, supplier.duyetpomax, style_number_row)
    wb.save(response)
    return response

def exportxls_lydowin(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lydowin.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lydowin')
    row_num = 0
    columns = ['ID','Lý do win', 'Chi tiết']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for lydowin in Lydowin.objects.all():
        row_num += 1
        ws.write(row_num, 0, lydowin.id, style_data_row)
        ws.write(row_num, 1, lydowin.lydowincode, style_data_row)
        ws.write(row_num, 2, lydowin.detail, style_data_row)
    wb.save(response)
    return response

def exportxls_lydoout(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lydoout.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lydoout')
    row_num = 0 
    columns = ['ID','Lý do out', 'Chi tiết']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for lydoout in Lydoout.objects.all():
        row_num += 1
        ws.write(row_num, 0, lydoout.id, style_data_row)
        ws.write(row_num, 1, lydoout.lydooutcode, style_data_row)
        ws.write(row_num, 2, lydoout.detail, style_data_row)
    wb.save(response)
    return response

def exportxls_kho(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Kho.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Kho')
    row_num = 0  
    columns = ['ID','Gcode-HDB', 'Số lượng về kho','Đơn giá Freight','Ngày nhập kho','Giao Dịch Viên','Ngày cập nhật']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for kho in Kho.objects.all():
        row_num += 1
        ws.write(row_num, 0, kho.id, style_data_row)
        ws.write(row_num, 1, kho.g2code.g2code, style_data_row)
        ws.write(row_num, 2, kho.qtykho, style_number_row)
        ws.write(row_num, 3, kho.dongiafreight, style_number_row)
        ws.write(row_num, 4, kho.ngaynhapkho, style_date_row)
        ws.write(row_num, 5, kho.gdvkho.gdvcode, style_data_row)
        ws.write(row_num, 6, kho.gdvkho.dateupdate, style_date_row)
    wb.save(response)
    return response

def exportxls_offer(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Kho.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Offer')
    row_num = 0  
    columns = ['ID', 'Gcode','Inquiry','Ký mã hiệu','Đơn vị','Số lượng','Supplier','Xuất xứ','NSX',
    'STT in ITB','Group in ITB','Sale','Đơn giá mua','Thành tiền mua','Đơn giá chào','Thành tiền chào',
    'Markup','Result','Lý do Win','Lý do Out','Ghi Chú','Giao dịch viên','Ngày cập nhật']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for offer in G1code.objects.all():
        row_num += 1
        ws.write(row_num, 0, offer.id, style_data_row)
        ws.write(row_num, 1, offer.gcode.ma, style_data_row)
        ws.write(row_num, 2, offer.inquiry.inquirycode, style_data_row)
        ws.write(row_num, 3, offer.kymahieuinq, style_data_row)
        ws.write(row_num, 4, offer.unitinq, style_data_row)
        ws.write(row_num, 5, offer.qtyinq, style_number_row)
        ws.write(row_num, 6, offer.supplier.suppliercode, style_data_row)
        ws.write(row_num, 7, offer.xuatxuinq, style_data_row)
        ws.write(row_num, 8, offer.nsxinq, style_data_row)
        ws.write(row_num, 9, offer.sttitb, style_data_row)
        ws.write(row_num, 10, offer.groupitb, style_data_row)
        ws.write(row_num, 11, offer.sales, style_data_row)
        ws.write(row_num, 12, offer.dongiamuainq, style_number_row)
        ws.write(row_num, 13, offer.thanhtienmua, style_number_row)
        ws.write(row_num, 14, offer.dongiachaoinq, style_number_row)
        ws.write(row_num, 15, offer.thanhtienchao, style_number_row)
        ws.write(row_num, 16, offer.markupinq, style_number_row)
        if offer.resultinq == 'Win':
            ws.write(row_num, 17, offer.resultinq, style_green_row)
        else:
            ws.write(row_num, 17, offer.resultinq, style_red_row)
        ws.write(row_num, 18, offer.lydowin, style_data_row)
        ws.write(row_num, 19, offer.lydoout, style_data_row)
        ws.write(row_num, 20, offer.ghichu, style_data_row)
        ws.write(row_num, 21, offer.gdvinq.gdvcode, style_data_row)
        ws.write(row_num, 22, offer.dateupdate, style_date_row)


    wb.save(response)
    return response
