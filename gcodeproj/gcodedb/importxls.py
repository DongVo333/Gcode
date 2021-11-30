from datetime import date
from .forms import MyForm
from os import replace
from re import split
from numpy import NAN, NaN, empty, result_type
from pandas._libs.tslibs import NaT
from pandas.core.dtypes.missing import isnull
from pandas.core.frame import DataFrame
import xlrd
from .models import Contract, G1code, Nhaplieuban, GDV,Gcode,Inquiry,Client,Nhaplieunhapkhau,Nhaplieumua,Phat,Supplier,Lydowin,Lydoout,Sales, Tienve,ScanOrder,Danhgiagcode
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
import pandas as pd
import numpy as np
from django.urls import reverse
import json
from django.utils.html import format_html
from fuzzywuzzy import fuzz,process
import re
from django.contrib.auth.decorators import login_required
from .decorators import allowed_permission

pd.options.display.float_format = '{:,.2f}'.format

def readdate(inputdate,workbook):
    if inputdate == "":
        return None
    else:
        return xlrd.xldate.xldate_as_datetime(inputdate,workbook.datemode).strftime("%Y-%m-%d")
def msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date):
    messages_=[]
    if df.empty:
        messages_.append("Data Import is empty! Please re-check again")
    elif not all([item in df.columns for item in list_column]): 
        for item in list_column:
            if not item in df.columns:
                message = format_html("Data Import doesn't has columns <b>{}</b>",item)
                messages_.append(message)
    elif df[list_column_required].isna().sum().sum()>0:
        for i,j in zip(*np.where(pd.isnull(df[list_column_required]))):
            message = format_html("Data Import is empty at <b>index STT {}: column {}</b>",df.loc[i,'STT'],list_column_required[j])
            messages_.append(message)
    else:
        if len(list_column_float):
            if any(df[item].dtype == "object" for item in list_column_float):
                for item in list_column_float:
                    for i1,i2 in zip(df['STT'],df[item].map(type)):
                        if i2!=int and i2!=float:
                            message = format_html("Data Import is formated wrong at <b>index STT {}: column {}</b>",i1,item)
                            messages_.append(message) 
        if len(list_column_date):
            for item in list_column_date:
                for i in range(0,df.shape[0]):
                    if pd.isnull(df[item][i]) == False:
                        df[item][i] = pd.to_datetime(df[item][i], format='%Y-%m-%d', errors='coerce')
                        if df[item][i] is pd.NaT:
                            message = format_html("Datapd Import is formated wrong at <b>index STT {}: column {}</b>",df['STT'][i],item)
                            messages_.append(message)
    if len(messages_)<=0:
        for item in list_column_float:
            for i in range(0,df.shape[0]):
                if df[item][i] <= 0:
                    message = format_html("Datapd Import shall be greater than 0 at <b>index STT {}: column {}</b>",df['STT'][i],item)
                    messages_.append(message)
    return messages_

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_client'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_gcode'})
def importxls_gcode(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            filename = request.FILES['myfile']
            df = pd.read_excel(filename, sheet_name='Gcode')
        except Exception as e: 
            message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','Gcode','Ký mã hiệu','Mô tả','Markup định mức','Ngày Win','Ngày Out']
            list_column_required = ['STT','Mô tả']
            list_column_float = ['Markup định mức']
            list_column_date = ['Ngày Win','Ngày Out']
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            df[['Gcode','Ký mã hiệu']] = (
                df[['Gcode','Ký mã hiệu']].fillna(0)
                .astype(int, errors = 'ignore')
                .astype(object)
                .where(df[['Gcode','Ký mã hiệu']].notnull())
            )
            print(df['Ký mã hiệu'])
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.astype(str).str.strip())
                df1 = df.loc[lambda df: df['Ký mã hiệu']!='nan', :]
                df2 = df.loc[lambda df: df['Ký mã hiệu']=='nan', :]
                df2.reset_index(drop=True,inplace= True)
                duplicateRowsDF = df1[df1.duplicated(subset=['Ký mã hiệu'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    if df2.shape[0]>1:
                        for x in range(0,df2.shape[0]-1):
                            for y in range(x+1,df2.shape[0]):
                                str1 = df2.loc[x,'Mô tả']
                                str2 = df2.loc[y,'Mô tả']
                                specialChars = "!#$%^&*().@~?<>+-,~`'" 
                                for specialChar in specialChars:
                                    str1 = str1.replace(specialChar,' ')
                                    str2 = str2.replace(specialChar,' ')
                                resultcheck = fuzz.token_sort_ratio(str1,str2)
                                if resultcheck == 100:
                                    message = format_html("Description is duplicate at <b>index STT {} & {}</b><br>",df2.loc[x,'STT'],df2.loc[y,'STT'])
                                    messages_.append(message)         
            if len(messages_) <=0:
                for i in range(0,df.shape[0]):
                    if df.loc[i,'Gcode']!='nan':
                        if Gcode.objects.filter(ma__contains=df.loc[i,'Gcode']).count()>0:
                            result_list = Gcode.objects.filter(ma__contains=df.loc[i,'Gcode']).values_list('ma', flat=True)
                            df_kmh = pd.DataFrame(columns=['Gcode','Ký mã hiệu','Mô tả'])
                            for item in result_list:
                                gcode_ = Gcode.objects.get(ma=item)
                                df_kmh = df_kmh.append(pd.DataFrame({'Gcode':[gcode_.ma],'Ký mã hiệu':[gcode_.kymahieuinq],'Mô tả':[gcode_.mota]}))
                            html_1 = df_kmh.to_html(index=False,justify='center')
                            displaydf = "Gcode {} is existed at <b>index STT {}</b><br>" + html_1
                            message = format_html(displaydf,df.loc[i,'Gcode'],df.loc[i,'STT'])
                            messages_.append(message)
                    elif df.loc[i,'Ký mã hiệu']!='nan':
                        if Gcode.objects.filter(kymahieuinq__contains=df.loc[i,'Ký mã hiệu']).count()>0:
                            result_list = Gcode.objects.filter(kymahieuinq__contains=df.loc[i,'Ký mã hiệu']).values_list('ma', flat=True)
                            df_kmh = pd.DataFrame(columns=['Gcode','Ký mã hiệu','Mô tả'])
                            for item in result_list:
                                gcode_ = Gcode.objects.get(ma=item)
                                df_kmh = df_kmh.append(pd.DataFrame({'Gcode':[gcode_.ma],'Ký mã hiệu':[gcode_.kymahieuinq],'Mô tả':[gcode_.mota]}))
                            html_1 = df_kmh.to_html(index=False,justify='center')
                            displaydf = "Gcode has 'ký mã hiệu'{} is existed at <b>index STT {}</b><br>" + html_1
                            message = format_html(displaydf,df.loc[i,'Ký mã hiệu'],df.loc[i,'STT'])
                            messages_.append(message)
                    else:
                        list_mota = Gcode.objects.values_list('mota',flat=True)
                        df_kmh = pd.DataFrame(columns=['Gcode','Ký mã hiệu','Mô tả'])
                        if len(list_mota) > 0:
                            for item in list_mota:
                                str_search = df.loc[i,'Mô tả']
                                txtmota = item 
                                specialChars = "!#$%^&*().@~?<>+-,~`" 
                                for specialChar in specialChars:
                                    str_search = str_search.replace(specialChar,' ')
                                    txtmota = txtmota.replace(specialChar,' ')
                                resultcheck = fuzz.token_sort_ratio(str_search,txtmota)
                                if resultcheck == 100:
                                    gcode_ = Gcode.objects.get(mota=item)
                                    df_kmh = df_kmh.append(pd.DataFrame({'Gcode':[gcode_.ma],'Ký mã hiệu':[gcode_.kymahieuinq],'Mô tả':[gcode_.mota]}))
                                    html_1 = df_kmh.to_html(index=False,justify='center')
                                    displaydf = "Description of Gcode is existed at <b>index STT {}</b><br>" + html_1
                                    message = format_html(displaydf,df.loc[i,'STT'])
                                    messages_.append(message)
            if len(messages_) <=0:
                list_gcode = Gcode.objects.values_list('ma',flat=True)
                Lastest_index = 0
                Lastest_gcode = ''
                if len(list_gcode)>0:
                    for i in range(len(list_gcode),0,-1):
                        if bool(re.match("G\d\d\d\d\d+",list_gcode[i])) == True:
                            Lastest_gcode = list_gcode[i]
                            break
                if Lastest_gcode == '' or len(list_gcode)<=0:
                    Lastest_index = 0
                else:
                    Lastest_index =  int(Lastest_gcode[1:])
                for r in range(0, df.shape[0]):
                    if df.loc[r,'Gcode']=='nan':
                        df.at[r,'Gcode']='G'+ "{:06n}".format(Lastest_index+1)
                        Lastest_index+=1
                for r in range(0, df.shape[0]):
                    ngaywin = None
                    ngayout = None
                    markup = None
                    kmh = None
                    if pd.isnull(df.loc[r,'Ngày Win'])==False:
                        ngaywin = df.loc[r,'Ngày Win']
                    if pd.isnull(df.loc[r,'Ngày Out'])==False:
                        ngayout = df.loc[r,'Ngày Out']
                    if df.loc[r,'Ký mã hiệu']!='nan':
                        kmh = df.loc[r,'Ký mã hiệu']
                    if pd.isnull(df.loc[r,'Markup định mức'])==False:
                        markup = df.loc[r,'Markup định mức']
                    gcode = Gcode(
                        ma=df.loc[r,'Gcode'],
                        kymahieuinq=kmh,
                        mota=df.loc[r,'Mô tả'],
                        markupdinhmuc=markup,
                        ngaywin = ngaywin,
                        ngayout = ngayout
                        )
                    gcode.save() 
                message = format_html("Data Gcode has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            html = html.replace('nan','')
            html = html.replace('NaN','')
            html = html.replace('NaT','')
            context = {'import_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/gcode_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/gcode_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_contract'})
def importxls_contractdetail(request):
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
        return redirect('/contractdetail/')     
    return render(request, 'gcodedb/contractdetail_list.html')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_inquiry'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_gdv'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_supplier'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_reasonwin'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_reasonout'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_g1code'})
def importxls_offer(request):
    messages_=  []
    warnings = []
    myform = MyForm()
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Offer')
        except Exception as e: 
            message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            #df = pd.read_excel(r'C:\Users\IDMD\Desktop\Tổng hợp_1.xls', sheet_name='Offer1')
            list_column = ['STT','Gcode', 'Inquiry', 'Ký mã hiệu', 'Đơn vị',
            'Số lượng', 'Supplier', 'Xuất xứ', 'NSX', 'STT in ITB', 'Group in ITB',
            'Sale', 'Đơn giá mua', 'Đơn giá chào', 'Giao dịch viên', 'Ghi Chú', 'Result']
            list_column_required = ['STT','Gcode', 'Inquiry', 'Ký mã hiệu', 'Đơn vị',
            'Số lượng', 'Supplier', 'Xuất xứ', 'NSX', 'STT in ITB', 'Group in ITB',
            'Sale', 'Đơn giá mua', 'Đơn giá chào', 'Giao dịch viên', 'Result']
            list_column_float = ["Đơn giá chào","Đơn giá mua","Số lượng"]
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Inquiry'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if G1code.objects.filter(gcode__ma__icontains=row['Gcode'],inquiry__inquirycode__icontains=row['Inquiry']).count()>0:
                            message = format_html("Gcode-Inquiry '{}-{}' is existed at <b>index STT {}</b>",row['Gcode'],row['Inquiry'],row['STT'])
                            messages_.append(message)
                        if Gcode.objects.filter(ma=row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn\'t exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['STT'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        if Inquiry.objects.filter(inquirycode=row['Inquiry']).count()<=0:
                            message = format_html("Inquiry '{}' doesn't exist at <b>index STT {}</b>, you shall import Inquiry before importing again"
                            " at link: <a href='{}'>Create Inquiry</a>",row['Inquiry'],row['STT'],reverse('gcodedb:inquiry_list'))
                            messages_.append(message)
                        if GDV.objects.filter(gdvcode=row['Giao dịch viên']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index STT {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao dịch viên'],row['STT'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
                    columnreason = df.columns.get_loc('Result') + 1
                    if not all(df['Result'].isin(['Win','Out'])):
                        message = format_html("The Result of Gcode-Inquiry is only 'Win' or 'Out'")
                        messages_.append(message) 
                    elif not df.iloc[:,columnreason:].isin(['Yes',NaN]).all(axis=None):
                        message = format_html("The Reason is only 'Yes' or None")
                        messages_.append(message)
                    else:
                        df_reason = df.loc[:,'Result':].replace('Yes',1)
                        df_gr = df_reason.groupby(by=["Result"], dropna=False).sum()
                        print (df_gr.iloc[0,0])
                        set_lydowin = {}
                        set_lydoout = {}
                        reason_duplicate = {}
                        if df_gr.shape[0]==1:
                            if df_gr.index[0] == "Win":
                                set_lydowin = set(df_gr.loc[:,df_gr.loc['Win']>0].columns)
                            else:
                                set_lydoout = set(df_gr.loc[:,df_gr.loc['Out']>0].columns)
                        else:
                            set_lydowin = set(df_gr.loc[:,df_gr.loc['Win']>0].columns)
                            set_lydoout = set(df_gr.loc[:,df_gr.loc['Out']>0].columns)
                            reason_duplicate = set_lydowin & set_lydoout
                        if len(reason_duplicate)>0:
                            message = format_html("Reason {} can\'t be use in both cases Result 'Win' and 'Out'",reason_duplicate)
                            messages_.append(message)
                        else:
                            list_lydoout = Lydoout.objects.values_list('lydooutcode',flat=True)
                            list_lydowin = Lydowin.objects.values_list('lydowincode',flat=True)
                            if len(set_lydowin)>0:
                                for setitem in set_lydowin:                                
                                    highest = process.extractOne(setitem,list_lydowin)
                                    if highest[1] < 90:
                                        message = format_html("Reason Win '{}' doesn't exist, you shall import it before importing again"
                                        " at link: <a href='{}'>Create Reason Win</a>",setitem,reverse('gcodedb:lydowin_list'))
                                        messages_.append(message)
                                    elif setitem != highest[0]:
                                        df.rename(columns={setitem: highest[0]}, inplace=True)
                                        warn = format_html("Reason Win '{}' is merged with '{}' in Database",setitem,highest[0])
                                        warnings.append(warn)
                            if len(set_lydoout)>0:
                                for setitem in set_lydoout:
                                    highest = process.extractOne(setitem,list_lydoout)
                                    if highest[1] < 90:
                                        message = format_html("Reason Out '{}' doesn't exist, you shall import it before importing again"
                                        " at link: <a href='{}'>Create Reason Out</a>",setitem,reverse('gcodedb:lydoout_list'))
                                        messages_.append(message)
                                    elif setitem != highest[0]:
                                        df.rename(columns={setitem: highest[0]}, inplace=True)
                                        warn = format_html("Reason Win '{}' is merged with '{}' in Database",setitem,highest[0])
                                        warnings.append(warn)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                #df[['Số lượng','Đơn giá mua','Đơn giá chào','Markup']] = df[['Số lượng','Đơn giá mua','Đơn giá chào','Markup']].round(decimals=2)
                """ df=df1.style.format({'value':'{:.2f}'}) """
                df['Thành tiền mua'] = df['Số lượng']*df['Đơn giá mua']
                df['Thành tiền chào'] = df['Số lượng']*df['Đơn giá chào']
                df['Markup'] = df['Đơn giá chào']/df['Đơn giá mua']
                for i in range(0,df.shape[0]):
                    df.loc[i,'Gcode-Inquiry'] = str(df.loc[i,'Gcode']) + '-' + df.loc[i,'Inquiry'] 
                for r in range(0, df.shape[0]):
                    g1code = G1code(
                        g1code=df.loc[r,'Gcode-Inquiry'],
                        gcode = Gcode.objects.get(ma=df.loc[r,'Gcode']),
                        inquiry = Inquiry.objects.get(inquirycode=df.loc[r,'Inquiry']),
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
                        resultinq = df.loc[r,'Result'],
                        ghichu = str(df.loc[r,'Ghi Chú']),
                        gdvinq = GDV.objects.get(gdvcode = df.loc[r,'Giao dịch viên']),
                        dateupdate = date.today(),
                        )
                    g1code.save()  
                    for i in range(df.columns.get_loc('Result') + 1, len(df.columns)-1):
                        if df.loc[r,'Result']=='Win' and df.iloc[r,i]=="Yes":
                            lydo_ = Lydowin.objects.get(lydowincode=df.columns[i])
                            g1code.lydowin.add(lydo_)
                    for i in range(df.columns.get_loc('Result') + 1, len(df.columns)-1):
                        if df.loc[r,'Result']=='Out' and df.iloc[r,i]=="Yes":
                            lydo_ = Lydoout.objects.get(lydooutcode=df.columns[i])
                            g1code.lydoout.add(lydo_)
                    gcode = Gcode.objects.get(ma = df.loc[r,'Gcode'])
                    if str(df.loc[r,'Result'])=='Win':
                        gcode.ngaywin =  date.today()
                    else: 
                        gcode.ngayout = date.today()
                    gcode.save()
                message = format_html("Data Offer has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            context = {'offer_list': html,'messages_':messages_,'warnings':warnings,'myform':myform}
            return render(request, 'gcodedb/offer_list.html', context)
    context = {'messages_':messages_, 'myform':myform}
    return render(request, 'gcodedb/offer_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_g2code'})
def importxls_nlb(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Contract')
        except Exception as e: 
            message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','Inquiry','Gcode','Contract No.','Số lượng','Đơn giá chào',
            'PO No.','Ghi Chú','Giao dịch viên']
            list_column_required = ['STT','Inquiry','Gcode','Contract No.','Số lượng','Đơn giá chào',
            'PO No.','Giao dịch viên']
            list_column_float = ['Số lượng','Đơn giá chào']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Nhaplieuban.objects.filter(g1code__gcode__ma__icontains=row['Gcode'],contract__contractcode__icontains=row['Contract No.']).count()>0:
                            message = format_html("Gcode-Contract '{}-{}' is existed at <b>index STT {}</b>",row['Gcode'],row['Contract No.'],row['STT'])
                            messages_.append(message)
                        if Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index STT {}</b>, you shall import Contract before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['STT'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        if G1code.objects.filter(gcode__ma=row['Gcode'],inquiry__inquirycode=row['Inquiry']).count()<=0:
                            message = format_html("Offer '{}-{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Offer</a>",row['Gcode'],row['Inquiry'],row['STT'],reverse('gcodedb:offer_list'))
                            messages_.append(message)
                        if GDV.objects.filter(gdvcode=row['Giao dịch viên']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index STT {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao dịch viên'],row['STT'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                df['Thành tiền chào'] = df['Số lượng']*df['Đơn giá chào']
                for i in range(0,df.shape[0]):
                    df.loc[i,'Gcode-Contract'] = str(df.loc[i,'Gcode']) + '-' + df.loc[i,'Contract No.'] 
                for r in range(0, df.shape[0]):
                    g2code = Nhaplieuban(
                        g2code=df.loc[r,'Gcode-Contract'],
                        contract = Contract.objects.get(contractcode = df.loc[r,'Contract No.']),
                        dongiachaonlb = df.loc[r,'Đơn giá chào'],
                        pono  = df.loc[r,'PO No.'],
                        status = "Contract",
                        g1code = G1code.objects.get(gcode__ma=df.loc[r,'Gcode'],inquiry__inquirycode=df.loc[r,'Inquiry']),
                        ghichu = str(df.loc[r,'Ghi Chú']),
                        gdvnlb = GDV.objects.get(gdvcode = df.loc[r,'Giao dịch viên']),
                        dateupdate = date.today(),
                        )
                    g2code.save()  
                message = format_html("Data Contract has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            context = {'nlb_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/nlb_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/nlb_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_nlm'})
def importxls_nlm(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Nhaplieumua')
        except Exception as e: 
            if e == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng','NSX','Xuất xứ',
    'Supplier','Đơn giá mua','Ghi Chú','Giao dịch viên']
            list_column_required = ['STT','PO No.','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','Số lượng','NSX','Xuất xứ',
    'Supplier','Đơn giá mua','Giao dịch viên']
            list_column_float = ['Số lượng','Đơn giá mua']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','PO No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(ma =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['STT'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['STT'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__ma=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
                        if Supplier.objects.filter(suppliercode=row['Supplier']).count()<=0:
                            message = format_html("Supplier '{}' doesn't exist at <b>index STT {}</b>, you shall import Supplier before importing again"
                            " at link: <a href='{}'>Create Supplier</a>",row['Supplier'],row['STT'],reverse('gcodedb:supplier_list'))
                            messages_.append(message)
                        if GDV.objects.filter(gdvcode=row['Giao dịch viên']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index STT {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao dịch viên'],row['STT'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                df['Thành tiền mua'] = df['Số lượng']*df['Đơn giá mua']
                for r in range(0, df.shape[0]):
                    if Nhaplieumua.objects.filter(g2code__g1code__gcode__ma=df.loc[r,'Gcode'],g2code__contract__contractcode=df.loc[r,'Contract No.']).count()>0:
                        nlm = Nhaplieumua.objects.get(g2code__g1code__gcode__ma=df.loc[r,'Gcode'],g2code__contract__contractcode=df.loc[r,'Contract No.'])
                        nlm.motapo = df.loc[r,'Mô tả']
                        nlm.kymahieupo = df.loc[r,'Ký mã hiệu']
                        nlm.unitpo =df.loc[r,'Đơn vị']
                        nlm.dongiamuapo = (df.loc[r,'Đơn giá mua'] * df.loc[r,'Số lượng'] + nlm.dongiamuapo * nlm.qtypo)/(nlm.qtypo + df.loc[r,'Số lượng'])
                        nlm.qtypo = nlm.qtypo + df.loc[r,'Số lượng'],
                        nlm.supplier =Supplier.objects.get(suppliercode = df.loc[r,'Supplier'])
                        nlm.xuatxupo = df.loc[r,'Xuất xứ']
                        nlm.nsxpo = df.loc[r,'NSX']
                        if df.loc[r,'Ghi Chú'] != "":
                            nlm.ghichu = nlm.ghichu + '\n' + str(df.loc[r,'Ghi Chú'])
                        nlm.gdvpo = GDV.objects.get(gdvcode=df.loc[r,'Giao dịch viên'])
                        nlm.dateupdate = date.today()
                        nlm.save()
                    else:
                        nlm = Nhaplieumua(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__ma = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            motapo = df.loc[r,'Mô tả'],
                            kymahieupo = df.loc[r,'Ký mã hiệu'],
                            unitpo =df.loc[r,'Đơn vị'],
                            qtypo = df.loc[r,'Số lượng'],
                            supplier =Supplier.objects.get(suppliercode = df.loc[r,'Supplier']),
                            xuatxupo = df.loc[r,'Xuất xứ'],
                            nsxpo = df.loc[r,'NSX'],
                            dongiamuapo = df.loc[r,'Đơn giá mua'],
                            ghichu = str(df.loc[r,'Ghi Chú']),
                            gdvpo = GDV.objects.get(gdvcode=df.loc[r,'Giao dịch viên']),
                            dateupdate = date.today(),
                            )
                        nlm.save()  
                message = format_html("Data PO has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            context = {'nlm_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/nlm_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/nlm_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_warehouse'})
def importxls_nlnk(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Nhập kho')
        except Exception as e: 
            if e == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','PO No.','Contract No.','Gcode','Số lượng',
            'Đơn giá freight','Ngày hàng về kho','Ghi Chú','Giao dịch viên']
            list_column_required = ['STT','PO No.','Contract No.','Gcode','Số lượng',
            'Đơn giá freight','Ngày hàng về kho','Giao dịch viên']
            list_column_float = ['Số lượng','Đơn giá freight']
            list_column_date = ['Ngày hàng về kho']
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','PO No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(ma =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['STT'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['STT'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__ma=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
                        elif Nhaplieumua.objects.filter(g2code__g1code__gcode__ma=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                            warn = format_html("Gcode-Contract '{}-{}' doesn't exist in PO detail at <b>index STT {}</b>, you can import it"
                            " at link: <a href='{}'>Create Gcode in PO</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:nlm_list'))
                            warnings.append(warn)
                        if GDV.objects.filter(gdvcode=row['Giao dịch viên']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index STT {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao dịch viên'],row['STT'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                df['Thành tiền freight'] = df['Số lượng']*df['Đơn giá freight']
                for r in range(0, df.shape[0]):
                    if Nhaplieunhapkhau.objects.filter(g2code__g1code__gcode__ma = df.loc[r,'Gcode'],g2code__contract__contractcode= df.loc[r,'Contract No.']).count()>0:
                        kho = Nhaplieunhapkhau.objects.get(g2code__g1code__gcode__ma = df.loc[r,'Gcode'],g2code__contract__contractcode= df.loc[r,'Contract No.'])
                        kho.dongiafreight = (df.loc[r,'Đơn giá freight']*df.loc[r,'Số lượng']+kho.qtykho * kho.dongiafreight)/(kho.qtykho + df.loc[r,'Số lượng']),
                        kho.qtykho = kho.qtykho + df.loc[r,'Số lượng'],
                        kho.ngaynhapkho = df.loc[r,'Ngày hàng về kho'],
                        kho.ghichu = df.loc[r,'Ghi Chú'],
                        kho.gdvkho = GDV.objects.get(gdvcode=df.loc[r,'Giao dịch viên']),
                        kho.dateupdate = date.today()
                        kho.save()
                    else:
                        kho = Nhaplieunhapkhau(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__ma = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            qtykho = df.loc[r,'Số lượng'],
                            dongiafreight = df.loc[r,'Đơn giá freight'],
                            ngaynhapkho = df.loc[r,'Ngày hàng về kho'],
                            ghichu = df.loc[r,'Ghi Chú'],
                            gdvkho = GDV.objects.get(gdvcode=df.loc[r,'Giao dịch viên']),
                            dateupdate = date.today(),
                            )
                        kho.save()  
                message = format_html("Data WAREHOUSE receipt has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            context = {'kho_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/kho_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/kho_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_punishment'})
def importxls_phat(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Punishment')
        except Exception as e: 
            if str(e) == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','Contract No.','Gcode','Số lượng',
            'Tổng phạt','Lý do phạt','Ghi Chú','Giao dịch viên']
            list_column_required = ['STT','Contract No.','Gcode','Số lượng',
            'Tổng phạt','Lý do phạt','Giao dịch viên']
            list_column_float = ['Số lượng','Tổng phạt']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(ma =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['STT'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['STT'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__ma=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
                        else:
                            if Nhaplieumua.objects.filter(g2code__g1code__gcode__ma=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                                warn = format_html("Gcode-Contract '{}-{}' doesn't exist in PO detail at <b>index STT {}</b>, you can import it"
                                " at link: <a href='{}'>Create Gcode in PO</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:nlm_list'))
                                warnings.append(warn)
                            if Nhaplieunhapkhau.objects.filter(g2code__g1code__gcode__ma=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                                warn = format_html("Gcode-Contract '{}-{}' doesn't exist in FREIGHT & WAREHOUSE at <b>index STT {}</b>, you can import it"
                                " at link: <a href='{}'>Create Gcode in FREIGHT & WAREHOUSE</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:kho_list'))
                                warnings.append(warn)
                            if Nhaplieunhapkhau.objects.filter(g2code__g1code__gcode__ma=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                                warn = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                                " at link: <a href='{}'>Create Gcode in Delivery</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:giaohang_list'))
                                warnings.append(warn)
                        if GDV.objects.filter(gdvcode=row['Giao dịch viên']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index STT {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao dịch viên'],row['STT'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                for r in range(0, df.shape[0]):
                    if Phat.objects.filter(g2code__g1code__gcode__ma = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.']).count()>0:
                        punishment = Phat.objects.get(g2code__g1code__gcode__ma = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.'])
                        punishment.qtyphat = punishment.qtyphat + df.loc[r,'Số lượng']
                        punishment.tongphat = punishment.tongphat + df.loc[r,'Tổng phạt']
                        punishment.lydophat = df.loc[r,'Lý do phạt']
                        if df.loc[r,'Ghi Chú'] != "":
                            punishment.ghichu = punishment.ghichu + '\n' + str(df.loc[r,'Ghi Chú'])
                        punishment.gdvphat = GDV.objects.get(gdvcode=df.loc[r,'Giao dịch viên'])
                        punishment.dateupdate = date.today()
                        punishment.save()
                    else:  
                        punishment = Phat(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__ma = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            qtyphat = df.loc[r,'Số lượng'],
                            tongphat = df.loc[r,'Tổng phạt'],
                            lydophat = df.loc[r,'Lý do phạt'],
                            ghichu = str(df.loc[r,'Ghi Chú']),
                            gdvphat = GDV.objects.get(gdvcode=df.loc[r,'Giao dịch viên']),
                            dateupdate = date.today(),
                            )
                        punishment.save()
                message = format_html("Data Delivery receipt has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            context = {'phat_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/phat_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/phat_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_accounting'})
def importxls_tienve(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Accounting')
        except Exception as e: 
            if str(e) == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','PO No.','Contract No.','Client','Gcode','Mô tả','Ký mã hiệu','Đơn vị',
            'NSX','Xuất xứ','Supplier','Số lượng','Đơn giá tiền về','Thành tiền','Ghi Chú']
            list_column_required = ['STT','Contract No.','Gcode','Số lượng','Đơn giá tiền về']
            list_column_float = ['Số lượng','Đơn giá tiền về']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(ma =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['STT'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['STT'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__ma=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing ACCOUNTING again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['STT'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                for r in range(0, df.shape[0]):
                    if Tienve.objects.filter(g2code__g1code__gcode__ma = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.']).count()>0:
                        tienve = Phat.objects.get(g2code__g1code__gcode__ma = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.'])
                        tienve.qtytienve = df.loc[r,'Số lượng']
                        tienve.dongiatienve = df.loc[r,'Đơn giá tiền về']
                        if df.loc[r,'Ghi Chú']!='':
                            tienve.ghichu = tienve.ghichu + '\n' + str(df.loc[r,'Ghi Chú'])
                        tienve.save()
                    else:  
                        tienve = Tienve(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__ma = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            qtytienve = df.loc[r,'Số lượng'],
                            dongiatienve = df.loc[r,'Đơn giá tiền về'],
                            ghichu = str(df.loc[r,'Ghi Chú']),
                            )
                        tienve.save()
                message = format_html("Data Delivery receipt has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            context = {'tienve_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/tienve_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/tienve_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.import_sales'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_profit'})
def profit_show(request,contract):
    messages_=  []
    df = pd.DataFrame(columns=['STT','Contract No.','Gcode','Mô tả','Ký mã hiệu','Đơn vị','NSX','Xuất xứ','Supplier','Số lượng bán',
    'Số lượng mua','Số lượng nhập kho','Số lượng giao','Số lượng phạt','Đơn giá bán',
    'Đơn giá mua offer','Đơn giá mua PO' ,'Đơn giá freight','Tổng phạt',
    'Lợi nhuận chưa đặt hàng','Lợi nhuận chưa về kho','Lợi nhuận chưa giao hàng','Lợi nhuận thực tế',
    'Lợi nhuận tổng','Tiền về thực tế','Tiền về dự kiến'])
    g2code_list = Nhaplieuban.objects.filter(contract__contractcode=contract)
    stt = 1
    for item in g2code_list:
        lncdh = item.qtychuadat*(item.dongiachaonlb-item.dongiamuainq)
        lncvk = item.qtychuanhapkho*(item.dongiachaonlb-item.dongiamuapo)
        lncgh = item.qtychuagiao*(item.dongiachaonlb-item.dongiamuapo-item.dongiafreight)
        lntt = item.qtygiaohang*(item.dongiachaonlb-item.dongiamuapo-item.dongiafreight)-item.tongphat
        lntong = lncdh+lncgh+lncvk+lntt
        tvdk = item.qty*item.dongiachaonlb-item.tongphat-item.tongtienve

        df = df.append(pd.DataFrame({'STT':[stt],'Contract No.':[contract],'Gcode':[item.gcode],'Mô tả':[item.mota],
        'Ký mã hiệu':[item.kymahieu],'Đơn vị':[item.unit],'NSX':[item.nsx],'Xuất xứ':[item.xuatxu],'Supplier':[item.supplier],
        'Số lượng bán':[item.qty],'Số lượng mua':[item.qtypo],'Số lượng nhập kho':[item.qtykho],
        'Số lượng giao':[item.qtygiaohang],'Số lượng phạt':[item.qtyphat],'Đơn giá bán':[item.dongiachaonlb],
        'Đơn giá mua offer':[item.dongiamuainq],'Đơn giá mua PO':[item.dongiamuapo] ,'Đơn giá freight':[item.dongiafreight],
        'Tổng phạt':[item.tongphat],'Lợi nhuận chưa đặt hàng':[lncdh],'Lợi nhuận chưa về kho':[lncvk],
        'Lợi nhuận chưa giao hàng':[lncgh],'Lợi nhuận thực tế':[lntt],
        'Lợi nhuận tổng':[lntong],'Tiền về thực tế':[item.tongtienve],'Tiền về dự kiến':[tvdk]}))
        stt +=1
    df.loc['Total']= df.sum(numeric_only=True, axis=0)
    df.loc['Total','STT']='Total'
    df = df.replace({np.nan: ''})
    message = format_html("<a href='{}'>Export report to Excel</a>",reverse('gcodedb:exportxls_profit', args=[contract]))
    messages_.append(message)
    html = df.to_html(index=False,justify='center')
    context = {'messages_':messages_,'profit_list':html}
    return render(request, 'gcodedb/profit_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_scanorder'})
def importxls_scanorder(request):
    messages_=  []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Scan Order')
            df_copy = df.copy()
        except Exception as e: 
            if str(e) == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['STT','Gcode']
            list_column_required = ['STT','Gcode']
            list_column_float = []
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode',],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index STT {}</b>",df.loc[duplicateRowsDF.index.to_list(),'STT'].tolist())
                    messages_.append(message)
                else:
                    scanorder = ScanOrder()
                    scanorder.save()
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(ma =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index STT {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['STT'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                            df_copy.drop([index],inplace=True)
                        else:
                            g1code = G1code.objects.filter(gcode__ma=row['Gcode']).order_by('-gcode__ngaywin','-gcode__ngayout')[0]
                            df_copy.loc[index,'Inquiry'] = g1code.inquiry.inquirycode
                            df_copy.loc[index,'Khách hàng'] = g1code.inquiry.client.clientcode
                            df_copy.loc[index,'Mô tả'] = g1code.gcode.mota
                            df_copy.loc[index,'Ký mã hiệu'] = g1code.gcode.kymahieuinq
                            df_copy.loc[index,'Đơn vị'] = g1code.unitinq
                            df_copy.loc[index,'Số lượng'] = g1code.qtyinq
                            df_copy.loc[index,'NSX'] = g1code.nsxinq
                            df_copy.loc[index,'Xuất xứ'] = g1code.xuatxuinq
                            df_copy.loc[index,'Supplier'] = g1code.supplier.suppliercode
                            df_copy.loc[index,'Đơn giá mua'] = g1code.dongiamuainq
                            df_copy.loc[index,'Thành tiền mua'] = g1code.dongiamuainq * g1code.qtyinq
                            df_copy.loc[index,'Ngày submit thầu'] = g1code.inquiry.datesubmitbid
                            df_copy.loc[index,'Đơn giá chào'] = g1code.dongiachaoinq
                            df_copy.loc[index,'Thành tiền chào'] = g1code.dongiachaoinq * g1code.qtyinq
                            df_copy.loc[index,'Hệ số mark up'] = g1code.markupinq
                            df_copy.loc[index,'Result'] = g1code.resultinq
                            for item in g1code.lydowin.all():
                                df_copy.loc[index,item.lydowincode] = 'Yes'
                            for item in g1code.lydoout.all():
                                df_copy.loc[index,item.lydooutcode] = 'Yes'
                            scanorder.gcode.add(Gcode.objects.get(ma=row['Gcode']))
                    scanorder.save()
                    df_copy = df_copy.replace({NaN: ''})
                    html = df_copy.to_html(index=False,justify='center')
                    msg = format_html("<a href='{}'>Click to Export Gcode Scan Results</a>",reverse('gcodedb:exportxls_scanorder', args=[scanorder.id]))
                    #msg=format_html("<a href='/'>Click to Export Gcode Scan Results</a>")
                    context = {'scanorder_list': html,'messages_':messages_,'msg':msg}
                    return render(request, 'gcodedb/scanorder_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/scanorder_list.html', context)