from datetime import date
import csv
from numpy import NaN
import xlwt
from tablib import Dataset
from xlwt.Workbook import Workbook
from .models import Contract, Danhgiagcode, G1code, Nhaplieuban, GDV, Gcode,Inquiry,Client, Lydowin, PAMHop, Phat, Sales, ScanOrder,Supplier,Lydoout, Tienve,Nhaplieumua,Nhaplieunhapkhau, Tinhtrangiaiquyetkhokhan, Unit
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth.decorators import login_required
from .decorators import allowed_permission
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_client'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_gcode'})
def exportxls_gcode_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Gcode.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Gcode')
    row_num = 0
    columns = ['STT','Gcode','Part number','Description','Markup ?????nh m???c','Ng??y Win','Ng??y Out']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_gcode'})
def exportxls_gcode(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Gcode.xlsx"'
    df = pd.DataFrame(columns=['STT','Gcode','Part number','Description','Markup ?????nh m???c'])  
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Gcode', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Gcode']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Markup ?????nh m???c']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Deadline giao h??ng cho kh??ch h??ng']
    list_index_fm_date = []
    for item in list_column_fm_date:
        list_index_fm_date.append(df.columns.get_loc(item))

    list_unit = []
    for item in Unit.objects.all():
        list_unit.append(item.unit) 
    unit_col = df.columns.get_loc('Unit')
    worksheet.data_validation(0,unit_col,100,unit_col,{'validate': 'list',
                                 'source': list_unit})
    list_sales = []
    for item in Sales.objects.all():
        list_sales.append(item.salescode)
    sales_col = df.columns.get_loc('Sales manager')
    worksheet.data_validation(0,sales_col,100,sales_col,{'validate': 'list',
                                 'source': list_sales})

    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        elif col in list_index_fm_date:
            worksheet.set_column(col,col, None, date_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    for column in range(2, 101):
        cell_location = 'M{0}'.format(column)
        formula = '=IF($K{0}*$L{0}=0,"",$K{0}*$L{0})'.format(column)
        worksheet.write_formula(cell_location, formula, float_format)

    writer.save()
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_contract'})    
def exportxls_contract_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Contract.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Contract')
    row_num = 0
    columns = ['ID','Contract No.', 'Contract No. (Client)', 'Ng??y k?? k???t','Kh??ch h??ng','Sales','Gi?? b??n','Tr???ng th??i','Ng??y giao h??ng cu???i c??ng']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_contract'})    
def exportxls_contract (request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Contract.xlsx"'
    df = pd.DataFrame(columns=['Stt','Contract No.', 'Contract No. (Client)', 'Ng??y k?? k???t','Kh??ch h??ng',
    'Sales','Deadline giao h??ng NLB','Deadline giao h??ng NLM','Gi?? b??n','Tr???ng th??i','Ng??y giao h??ng cu???i c??ng'])  
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
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Gi?? b??n']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Ng??y k?? k???t','Ng??y giao h??ng cu???i c??ng','Deadline giao h??ng NLB','Deadline giao h??ng NLM']
    list_index_fm_date = []
    for item in list_column_fm_date:
        list_index_fm_date.append(df.columns.get_loc(item))

    list_sales = []
    for item in Sales.objects.all():
        list_sales.append(item.salescode)
    sales_col = df.columns.get_loc('Sales')
    worksheet.data_validation(0,sales_col,100,sales_col,{'validate': 'list',
                                 'source': list_sales})
    list_client = []
    for item in Client.objects.all():
        list_client.append(item.clientcode)
    client_col = df.columns.get_loc('Kh??ch h??ng')
    worksheet.data_validation(0,client_col,100,client_col,{'validate': 'list',
                                 'source': list_client})

    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        elif col in list_index_fm_date:
            worksheet.set_column(col,col, None, date_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    for column in range(2, 101):
        cell_location = 'H{0}'.format(column)
        formula = '=IF($G{0}="","",$G{0})'.format(column)
        worksheet.write_formula(cell_location, formula, date_format)
    writer.save()
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_inquiry'}) 
def exportxls_inquiry(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Inquiry.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Inquiry')
    row_num = 0   
    columns = ['ID','Inquiry', 'Ng??y submit th???u', 'Kh??ch h??ng']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_gdv'}) 
def exportxls_gdv(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="GDV.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GDV')
    row_num = 0
    columns = ['ID','Giao d???ch vi??n', 'T??n ?????y ?????']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for gdv in GDV.objects.all():
        row_num += 1
        ws.write(row_num, 0, gdv.id, style_data_row)
        ws.write(row_num, 1, gdv.gdvcode, style_data_row)
        ws.write(row_num, 2, gdv.fullname, style_data_row)
    wb.save(response)
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_supplier'}) 
def exportxls_supplier(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Supplier.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GDV')
    row_num = 0  
    columns = ['ID','Supplier', 'T??n ?????y ?????','Duy???t PO (max)']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_reasonwin'}) 
def exportxls_lydowin(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lydowin.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lydowin')
    row_num = 0
    columns = ['ID','L?? do win', 'Chi ti???t']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for lydowin in Lydowin.objects.all():
        row_num += 1
        ws.write(row_num, 0, lydowin.id, style_data_row)
        ws.write(row_num, 1, lydowin.lydowincode, style_data_row)
        ws.write(row_num, 2, lydowin.detail, style_data_row)
    wb.save(response)
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_reasonout'}) 
def exportxls_lydoout(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lydoout.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Lydoout')
    row_num = 0 
    columns = ['ID','L?? do out', 'Chi ti???t']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for lydoout in Lydoout.objects.all():
        row_num += 1
        ws.write(row_num, 0, lydoout.id, style_data_row)
        ws.write(row_num, 1, lydoout.lydooutcode, style_data_row)
        ws.write(row_num, 2, lydoout.detail, style_data_row)
    wb.save(response)
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_danhgiacode'}) 
def exportxls_danhgiacode(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Danh gia code.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('????nh gi?? code')
    row_num = 0 
    columns = ['ID','????nh gi?? code']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for danhgia in Danhgiagcode.objects.all():
        row_num += 1
        ws.write(row_num, 0, danhgia.id, style_data_row)
        ws.write(row_num, 1, danhgia.danhgiacode, style_data_row)
    wb.save(response)
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_all_g1code'}) 
def exportxls_offer_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Offer.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Offer')
    row_num = 0  
    columns = ['ID','Gcode-Inquiry','Gcode','Inquiry','K?? m?? hi???u','????n v???','S??? l?????ng','Supplier','Xu???t x???','NSX',
    'STT in ITB','Group in ITB','Sale','????n gi?? mua','????n gi?? ch??o',
    'Markup','Result','L?? do Win','L?? do Out','Ghi Ch??','Giao d???ch vi??n','Ng??y c???p nh???t']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for offer in G1code.objects.all():
        row_num += 1
        ws.write(row_num, 0, offer.id, style_data_row)
        ws.write(row_num, 1, offer.g1code, style_data_row)
        ws.write(row_num, 2, offer.gcode.ma, style_data_row)
        ws.write(row_num, 3, offer.inquiry.inquirycode, style_data_row)
        ws.write(row_num, 4, offer.gcode.kymahieuinq, style_data_row)
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_g1code'}) 
def exportxls_offer(request):
    current_user = request.user
    print (current_user.username)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Offer.xlsx"'
    list_null = []
    df = pd.DataFrame({'STT':list_null,'Gcode':list_null,'Inquiry':list_null,'K?? m?? hi???u':list_null,'????n v???':list_null,'S??? l?????ng':list_null,
    'Supplier':list_null,'Xu???t x???':list_null,'NSX':list_null,'STT in ITB':list_null,'Group in ITB':list_null,'Sale':list_null,
    '????n gi?? mua':list_null,'????n gi?? ch??o':list_null,'Giao d???ch vi??n':list_null,'Ghi Ch??':list_null,'Result':list_null})
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
    list_column_fm_float = ['S??? l?????ng','????n gi?? mua','????n gi?? ch??o']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    #worksheet.set_column('F:F', None, fm_float)
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
        username = request.user.username
    Unit_list=['Set','Pcs']
    worksheet.data_validation(0,4,100,4, {'validate': 'list',
                                 'source': Unit_list})
    """ worksheet.data_validation(0,4,100,4, {'validate': 'integer',
                                  'criteria': 'between',
                                  'minimum': 1,
                                  'maximum': 100,
                                  'input_title': 'Enter an integer:',
                                  'input_message': 'between 1 and 100'}) """
    writer.save()
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.add_nhaplieuban'}) 
def exportxls_nlb(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Nhaplieuban.xlsx"'
    df = pd.DataFrame(columns=['Stt','Gcode','Contract No.','Description','MNF','Unit','Quantity b??n',
    'Unit price (VND)','Ext Price (VND)','GDV'])  
    """ g1code_list = G1code.objects.filter(inquiry__pk=id,resultinq = "Win")
    stt = 1
    for item in g1code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Inquiry':[item.inquiry.inquirycode],'Gcode':[item.gcode.ma],'M?? t???':[item.gcode.mota],'K?? m?? hi???u':[item.gcode.kymahieuinq],
        '????n v???':[item.unitinq],'S??? l?????ng':[item.qtyinq],'????n gi?? ch??o':[item.dongiachaoinq],'Supplier':[item.supplier.suppliercode],
        'STT in ITB':[item.sttitb],'Group in ITB':[item.groupitb],'Xu???t x???':[item.xuatxuinq],'NSX':[item.nsxinq]}))
        stt +=1 """
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Nh???p li???u b??n', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Nh???p li???u b??n']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['Quantity b??n','Unit price (VND)','Ext Price (VND)']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_unit = []
    for item in Unit.objects.all():
        list_unit.append(item.unit) 
    unit_col = df.columns.get_loc('Unit')
    worksheet.data_validation(0,unit_col,100,unit_col,{'validate': 'list',
                                 'source': list_unit})
    list_gdv = []
    for item in GDV.objects.all():
        list_gdv.append(item.gdvcode) 
    gdv_col = df.columns.get_loc('GDV')
    worksheet.data_validation(0,gdv_col,100,gdv_col,{'validate': 'list',
                                 'source': list_gdv})
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    for column in range(2, 101):
        cell_location = 'I{0}'.format(column)
        formula = '=IF($G{0}*$H{0}=0,"",$G{0}*$H{0})'.format(column)
        worksheet.write_formula(cell_location, formula, float_format)

    writer.save()
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_all_g2code'}) 
def exportxls_nlb_all(request,id):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Gcode-Contract.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Gcode-Contract')
    row_num = 0  
    columns = ['ID','Gcode-Contract', 'Contract No.','????n gi?? ch??o','PO No.','Status','Gcode-Inquiry','Ghi ch??','Giao d???ch vi??n','Ng??y c???p nh???t']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for g2code_ in Nhaplieuban.objects.all():
        row_num += 1
        ws.write(row_num, 0, g2code_.id, style_data_row)
        ws.write(row_num, 1, "", style_data_row)
        ws.write(row_num, 2, "", style_data_row)
        ws.write(row_num, 3, g2code_.dongiachaonlb, style_number_row)
        ws.write(row_num, 4, "", style_data_row)
        ws.write(row_num, 5, "Ch??a ?????t", style_data_row)
        ws.write(row_num, 6, g2code_.g1code.g1code, style_data_row)
        ws.write(row_num, 7, "", style_data_row)
        ws.write(row_num, 8, "", style_data_row)
        ws.write(row_num, 9, date.today(), style_date_row)
    wb.save(response)
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_all_nlm'}) 
def exportxls_nlm_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Po.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Purchase Order')
    row_num = 0  
    columns = ['ID','Gcode-Contract', 'M?? t???','K?? hi???u m??','????n v???','S??? l?????ng','Supplier','Xu???t x???','NSX','????n gi?? mua','Ghi ch??','Giao d???ch vi??n','Ng??y c???p nh???t']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for g2code_ in Nhaplieumua.objects.all():
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_nlm'}) 
def exportxls_nlm(request,contractid):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Nhaplieumua.xlsx"'
    df = pd.DataFrame(columns=['STT','Gcode','PO No.','Contract No.','GDV',
    'Supplier','Ng??y k?? PO','Delivery term','Qu???c gia xu???t kh???u','Deadline h??ng c?? m???t t???i kho Vam',
    'PAMH','Ng??y thanh to??n ?????t 1','S??? ti???n thanh to??n ?????t 1 (currency bao g???m VAT / GST)',
    'Ng??y thanh to??n ?????t 2','S??? ti???n thanh to??n ?????t 2 (currency bao g???m VAT / GST)','Ng??y thanh to??n ?????t n',	
    'S??? ti???n thanh to??n ?????t n (currency bao g???m VAT / GST)','Description','MNF','Origin','Part number',
    'Unit','Quantity mua','Currency','Unit pirce (currency)','Ext Price (currency)',
    'Thu??? VAT / GST (currency)','Certificate','????nh gi?? Gcode','L?? do h??ng tr??? so v???i deadline',	
    'Chi ti???t r???i ro k??? thu???t','V???n ????? kh?? kh??n','?? ki???n c???a Pal','?? ki???n c???a Sales',
    'T??nh tr???ng gi???i quy???t kh?? kh??n','Ng??y k?? PO (plan)','Budget (VND)'])

    g2code_list = Nhaplieuban.objects.filter(contractno=contractid)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[item.contractno.contractcode],'Gcode':[item.gcodeban],
        'Description':[item.descriptionban],'Unit':[item.unitban],'Quantity mua':[item.qtyban]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Nhaplieumua', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Nhaplieumua']
    #Format header 
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#4788F9','font_color': 'white','border': 1})
    noedit_format =workbook.add_format({'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center',
    'fg_color': '#FC7575','font_color': 'white','border': 1})
    text_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1})
    float_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': '#,##0.00'})
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,'num_format': 'dd/mm/yyyy'})
    list_header_noedit = ['Contract No.','Gcode']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_gdv = []
    for item in GDV.objects.all():
        list_gdv.append(item.gdvcode) 
    gdv_col = df.columns.get_loc('GDV')
    worksheet.data_validation(0,gdv_col,100,gdv_col,{'validate': 'list','source': list_gdv})
    list_pamh = []
    for item in PAMHop.objects.all():
        list_pamh.append(item.pamhop) 
    pamh_col = df.columns.get_loc('PAMH')
    worksheet.data_validation(0,pamh_col,100,pamh_col,{'validate': 'list','source': list_pamh})
    list_unit = []
    for item in Unit.objects.all():
        list_unit.append(item.unit) 
    unit_col = df.columns.get_loc('Unit')
    worksheet.data_validation(0,unit_col,100,unit_col,{'validate': 'list','source': list_unit})
    list_dggcode = []
    for item in Danhgiagcode.objects.all():
        list_dggcode.append(item.danhgiagcode) 
    dggcode_col = df.columns.get_loc('????nh gi?? Gcode')
    worksheet.data_validation(0,dggcode_col,100,dggcode_col,{'validate': 'list','source': list_dggcode})
    list_ttgqkk = []
    for item in Tinhtrangiaiquyetkhokhan.objects.all():
        list_ttgqkk.append(item.ttgqkk) 
    ttgqkk_col = df.columns.get_loc('T??nh tr???ng gi???i quy???t kh?? kh??n')
    worksheet.data_validation(0,ttgqkk_col,100,ttgqkk_col,{'validate': 'list','source': list_ttgqkk})

    list_column_fm_float = ['S??? ti???n thanh to??n ?????t 1 (currency bao g???m VAT / GST)','S??? ti???n thanh to??n ?????t 2 (currency bao g???m VAT / GST)',
    'S??? ti???n thanh to??n ?????t n (currency bao g???m VAT / GST)','Quantity mua','Currency','Unit pirce (currency)',
    'Ext Price (currency)','Thu??? VAT / GST (currency)','Budget (VND)']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Ng??y k?? PO','Deadline h??ng c?? m???t t???i kho Vam','Ng??y thanh to??n ?????t 1','Ng??y thanh to??n ?????t 2',
    'Ng??y thanh to??n ?????t n','Ng??y k?? PO (plan)']
    list_index_fm_date = []
    for item in list_column_fm_date:
        list_index_fm_date.append(df.columns.get_loc(item))

    #worksheet.set_column('F:F', None, fm_float)
    for col in range(0,len(df.columns)):
        if col in list_index_fm_float:
            worksheet.set_column(col,col, None, float_format)
        elif col in list_index_fm_date:
            worksheet.set_column(col,col, None, date_format)
        else:
            worksheet.set_column(col,col, None, text_format)
    for column in range(2, 101):
        cell_location = 'Z{0}'.format(column)
        formula = '=IF($W{0}*$Y{0}=0,"",$W{0}*$Y{0})'.format(column)
        worksheet.write_formula(cell_location, formula, float_format)
    writer.save()
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_warehouse'}) 
def exportxls_nlnk(request,po):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Nhapkho.xlsx"'
    df = pd.DataFrame(columns=['STT','PO No.','Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???','S??? l?????ng',
    '????n gi?? freight','Ng??y h??ng v??? kho','Ghi Ch??','Giao d???ch vi??n'])
    nlm_list = Nhaplieumua.objects.filter(g2code__nlbno=po)
    stt = 1
    for item in nlm_list:
        df = df.append(pd.DataFrame({'STT':[stt],'PO No.':[po],'Contract No.':[item.g2code.contract.contractcode],'Gcode':[item.gcode],
        'M?? t???':[item.motapo],'K?? m?? hi???u':[item.kymahieupo],'????n v???':[item.unitpo],'S??? l?????ng':[item.g2code.qtychuanhapkho]}))
        stt +=1
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Nh???p kho', startrow=1, header=False,index=False)
    workbook  = writer.book
    worksheet = writer.sheets['Nh???p kho']
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
    list_header_noedit = ['PO No.','Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['S??? l?????ng','????n gi?? freight']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Ng??y h??ng v??? kho']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_delivery'}) 
def exportxls_giaohang(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Delivery.xlsx"'
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???','S??? l?????ng',
    'Ng??y giao h??ng','Ghi Ch??','Giao d???ch vi??n'])

    g2code_list = Nhaplieunhapkhau.objects.filter(g2code__contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],
        'M?? t???':[item.mota],'K?? m?? hi???u':[item.kymahieu],'????n v???':[item.unit],'S??? l?????ng':[item.g2code.qtychuagiao]}))
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
    list_header_noedit = ['Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['S??? l?????ng']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))
    list_column_fm_date = ['Ng??y giao h??ng']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_punishment'}) 
def exportxls_phat(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Punishment.xlsx"'
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???','S??? l?????ng',
    'T???ng ph???t','L?? do ph???t','Ghi Ch??','Giao d???ch vi??n'])
    g2code_list = Nhaplieunhapkhau.objects.filter(g2code__contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],
        'M?? t???':[item.mota],'K?? m?? hi???u':[item.kymahieu],'????n v???':[item.unit],'S??? l?????ng':[item.qtygiaohang]}))
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
    list_header_noedit = ['Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['S??? l?????ng','T???ng ph???t']
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_accounting'}) 
def exportxls_tienve(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Accounting.xlsx"'
    df = pd.DataFrame(columns=['STT','PO No.','Contract No.','Client','Gcode','M?? t???','K?? m?? hi???u','????n v???',
    'NSX','Xu???t x???','Supplier','S??? l?????ng','????n gi?? ti???n v???','Th??nh ti???n','Ghi Ch??'])
    g2code_list = Nhaplieuban.objects.filter(contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        df = df.append(pd.DataFrame({'STT':[stt],'PO No.':[item.pono],'Contract No.':[contract],'Client':[item.contract.client.clientcode],
        'Gcode':[item.gcode],'M?? t???':[item.mota],'K?? m?? hi???u':[item.kymahieu],'????n v???':[item.unit],
        'S??? l?????ng':[item.qty],'????n gi?? ti???n v???':[item.dongiachaonlb],'NSX':[item.nsx],'Xu???t x???':[item.xuatxu],'Supplier':[item.supplier]}))
        stt +=1
    df['Th??nh ti???n']= df['S??? l?????ng']*df['????n gi?? ti???n v???']
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
    list_header_noedit = ['PO No.','Contract No.','Client','Gcode','M?? t???','K?? m?? hi???u','????n v???',
    'NSX','Xu???t x???','Supplier']
    list_index_fm_noedit = []
    for item in list_header_noedit:
        list_index_fm_noedit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_noedit:
            worksheet.write(0, col_num, value, noedit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['S??? l?????ng','????n gi?? ti???n v???','Th??nh ti???n']
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_sales'}) 
def exportxls_sales(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales')
    row_num = 0  
    columns = ['ID','T??n vi???t t???t', 'T??n ?????y ?????']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_head_row)
    for sales in Sales.objects.all():
        row_num += 1
        ws.write(row_num, 0, sales.id, style_data_row)
        ws.write(row_num, 1, sales.salescode, style_data_row)
        ws.write(row_num, 2, sales.fullname, style_data_row)
    wb.save(response)
    return response

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_profit'}) 
def exportxls_profit(request,contract):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Profit.xlsx"'
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','M?? t???','K?? m?? hi???u','????n v???','NSX','Xu???t x???','Supplier','S??? l?????ng b??n',
    'S??? l?????ng mua','S??? l?????ng nh???p kho','S??? l?????ng giao','S??? l?????ng ph???t','????n gi?? b??n',
    '????n gi?? mua offer','????n gi?? mua PO' ,'????n gi?? freight','T???ng ph???t',
    'L???i nhu???n ch??a ?????t h??ng','L???i nhu???n ch??a v??? kho','L???i nhu???n ch??a giao h??ng','L???i nhu???n th???c t???',
    'L???i nhu???n t???ng','Ti???n v??? th???c t???','Ti???n v??? d??? ki???n'])
    g2code_list = Nhaplieuban.objects.filter(contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        lncdh = item.qtychuadat*(item.dongiachaonlb-item.dongiamuainq)
        lncvk = item.qtychuanhapkho*(item.dongiachaonlb-item.dongiamuapo)
        lncgh = item.qtychuagiao*(item.dongiachaonlb-item.dongiamuapo-item.dongiafreight)
        lntt = item.qtygiaohang*(item.dongiachaonlb-item.dongiamuapo-item.dongiafreight)-item.tongphat
        lntong = lncdh+lncgh+lncvk+lntt
        tvdk = item.qty*item.dongiachaonlb-item.tongphat-item.tongtienve

        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],'M?? t???':[item.mota],
        'K?? m?? hi???u':[item.kymahieu],'????n v???':[item.unit],'NSX':[item.nsx],'Xu???t x???':[item.xuatxu],'Supplier':[item.supplier],
        'S??? l?????ng b??n':[item.qty],'S??? l?????ng mua':[item.qtypo],'S??? l?????ng nh???p kho':[item.qtykho],
        'S??? l?????ng giao':[item.qtygiaohang],'S??? l?????ng ph???t':[item.qtyphat],'????n gi?? b??n':[item.dongiachaonlb],
        '????n gi?? mua offer':[item.dongiamuainq],'????n gi?? mua PO':[item.dongiamuapo] ,'????n gi?? freight':[item.dongiafreight],
        'T???ng ph???t':[item.tongphat],'L???i nhu???n ch??a ?????t h??ng':[lncdh],'L???i nhu???n ch??a v??? kho':[lncvk],
        'L???i nhu???n ch??a giao h??ng':[lncgh],'L???i nhu???n th???c t???':[lntt],
        'L???i nhu???n t???ng':[lntong],'Ti???n v??? th???c t???':[item.tongtienve],'Ti???n v??? d??? ki???n':[tvdk]}))
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
    list_header_profit = ['L???i nhu???n ch??a ?????t h??ng','L???i nhu???n ch??a v??? kho','L???i nhu???n ch??a giao h??ng','L???i nhu???n th???c t???',
    'L???i nhu???n t???ng','Ti???n v??? th???c t???','Ti???n v??? d??? ki???n']
    list_index_fm_profit = []
    for item in list_header_profit:
        list_index_fm_profit.append(df.columns.get_loc(item))
    for col_num, value in enumerate(df.columns.values):
        if col_num in list_index_fm_profit:
            worksheet.write(0, col_num, value, profit_format)
        else:
            worksheet.write(0, col_num, value, header_format)
            
    # Add some cell formats.
    list_column_fm_float = ['S??? l?????ng b??n',
    'S??? l?????ng mua','S??? l?????ng nh???p kho','S??? l?????ng giao','S??? l?????ng ph???t','????n gi?? b??n',
    '????n gi?? mua offer','????n gi?? mua PO' ,'????n gi?? freight','T???ng ph???t',
    'L???i nhu???n ch??a ?????t h??ng','L???i nhu???n ch??a v??? kho','L???i nhu???n ch??a giao h??ng','L???i nhu???n th???c t???',
    'L???i nhu???n t???ng','Ti???n v??? th???c t???','Ti???n v??? d??? ki???n']
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.export_scanorder'}) 
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
        df.loc[index,'Kh??ch h??ng'] = g1code.inquiry.client.clientcode
        df.loc[index,'M?? t???'] = g1code.gcode.mota
        df.loc[index,'K?? m?? hi???u'] = g1code.gcode.kymahieuinq
        df.loc[index,'????n v???'] = g1code.unitinq
        df.loc[index,'S??? l?????ng'] = g1code.qtyinq
        df.loc[index,'NSX'] = g1code.nsxinq
        df.loc[index,'Xu???t x???'] = g1code.xuatxuinq
        df.loc[index,'Supplier'] = g1code.supplier.suppliercode
        df.loc[index,'????n gi?? mua'] = g1code.dongiamuainq
        df.loc[index,'Th??nh ti???n mua'] = g1code.dongiamuainq * g1code.qtyinq
        df.loc[index,'Ng??y submit th???u'] = g1code.inquiry.datesubmitbid
        df.loc[index,'????n gi?? ch??o'] = g1code.dongiachaoinq
        df.loc[index,'Th??nh ti???n ch??o'] = g1code.dongiachaoinq * g1code.qtyinq
        df.loc[index,'H??? s??? mark up'] = g1code.markupinq
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
    date_format = workbook.add_format({'text_wrap': True,'valign': 'vcenter','align': 'center','border': 1,
    'num_format': 'dd/mm/yyyy'})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    # Add some cell formats.
    list_column_fm_float = ['S??? l?????ng','????n gi?? mua','Th??nh ti???n mua','????n gi?? ch??o','Th??nh ti???n ch??o','H??? s??? mark up']
    list_index_fm_float = []
    for item in list_column_fm_float:
        list_index_fm_float.append(df.columns.get_loc(item))

    list_column_fm_date = ['Ng??y submit th???u']
    list_index_fm_date = []
    for item in list_column_fm_date:
        list_index_fm_date.append(df.columns.get_loc(item))
    for col in range(0,len(df.columns)):
        for r in range(1,df.shape[0]+1):
            if col in list_index_fm_float:
                worksheet.write(r,col, df.iloc[r-1,col], float_format)
            elif col in list_index_fm_date:
                worksheet.write(r,col, df.iloc[r-1,col], date_format)
            else:
                worksheet.write(r,col, df.iloc[r-1,col], text_format)
    writer.save()
    return response