from datetime import date
import csv
from numpy import NaN
import xlwt
from tablib import Dataset
from xlwt.Workbook import Workbook
from .models import Contract, DanhgiaNCC, Danhgiacode, G1code, G2code, GDV, Gcode, Giaohang,Inquiry,Client, Kho, Lydowin, POdetail, Phat, Sales, ScanOrder,Supplier,Lydoout, Tienve
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse
import pandas as pd
import xlsxwriter
from django.utils.html import format_html

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
    columns = ['ID','Gcode', 'Mô tả', 'Markup định mức','Ngày Out gần nhất','Ngày Win gần nhất']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for gcode in Gcode.objects.all():
        row_num += 1
        ws.write(row_num, col_num, gcode.id, style_data_row)
        ws.write(row_num, col_num, gcode.ma, style_data_row)
        ws.write(row_num, col_num, gcode.mota, style_data_row)
        ws.write(row_num, col_num, gcode.markupdinhmuc, style_number_row)
        ws.write(row_num, col_num, gcode.ngaywin, style_date_row)
        ws.write(row_num, col_num, gcode.ngayout, style_date_row)
    wb.save(response)
    return response
    
def exportxls_contractdetail(request):
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

def exportxls_danhgiacode(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Danh gia code.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Đánh giá code')
    row_num = 0 
    columns = ['ID','Đánh giá code']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for danhgia in Danhgiacode.objects.all():
        row_num += 1
        ws.write(row_num, 0, danhgia.id, style_data_row)
        ws.write(row_num, 1, danhgia.danhgiacode, style_data_row)
    wb.save(response)
    return response

def exportxls_offer_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Offer.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Offer')
    row_num = 0  
    columns = ['ID','Gcode-Inquiry','Gcode','Inquiry','Ký mã hiệu','Đơn vị','Số lượng','Supplier','Xuất xứ','NSX',
    'STT in ITB','Group in ITB','Sale','Đơn giá mua','Đơn giá chào',
    'Markup','Result','Lý do Win','Lý do Out','Ghi Chú','Giao dịch viên','Ngày cập nhật']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for offer in G1code.objects.all():
        row_num += 1
        ws.write(row_num, 0, offer.id, style_data_row)
        ws.write(row_num, 1, offer.g1code, style_data_row)
        ws.write(row_num, 2, offer.gcode.ma, style_data_row)
        ws.write(row_num, 3, offer.inquiry.inquirycode, style_data_row)
        ws.write(row_num, 4, offer.kymahieuinq, style_data_row)
        ws.write(row_num, 5, offer.unitinq, style_data_row)
        ws.write(row_num, 6, offer.qtyinq, style_number_row)
        ws.write(row_num, 7, offer.supplier.suppliercode, style_data_row)
        ws.write(row_num, 8, offer.xuatxuinq, style_data_row)
        ws.write(row_num, 9, offer.nsxinq, style_data_row)
        ws.write(row_num, 10, offer.sttitb, style_data_row)
        ws.write(row_num, 11, offer.groupitb, style_data_row)
        ws.write(row_num, 12, offer.sales.salescode, style_data_row)
        ws.write(row_num, 13, offer.dongiamuainq, style_number_row)
        ws.write(row_num, 14, offer.dongiachaoinq, style_number_row)
        ws.write(row_num, 15, offer.markupinq, style_number_row)
        if offer.resultinq == 'Win':
            ws.write(row_num, 16, offer.resultinq, style_green_row)
        else:
            ws.write(row_num, 16, offer.resultinq, style_red_row)
        strlydowin =""
        for lydowin in offer.lydowin.all():
            strlydowin = lydowin.lydowincode + "," + strlydowin
        ws.write(row_num, 17, strlydowin, style_data_row)
        strlydoout =""
        for lydoout in offer.lydoout.all():
            strlydoout = lydoout.lydooutcode + "," + strlydoout
        ws.write(row_num, 18, strlydoout, style_data_row)
        ws.write(row_num, 19, offer.ghichu, style_data_row)
        ws.write(row_num, 20, offer.gdvinq.gdvcode, style_data_row)
        ws.write(row_num, 21, offer.dateupdate, style_date_row)
    wb.save(response)
    return response

def exportxls_offer(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Offer.xlsx"'
    list_null = []
    df = pd.DataFrame({'STT':list_null,'Gcode':list_null,'Inquiry':list_null,'Ký mã hiệu':list_null,'Đơn vị':list_null,'Số lượng':list_null,
    'Supplier':list_null,'Xuất xứ':list_null,'NSX':list_null,'STT in ITB':list_null,'Group in ITB':list_null,'Sale':list_null,
    'Đơn giá mua':list_null,'Đơn giá chào':list_null,'Giao dịch viên':list_null,'Ghi Chú':list_null,'Result':list_null})
    for lydowin in Lydowin.objects.all():
        df[lydowin.lydowincode]=None
    for lydoout in Lydoout.objects.all():
        df[lydoout.lydooutcode]=None    
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Offer', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Offer']
    #Format header 
    header_format = workbook.add_format({
    'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center','fg_color': '#4788F9','font_color': 'white','border': 1})
    lydo_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center','fg_color': '#F9B747','font_color': 'black','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})

    for col_num, value in enumerate(df.columns.values):
        if col_num <= df.columns.get_loc('Result'):
            worksheet.write(0, col_num, value, header_format)
        else:
            worksheet.write(0, col_num, value, lydo_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Đơn giá mua','Đơn giá chào']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    #worksheet.set_column('F:F', None, fm_float)
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_hdb(request,id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Contract.xlsx"'
    df = pd.DataFrame(columns=['STT','Inquiry','Gcode','Contract No.','Mô tả','Ký mã hiệu','Đơn vị','Số lượng','Đơn giá chào',
            'PO No.','Supplier','STT in ITB','Group in ITB','Xuất xứ','NSX','Ghi Chú','Giao dịch viên'])  
    g1code_list = G1code.objects.filter(inquiry__pk=id,resultinq = "Win")
    stt = 1
    for item in g1code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Inquiry':[item.inquiry.inquirycode],'Gcode':[item.gcode.ma],'Mô tả':[item.gcode.mota],'Ký mã hiệu':[item.kymahieuinq],
        'Đơn vị':[item.unitinq],'Số lượng':[item.qtyinq],'Đơn giá chào':[item.dongiachaoinq],'Supplier':[item.supplier.suppliercode],
        'STT in ITB':[item.sttitb],'Group in ITB':[item.groupitb],'Xuất xứ':[item.xuatxuinq],'NSX':[item.nsxinq]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Contract', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Contract']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    #date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['Inquiry','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng','Supplier','Xuất xứ','NSX']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Đơn giá chào']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    #worksheet.set_column('F:F', None, fm_float)
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_hdb_all(request,id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Gcode-Contract.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Gcode-Contract')
    row_num = 0  
    columns = ['ID','Gcode-Contract', 'Contract No.','Đơn giá chào','PO No.','Status','Gcode-Inquiry','Ghi chú','Giao dịch viên','Ngày cập nhật']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for g2code_ in G2code.objects.all():
        row_num += 1
        ws.write(row_num, 0, g2code_.id, style_data_row)
        ws.write(row_num, 1, "", style_data_row)
        ws.write(row_num, 2, "", style_data_row)
        ws.write(row_num, 3, g2code_.dongiachaohdb, style_number_row)
        ws.write(row_num, 4, "", style_data_row)
        ws.write(row_num, 5, "Chưa đặt", style_data_row)
        ws.write(row_num, 6, g2code_.g1code.g1code, style_data_row)
        ws.write(row_num, 7, "", style_data_row)
        ws.write(row_num, 8, "", style_data_row)
        ws.write(row_num, 9, date.today(), style_date_row)
    wb.save(response)
    return response

def exportxls_poall(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Po.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Purchase Order')
    row_num = 0  
    columns = ['ID','Gcode-Contract', 'Mô tả','Ký hiệu mã','Đơn vị','Số lượng','Supplier','Xuất xứ','NSX','Đơn giá mua','Ghi chú','Giao dịch viên','Ngày cập nhật']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for g2code_ in POdetail.objects.all():
        row_num += 1
        ws.write(row_num, 0, g2code_.id, style_data_row)
        ws.write(row_num, 1, g2code_.g2code.g2code, style_data_row)
        ws.write(row_num, 2, g2code_.motapo, style_data_row)
        ws.write(row_num, 3, g2code_.kymahieupo, style_data_row)
        ws.write(row_num, 4, g2code_.unitpo, style_data_row)
        ws.write(row_num, 5, g2code_.qtypo, style_number_row)
        ws.write(row_num, 6, g2code_.supplier.suppliercode, style_data_row)
        ws.write(row_num, 7, g2code_.xuatxupo, style_data_row)
        ws.write(row_num, 8, g2code_.nsxpo, style_data_row)
        ws.write(row_num, 9, g2code_.dongiamuapo, style_number_row)
        ws.write(row_num, 10, g2code_.ghichu, style_data_row)
        ws.write(row_num, 11, g2code_.gdvpo.gdvcode, style_data_row)
        ws.write(row_num, 12, g2code_.dateupdate, style_date_row)
    wb.save(response)
    return response

def exportxls_po(request,po):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="POdetail.xlsx"'
    df = pd.DataFrame(columns=['STT','PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng','NSX','Xuất xứ',
    'Supplier','Đơn giá mua','Ghi Chú','Giao dịch viên'])
    g2code_list = G2code.objects.filter(pono=po)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'PO No.':[po],'Contract No.':[item.contract.contractcode],'Gcode':[item.gcode],
        'Mô tả':[item.mota],'Ký mã hiệu':[item.kymahieu],'Đơn vị':[item.unit],'Số lượng':[item.qty],'NSX':[item.nsx],'Xuất xứ':[item.xuatxu],
        'Supplier':[item.supplier],'Đơn giá mua':[item.g1code.dongiamuainq]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='POdetail', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['POdetail']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    #date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['PO No.','Contract No.','Gcode']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Đơn giá mua']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    #worksheet.set_column('F:F', None, fm_float)
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_kho(request,po):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Nhapkho.xlsx"'
    df = pd.DataFrame(columns=['STT','PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng',
    'Đơn giá freight','Ngày hàng về kho','Ghi Chú','Giao dịch viên'])
    podetail_list = POdetail.objects.filter(g2code__pono=po)
    stt = 1
    for item in podetail_list:
        df = df.append(pd.DataFrame({'STT':[stt],'PO No.':[po],'Contract No.':[item.g2code.contract.contractcode],'Gcode':[item.gcode],
        'Mô tả':[item.motapo],'Ký mã hiệu':[item.kymahieupo],'Đơn vị':[item.unitpo],'Số lượng':[item.g2code.qtychuanhapkho]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Nhập kho', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Nhập kho']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Đơn giá freight']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Ngày hàng về kho']
    list_index_fm_date = []
    for item in list_column_fm_date:
        list_index_fm_date.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        elif col in list_index_fm_date:
            worksheet.set_column(col,col, None, date_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_giaohang(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Delivery.xlsx"'
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng',
    'Ngày giao hàng','Ghi Chú','Giao dịch viên'])

    g2code_list = Kho.objects.filter(g2code__contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],
        'Mô tả':[item.mota],'Ký mã hiệu':[item.kymahieu],'Đơn vị':[item.unit],'Số lượng':[item.g2code.qtychuagiao]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Delivery', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Delivery']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Ngày giao hàng']
    list_index_fm_date = []
    for item in list_column_fm_date:
        list_index_fm_date.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        elif col in list_index_fm_date:
            worksheet.set_column(col,col, None, date_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_phat(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Punishment.xlsx"'
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng',
    'Tổng phạt','Lý do phạt','Ghi Chú','Giao dịch viên'])
    g2code_list = Giaohang.objects.filter(g2code__contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],
        'Mô tả':[item.mota],'Ký mã hiệu':[item.kymahieu],'Đơn vị':[item.unit],'Số lượng':[item.qtygiaohang]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Punishment', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Punishment']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Tổng phạt']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_danhgiancc(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="DanhgiaNCC.xlsx"'
    df = pd.DataFrame(columns=['STT','PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị',
    'Số lượng','NSX','Xuất xứ','Supplier','Đơn giá mua','Thành tiền mua','Ghi Chú','Giao dịch viên'])
    for danhgia in Danhgiacode.objects.all():
        df[danhgia.danhgiacode]=None
    g2code_list = POdetail.objects.filter(g2code__contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'PO No.':[item.pono],'Contract No.':[contract],'Gcode':[item.gcode],
        'Mô tả':[item.motapo],'Ký mã hiệu':[item.kymahieupo],'Đơn vị':[item.unitpo],'Số lượng':[item.qtypo],
        'NSX':[item.nsxpo],'Xuất xứ':[item.xuatxupo],'Supplier':[item.supplier],'Đơn giá mua':[item.dongiamuapo],'Thành tiền mua':[item.thanhtienmuapo]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Đánh giá NCC', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Đánh giá NCC']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    danhgia_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#F9B747','font_color': 'black','border': 1})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị',
    'Số lượng','NSX','Xuất xứ','Supplier','Đơn giá mua','Thành tiền mua']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        elif col_num <= df.columns.get_loc('Giao dịch viên'):
            worksheet.write(0, col_num, value, header_format)
        else:
           worksheet.write(0, col_num, value, danhgia_format) 
    # Add some cell formats.
    list_column_fm_float = ['Đơn giá mua','Thành tiền mua']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response

def exportxls_tienve(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Accounting.xlsx"'
    df = pd.DataFrame(columns=['STT','PO No.','Contract No.','Client','Gcode','Mô tả','Ký mã hiệu','Đơn vị',
    'NSX','Xuất xứ','Supplier','Số lượng','Đơn giá tiền về','Thành tiền','Ghi Chú'])
    g2code_list = G2code.objects.filter(contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'PO No.':[item.pono],'Contract No.':[contract],'Client':[item.contract.client.clientcode],
        'Gcode':[item.gcode],'Mô tả':[item.mota],'Ký mã hiệu':[item.kymahieu],'Đơn vị':[item.unit],
        'Số lượng':[item.qty],'Đơn giá tiền về':[item.dongiachaohdb],'NSX':[item.nsx],'Xuất xứ':[item.xuatxu],'Supplier':[item.supplier]}))
        stt +=1
    df['Thành tiền']= df['Số lượng']*df['Đơn giá tiền về']
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Accounting', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Accounting']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['PO No.','Contract No.','Client','Gcode','Mô tả','Ký mã hiệu','Đơn vị',
    'NSX','Xuất xứ','Supplier']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Đơn giá tiền về','Thành tiền']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    writer.save()
    return response


def exportxls_sales(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales')
    row_num = 0  
    columns = ['ID','Tên viết tắt', 'Tên đầy đủ']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for sales in Sales.objects.all():
        row_num += 1
        ws.write(row_num, 0, sales.id, style_data_row)
        ws.write(row_num, 1, sales.salescode, style_data_row)
        ws.write(row_num, 2, sales.fullname, style_data_row)
    wb.save(response)
    return response

def exportxls_profit(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Profit.xlsx"'
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','NSX','Xuất xứ','Supplier','Số lượng bán',
    'Số lượng mua','Số lượng nhập kho','Số lượng giao','Số lượng phạt','Đơn giá bán',
    'Đơn giá mua offer','Đơn giá mua PO' ,'Đơn giá freight','Tổng phạt',
    'Lợi nhuận chưa đặt hàng','Lợi nhuận chưa về kho','Lợi nhuận chưa giao hàng','Lợi nhuận thực tế',
    'Lợi nhuận tổng','Tiền về thực tế','Tiền về dự kiến'])
    g2code_list = G2code.objects.filter(contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        lncdh = item.qtychuadat*(item.dongiachaohdb-item.dongiamuainq)
        lncvk = item.qtychuanhapkho*(item.dongiachaohdb-item.dongiamuapo)
        lncgh = item.qtychuagiao*(item.dongiachaohdb-item.dongiamuapo-item.dongiafreight)
        lntt = item.qtygiaohang*(item.dongiachaohdb-item.dongiamuapo-item.dongiafreight)-item.tongphat
        lntong = lncdh+lncgh+lncvk+lntt
        tvdk = item.qty*item.dongiachaohdb-item.tongphat-item.tongtienve

        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],'Mô tả':[item.mota],
        'Ký mã hiệu':[item.kymahieu],'Đơn vị':[item.unit],'NSX':[item.nsx],'Xuất xứ':[item.xuatxu],'Supplier':[item.supplier],
        'Số lượng bán':[item.qty],'Số lượng mua':[item.qtypo],'Số lượng nhập kho':[item.qtykho],
        'Số lượng giao':[item.qtygiaohang],'Số lượng phạt':[item.qtyphat],'Đơn giá bán':[item.dongiachaohdb],
        'Đơn giá mua offer':[item.dongiamuainq],'Đơn giá mua PO':[item.dongiamuapo] ,'Đơn giá freight':[item.dongiafreight],
        'Tổng phạt':[item.tongphat],'Lợi nhuận chưa đặt hàng':[lncdh],'Lợi nhuận chưa về kho':[lncvk],
        'Lợi nhuận chưa giao hàng':[lncgh],'Lợi nhuận thực tế':[lntt],
        'Lợi nhuận tổng':[lntong],'Tiền về thực tế':[item.tongtienve],'Tiền về dự kiến':[tvdk]}))
        stt +=1
    df.loc['Total']= df.sum(numeric_only=True, axis=0)
    df.loc['Total','STT']='Total'
    df = df.replace({NaN: ''})
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Profit', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Profit']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    profit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#7EF68B','font_color': 'black','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    total_format = workbook.add_format({'bold': True,'fg_color': '#FFFA5B','text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    list_header_profit = ['Lợi nhuận chưa đặt hàng','Lợi nhuận chưa về kho','Lợi nhuận chưa giao hàng','Lợi nhuận thực tế',
    'Lợi nhuận tổng','Tiền về thực tế','Tiền về dự kiến']
    list_index_fm_profit = []
    for item in list_header_profit:
        list_index_fm_profit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_profit:
            worksheet.write(0, col_num, value, profit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng bán',
    'Số lượng mua','Số lượng nhập kho','Số lượng giao','Số lượng phạt','Đơn giá bán',
    'Đơn giá mua offer','Đơn giá mua PO' ,'Đơn giá freight','Tổng phạt',
    'Lợi nhuận chưa đặt hàng','Lợi nhuận chưa về kho','Lợi nhuận chưa giao hàng','Lợi nhuận thực tế',
    'Lợi nhuận tổng','Tiền về thực tế','Tiền về dự kiến']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        for r in range(1,df.shape[0]+1):
            if r == df.shape[0]:
                worksheet.write(r,col, df.iloc[r-1,col], total_format) 
            elif col in list_index_fm_float:
                worksheet.write(r,col, df.iloc[r-1,col], float_format)
            else:
                worksheet.write(r,col, df.iloc[r-1,col], text_format)
    writer.save()
    return response

def exportxls_scanorder(request,id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Scan Order.xlsx"'
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    scanorder = ScanOrder.objects.get(pk=id)
    df = pd.DataFrame(columns=['STT'])
    index = 0
    for gcode_ in scanorder.gcode.all():
        g1code = G1code.objects.filter(gcode__ma=gcode_).order_by('-gcode__ngaywin','-gcode__ngayout')[0]
        df.loc[index,'STT']=index+1
        df.loc[index,'Gcode']=g1code.gcode.ma
        df.loc[index,'Inquiry'] = g1code.inquiry.inquirycode
        df.loc[index,'Khách hàng'] = g1code.inquiry.client.clientcode
        df.loc[index,'Mô tả'] = g1code.gcode.mota
        df.loc[index,'Ký mã hiệu'] = g1code.kymahieuinq
        df.loc[index,'Đơn vị'] = g1code.unitinq
        df.loc[index,'Số lượng'] = g1code.qtyinq
        df.loc[index,'NSX'] = g1code.nsxinq
        df.loc[index,'Xuất xứ'] = g1code.xuatxuinq
        df.loc[index,'Supplier'] = g1code.supplier.suppliercode
        df.loc[index,'Đơn giá mua'] = g1code.dongiamuainq
        df.loc[index,'Thành tiền mua'] = g1code.dongiamuainq * g1code.qtyinq
        df.loc[index,'Ngày submit thầu'] = g1code.inquiry.datesubmitbid
        df.loc[index,'Đơn giá chào'] = g1code.dongiachaoinq
        df.loc[index,'Thành tiền chào'] = g1code.dongiachaoinq * g1code.qtyinq
        df.loc[index,'Hệ số mark up'] = g1code.markupinq
        df.loc[index,'Result'] = g1code.resultinq
        for item in g1code.lydowin.all():
            df.loc[index,item.lydowincode] = 'Yes'
        for item in g1code.lydoout.all():
            df.loc[index,item.lydooutcode] = 'Yes'
        index +=1
    df = df.replace({NaN: ''})
    df.to_excel(writer, sheet_name='Scan Order', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Scan Order']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Số lượng','Đơn giá mua','Thành tiền mua','Đơn giá chào','Thành tiền chào','Hệ số mark up']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        for r in range(1,df.shape[0]+1):
            if col in list_index_fm_float:
                worksheet.write(r,col, df.iloc[r-1,col], float_format)
            else:
                worksheet.write(r,col, df.iloc[r-1,col], text_format)
    writer.save()
    return response