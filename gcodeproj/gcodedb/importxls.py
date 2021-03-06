from datetime import date
from .forms import MyForm
from os import replace
from re import split
from numpy import NAN, NaN, empty, result_type
from pandas._libs.tslibs import NaT
from pandas.core.dtypes.missing import isnull
from pandas.core.frame import DataFrame
import xlrd
from .models import Contract, G1code, Nhaplieuban, GDV,Gcode,Inquiry,Client,Nhaplieunhapkhau,Nhaplieumua,Phat,Supplier,Lydowin,Lydoout,Sales, Tienve,ScanOrder,Danhgiagcode, Yearcode,Unit
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
            message = format_html("Data Import is empty at <b>index Stt {}: column {}</b>",df.loc[i,'Stt'],list_column_required[j])
            messages_.append(message)
    else:
        if len(list_column_float):
            if any(df[item].dtype == "object" for item in list_column_float):
                for item in list_column_float:
                    for i1,i2 in zip(df['Stt'],df[item].map(type)):
                        if i2!=int and i2!=float:
                            message = format_html("Data Import is formated wrong at <b>index Stt {}: column {}</b>",i1,item)
                            messages_.append(message) 
        if len(list_column_date):
            for item in list_column_date:
                for i in range(0,df.shape[0]):
                    if pd.isnull(df[item][i]) == False:
                        df[item][i] = pd.to_datetime(df[item][i], format='%Y-%m-%d', errors='coerce')
                        if df[item][i] is pd.NaT:
                            message = format_html("Datapd Import is formated wrong at <b>index Stt {}: column {}</b>",df['Stt'][i],item)
                            messages_.append(message)
    if len(messages_)<=0:
        for item in list_column_float:
            for i in range(0,df.shape[0]):
                if df[item][i] <= 0:
                    message = format_html("Datapd Import shall be greater than 0 at <b>index Stt {}: column {}</b>",df['Stt'][i],item)
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
            list_column = ['Stt','Gcode','Part number','Description','Markup ?????nh m???c']
            list_column_required = ['Stt','Description']
            list_column_float = ['Markup ?????nh m???c']
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float))
            df[['Gcode','Part number']] = (
                df[['Gcode','Part number']].fillna(0)
                .astype(int, errors = 'ignore')
                .astype(object)
                .where(df[['Gcode','Part number']].notnull())
            )
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.astype(str).str.strip())
                df1 = df.loc[lambda df: df['Part number']!='nan', :]
                df2 = df.loc[lambda df: df['Part number']=='nan', :]
                df2.reset_index(drop=True,inplace= True)
                duplicateRowsDF = df1[df1.duplicated(subset=['Part number'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    if df2.shape[0]>1:
                        for x in range(0,df2.shape[0]-1):
                            for y in range(x+1,df2.shape[0]):
                                str1 = df2.loc[x,'Description']
                                str2 = df2.loc[y,'Description']
                                specialChars = "!#$%^&*().@~?<>+-,~`'" 
                                for specialChar in specialChars:
                                    str1 = str1.replace(specialChar,' ')
                                    str2 = str2.replace(specialChar,' ')
                                resultcheck = fuzz.token_sort_ratio(str1,str2)
                                if resultcheck == 100:
                                    message = format_html("Description is duplicate at <b>index Stt {} & {}</b><br>",df2.loc[x,'Stt'],df2.loc[y,'Stt'])
                                    messages_.append(message)         
            if len(messages_) <=0:
                for i in range(0,df.shape[0]):
                    if df.loc[i,'Gcode']!='nan':
                        if Gcode.objects.filter(gcode__contains=df.loc[i,'Gcode']).count()>0:
                            result_list = Gcode.objects.filter(gcode__contains=df.loc[i,'Gcode']).values_list('gcode', flat=True)
                            df_kmh = pd.DataFrame(columns=['Gcode','Part number','Description'])
                            for item in result_list:
                                gcode_ = Gcode.objects.get(gcode=item)
                                df_kmh = df_kmh.append(pd.DataFrame({'Gcode':[gcode_.gcode],'Part number':[gcode_.PNban],'Description':[gcode_.mota]}))
                            html_1 = df_kmh.to_html(index=False,justify='center')
                            displaydf = "Gcode {} is existed at <b>index Stt {}</b><br>" + html_1
                            message = format_html(displaydf,df.loc[i,'Gcode'],df.loc[i,'Stt'])
                            messages_.append(message)
                    elif df.loc[i,'Part number']!='nan':
                        if (Gcode.objects.filter(PNban__contains=df.loc[i,'Part number']).count()>0) :
                            timPNban = Gcode.objects.filter(PNban__contains=df.loc[i,'Part number']).values_list('gcode', flat=True)
                            #timPNmua = Gcode.objects.filter(PNmua__contains=df.loc[i,'Part number']).values_list('gcode', flat=True)
                            df_kmh = pd.DataFrame(columns=['Gcode','Part number','Description'])
                            for item in timPNban:
                                gcode_ = Gcode.objects.get(gcode=item)
                                df_kmh = df_kmh.append(pd.DataFrame({'Gcode':[gcode_.gcode],'Part number':[gcode_.PNban],'Description':[gcode_.descriptionban]}))
                            html_1 = df_kmh.to_html(index=False,justify='center')
                            displaydf = "Gcode has 'k?? m?? hi???u'{} is existed at <b>index Stt {}</b><br>" + html_1
                            message = format_html(displaydf,df.loc[i,'Part number'],df.loc[i,'Stt'])
                            messages_.append(message)
                    else:
                        list_mota = Gcode.objects.values_list('descriptionban',flat=True)
                        df_kmh = pd.DataFrame(columns=['Gcode','Part number','Description'])
                        if len(list_mota) > 0:
                            for item in list_mota:
                                str_search = df.loc[i,'Description']
                                txtmota = item 
                                specialChars = "!#$%^&*().@~?<>+-,~`" 
                                for specialChar in specialChars:
                                    str_search = str_search.replace(specialChar,' ')
                                    txtmota = txtmota.replace(specialChar,' ')
                                resultcheck = fuzz.token_sort_ratio(str_search,txtmota)
                                if resultcheck == 100:
                                    gcode_ = Gcode.objects.get(descriptionban=item)
                                    df_kmh = df_kmh.append(pd.DataFrame({'Gcode':[gcode_.gcode],'Part number':[gcode_.PNban],'Description':[gcode_.descriptionban]}))
                                    html_1 = df_kmh.to_html(index=False,justify='center')
                                    displaydf = "Description of Gcode is existed at <b>index Stt {}</b><br>" + html_1
                                    message = format_html(displaydf,df.loc[i,'Stt'])
                                    messages_.append(message)                    
            if len(messages_) <=0:
                list_gcode = Gcode.objects.values_list('gcode',flat=True)
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
                    if df.loc[r,'Part number']!='nan':
                        kmh = df.loc[r,'Part number']
                    if pd.isnull(df.loc[r,'Markup ?????nh m???c'])==False:
                        markup = df.loc[r,'Markup ?????nh m???c']
                    gcode_temp = Gcode(
                        gcode=df.loc[r,'Gcode'],
                        PNban=kmh,
                        descriptionban=df.loc[r,'Description'],
                        markupdinhmuc=markup,
                        ngaywin = ngaywin,
                        ngayout = ngayout
                        )
                    gcode_temp.save() 
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
def importxls_contract(request):
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
            list_column = ['Stt','Contract No.', 'Contract No. (Client)', 'Ng??y k?? k???t','Kh??ch h??ng',
    'Sales','Deadline giao h??ng NLB','Deadline giao h??ng NLM','Gi?? b??n','Tr???ng th??i','Ng??y giao h??ng cu???i c??ng']
            list_column_required = ['Stt','Contract No.', 'Ng??y k?? k???t','Kh??ch h??ng',
    'Sales','Deadline giao h??ng NLB']            
            list_column_float = ['Gi?? b??n']
            list_column_date = ['Ng??y k?? k???t','Deadline giao h??ng NLB','Deadline giao h??ng NLM','Ng??y giao h??ng cu???i c??ng']
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    noclient = set()
                    nosale = set()
                    for index,row in df.iterrows():
                        if Client.objects.filter(clientcode=row['Kh??ch h??ng']).count()<=0:
                            noclient.add(row['Kh??ch h??ng'])
                        if Sales.objects.filter(salescode=row['Sales']).count()<=0:
                            nosale.add(row['Sales'])
                        if Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            warning = format_html("Contract '{}' is existed, you shall be update it", row['Contract No.'])
                            warnings.append(warning)
                    if len(nosale)>=0:
                        for item in nosale:
                            message = format_html("Sales '{}' doesn't exist, please contact with administrator to add Sales", item)
                            messages_.append(message)
                    if len(noclient)>=0:
                        for item in noclient:
                            message = format_html("Client '{}' doesn\'t exist, you shall import Client before importing again"
                            " at link: <a href='{}'>Create Client</a>",item,reverse('gcodedb:client_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                for r in range(0, df.shape[0]): 
                    if Contract.objects.filter(contractcode__icontains=df.loc[r,'Contract No.']).count()>0:
                        contract_temp = Contract.objects.get(contractcode__icontains=df.loc[r,'Contract No.'])
                        contract_temp.contractnoclient = df.loc[r,'Contract No. (Client)']
                        contract_temp.datesign = df.loc[r,'Ng??y k?? k???t']
                        contract_temp.client = Client.objects.get(clientcode=df.loc[r,'Kh??ch h??ng'])
                        contract_temp.sales = Sales.objects.get(salescode=df.loc[r,'Sales'])
                        contract_temp.deadlineghnlb = df.loc[r,'Deadline giao h??ng NLB']
                        contract_temp.deadlineghnlm = df.loc[r,'Deadline giao h??ng NLM']
                        contract_temp.sellcost = df.loc[r,'Gi?? b??n']
                        contract_temp.nguoicapnhat = request.user.username
                    else:
                        contract_temp = Contract(
                            contractcode   = df.loc[r,'Contract No.'],
                            contractnoclient  = df.loc[r,'Contract No. (Client)'],
                            datesign   = df.loc[r,'Ng??y k?? k???t'],
                            client = Client.objects.get(clientcode=df.loc[r,'Kh??ch h??ng']),
                            sales = Sales.objects.get(salescode=df.loc[r,'Sales']),
                            deadlineghnlb = df.loc[r,'Deadline giao h??ng NLB'],
                            deadlineghnlm = df.loc[r,'Deadline giao h??ng NLM'],
                            sellcost = df.loc[r,'Gi?? b??n'],
                            status  = "Open",
                            nguoicapnhat = request.user.username,
                            )
                        contract_temp.save()  
                message = format_html("Data Contract has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            html = html.replace('nan','')
            html = html.replace('NaN','')
            html = html.replace('NaT','')
            context = {'contract_list': html,'messages_':messages_,'warnings':warnings}
            return render(request, 'gcodedb/contract_list.html', context)
    context = {'messages_':messages_} 
    return render(request, 'gcodedb/contract_list.html', context)

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
            #df = pd.read_excel(r'C:\Users\IDMD\Desktop\T???ng h???p_1.xls', sheet_name='Offer1')
            list_column = ['Stt','Gcode', 'Inquiry', 'Part number', '????n v???',
            'S??? l?????ng', 'Supplier', 'Xu???t x???', 'NSX', 'Stt in ITB', 'Group in ITB',
            'Sale', '????n gi?? mua', '????n gi?? ch??o', 'Giao d???ch vi??n', 'Ghi Ch??', 'Result']
            list_column_required = ['Stt','Gcode', 'Inquiry', 'Part number', '????n v???',
            'S??? l?????ng', 'Supplier', 'Xu???t x???', 'NSX', 'Stt in ITB', 'Group in ITB',
            'Sale', '????n gi?? mua', '????n gi?? ch??o', 'Giao d???ch vi??n', 'Result']
            list_column_float = ["????n gi?? ch??o","????n gi?? mua","S??? l?????ng"]
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Inquiry'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if G1code.objects.filter(gcode__gcode__icontains=row['Gcode'],inquiry__inquirycode__icontains=row['Inquiry']).count()>0:
                            message = format_html("Gcode-Inquiry '{}-{}' is existed at <b>index Stt {}</b>",row['Gcode'],row['Inquiry'],row['Stt'])
                            messages_.append(message)
                        if Gcode.objects.filter(gcode=row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn\'t exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['Stt'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        if Inquiry.objects.filter(inquirycode=row['Inquiry']).count()<=0:
                            message = format_html("Inquiry '{}' doesn't exist at <b>index Stt {}</b>, you shall import Inquiry before importing again"
                            " at link: <a href='{}'>Create Inquiry</a>",row['Inquiry'],row['Stt'],reverse('gcodedb:inquiry_list'))
                            messages_.append(message)
                        if GDV.objects.filter(gdvcode=row['Giao d???ch vi??n']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index Stt {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao d???ch vi??n'],row['Stt'],reverse('gcodedb:gdv_list'))
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
                #df[['S??? l?????ng','????n gi?? mua','????n gi?? ch??o','Markup']] = df[['S??? l?????ng','????n gi?? mua','????n gi?? ch??o','Markup']].round(decimals=2)
                """ df=df1.style.format({'value':'{:.2f}'}) """
                df['Th??nh ti???n mua'] = df['S??? l?????ng']*df['????n gi?? mua']
                df['Th??nh ti???n ch??o'] = df['S??? l?????ng']*df['????n gi?? ch??o']
                df['Markup'] = df['????n gi?? ch??o']/df['????n gi?? mua']
                for i in range(0,df.shape[0]):
                    df.loc[i,'Gcode-Inquiry'] = str(df.loc[i,'Gcode']) + '-' + df.loc[i,'Inquiry'] 
                for r in range(0, df.shape[0]):
                    g1code = G1code(
                        g1code=df.loc[r,'Gcode-Inquiry'],
                        gcode = Gcode.objects.get(gcode=df.loc[r,'Gcode']),
                        inquiry = Inquiry.objects.get(inquirycode=df.loc[r,'Inquiry']),
                        unitinq = df.loc[r,'????n v???'],
                        qtyinq = df.loc[r,'S??? l?????ng'],
                        supplier = Supplier.objects.get(suppliercode=df.loc[r,'Supplier']),
                        xuatxuinq = df.loc[r,'Xu???t x???'],
                        nsxinq = df.loc[r,'NSX'],
                        sttitb = df.loc[r,'Stt in ITB'],
                        groupitb = df.loc[r,'Group in ITB'],
                        sales = Sales.objects.get(salescode=df.loc[r,'Sale']),
                        dongiamuainq = df.loc[r,'????n gi?? mua'],
                        dongiachaoinq = df.loc[r,'????n gi?? ch??o'],
                        resultinq = df.loc[r,'Result'],
                        ghichu = str(df.loc[r,'Ghi Ch??']),
                        gdvinq = GDV.objects.get(gdvcode = df.loc[r,'Giao d???ch vi??n']),
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
                    gcode = Gcode.objects.get(gcode = df.loc[r,'Gcode'])
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
@allowed_permission(allowed_roles={'gcodedb.add_g2code'})
def importxls_nlb(request):
    messages_=  []
    warnings = []
    if request.method == 'POST':
        try:
            new_persons = request.FILES['myfile']
            df = pd.read_excel(new_persons, sheet_name='Nh???p li???u b??n')
            df['Gcode']=df['Gcode'].astype(str)
        except Exception as e: 
            message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['Stt','Gcode','Contract No.','Description','MNF','Unit','Quantity b??n',
            'Unit price (VND)','Ext Price (VND)','GDV']
            list_column_required = ['Stt','Contract No.','Description',
            'MNF','Unit','Quantity b??n','Unit price (VND)','GDV']            
            list_column_float = ['Quantity b??n','Unit price (VND)']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Description','Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    if Yearcode.objects.count()<=0 or Yearcode.objects.filter(nowyear=date.today().year).count()<=0:
                        message = format_html("Wrong definition for yearcode")
                        messages_.append(message)
                    nocontract = set()
                    nogdv = set()
                    nounit = set()
                    for index,row in df.iterrows():
                        if Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            nocontract.add(row['Contract No.'])
                        elif Nhaplieuban.objects.filter(descriptionban=row['Description'], contractno=Contract.objects.get(contractcode=row['Contract No.'])).count()>0:
                            findgcode = Nhaplieuban.objects.get(descriptionban=row['Description'], contractno=Contract.objects.get(contractcode=row['Contract No.']))
                            df.at[index,'Gcode'] = findgcode.gcodeban
                            warning = format_html("Gcode '{}' is updated <b>index Stt {}</b>",row['Gcode'],row['Stt'])
                            warnings.append(warning)
                        if GDV.objects.filter(gdvcode=row['GDV']).count()<=0:
                            nogdv.add(row['GDV'])
                        if Unit.objects.filter(unit=row['Unit']).count()<=0:
                            nounit.add(row['Unit'])
                    if len(nocontract)>=0:
                        for item in nocontract:
                            message = format_html("Contract '{}' doesn't exist, you shall import Contract before importing again"
                            " at link: <a href='{}'>Create Contract</a>",item,reverse('gcodedb:contract_list'))
                            messages_.append(message)
                    if len(nogdv)>=0:
                        for item in nogdv:
                            message = format_html("GDV '{}' doesn't exist, contact to administrator to add GDV",item)
                            messages_.append(message)
                    if len(nounit)>=0:
                        for item in nounit:
                            message = format_html("Unit '{}' doesn't exist, contact to administrator to add Unit",item)
                            messages_.append(message)
            if len(messages_) <=0:
                list_gcode = Nhaplieuban.objects.values_list('gcodeban',flat=True)
                Lastest_index = 0
                Lastest_gcode = ''
                ny  = date.today().year
                yc = Yearcode.objects.get(nowyear= ny)
                strcheck  = yc.yearcode + '\d\d\d\d\d'
                if len(list_gcode)>0:
                    for i in range(len(list_gcode)-1,0,-1):
                        if bool(re.match(strcheck,list_gcode[i])) == True:
                            Lastest_gcode = list_gcode[i]
                            break
                if Lastest_gcode == '' or len(list_gcode)<=0:
                    Lastest_index = 0
                else:
                    Lastest_index =  int(Lastest_gcode[1:])
                df[list_column_float]= df[list_column_float].astype('float64')
                df['Ext Price (VND)'] = df['Quantity b??n']*df['Unit price (VND)']
                for r in range(0, df.shape[0]): 
                    if Nhaplieuban.objects.filter(descriptionban=df.loc[r,'Description'],contractno=Contract.objects.get(contractcode=df.loc[r,'Contract No.'])).count()>0:
                        g2code = Nhaplieuban.objects.get(descriptionban=df.loc[r,'Description'],contractno=Contract.objects.get(contractcode=df.loc[r,'Contract No.']))
                        g2code.dongiachaohdb = df.loc[r,'Unit price (VND)']
                        g2code.MNFban = df.loc[r,'MNF']
                        g2code.qtyban = df.loc[r,'Quantity b??n']
                        g2code.unitban = Unit.objects.get(unit=df.loc[r,'Unit'])
                        g2code.gdvhdb = GDV.objects.get(gdvcode=df.loc[r,'GDV'])
                        g2code.nguoicapnhat = request.user.username
                        g2code.dateupdate = date.today()
                        df.at[r,'Gcode'] = g2code.gcodeban
                    else:
                        g2code = Nhaplieuban(
                            gcodeban = yc.yearcode + "{:05n}".format(Lastest_index+1),
                            contractno = Contract.objects.get(contractcode = df.loc[r,'Contract No.']),
                            dongiachaohdb = df.loc[r,'Unit price (VND)'],
                            descriptionban = df.loc[r,'Description'],
                            MNFban = df.loc[r,'MNF'],
                            qtyban = df.loc[r,'Quantity b??n'],
                            unitban = Unit.objects.get(unit=df.loc[r,'Unit']),
                            gdvhdb = GDV.objects.get(gdvcode=df.loc[r,'GDV']),
                            nguoicapnhat = request.user.username,
                            dateupdate = date.today(),
                            )
                        Lastest_index+=1
                        g2code.save()
                        df.at[r,'Gcode'] = g2code.gcodeban
                          
                message = format_html("Data Contract has been successfully import")
                messages_.append(message)
            html = df.to_html(index=False,justify='center')
            html = html.replace('nan','')
            html = html.replace('NaN','')
            html = html.replace('NaT','')
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
            list_column = ['STT','Gcode','PO No.','Contract No.','GDV',
            'Supplier','Ng??y k?? PO','Delivery term','Qu???c gia xu???t kh???u','Deadline h??ng c?? m???t t???i kho Vam',
            'PAMH','Ng??y thanh to??n ?????t 1','S??? ti???n thanh to??n ?????t 1 (currency bao g???m VAT / GST)',
            'Ng??y thanh to??n ?????t 2','S??? ti???n thanh to??n ?????t 2 (currency bao g???m VAT / GST)','Ng??y thanh to??n ?????t n',	
            'S??? ti???n thanh to??n ?????t n (currency bao g???m VAT / GST)','Description','MNF','Origin','Part number',
            'Unit','Quantity mua','Currency','Unit pirce (currency)',
            'Thu??? VAT / GST (currency)','Certificate','????nh gi?? Gcode','L?? do h??ng tr??? so v???i deadline',	
            'Chi ti???t r???i ro k??? thu???t','V???n ????? kh?? kh??n','?? ki???n c???a Pal','?? ki???n c???a Sales',
            'T??nh tr???ng gi???i quy???t kh?? kh??n','Ng??y k?? PO (plan)','Budget (VND)']
            list_column_required = ['STT','Gcode','PO No.','Contract No.','GDV',
            'Supplier','Ng??y k?? PO','Delivery term','Qu???c gia xu???t kh???u','Deadline h??ng c?? m???t t???i kho Vam',
            'PAMH','Ng??y thanh to??n ?????t 1','S??? ti???n thanh to??n ?????t 1 (currency bao g???m VAT / GST)',
            'Ng??y thanh to??n ?????t 2','S??? ti???n thanh to??n ?????t 2 (currency bao g???m VAT / GST)','Ng??y thanh to??n ?????t n',	
            'S??? ti???n thanh to??n ?????t n (currency bao g???m VAT / GST)','Description','MNF','Origin','Part number',
            'Unit','Quantity mua','Currency','Unit pirce (currency)',
            'Thu??? VAT / GST (currency)','Certificate','????nh gi?? Gcode','L?? do h??ng tr??? so v???i deadline',	
            'Chi ti???t r???i ro k??? thu???t','V???n ????? kh?? kh??n','?? ki???n c???a Pal','?? ki???n c???a Sales',
            'T??nh tr???ng gi???i quy???t kh?? kh??n','Ng??y k?? PO (plan)','Budget (VND)']
            list_column_float = ['S??? ti???n thanh to??n ?????t 1 (currency bao g???m VAT / GST)','S??? ti???n thanh to??n ?????t 2 (currency bao g???m VAT / GST)',
            'S??? ti???n thanh to??n ?????t n (currency bao g???m VAT / GST)','Quantity mua','Unit pirce (currency)','Thu??? VAT / GST (currency)',
            'Budget (VND)']
            list_column_date = ['Ng??y k?? PO','Deadline h??ng c?? m???t t???i kho Vam','Ng??y thanh to??n ?????t 1',
            'Ng??y thanh to??n ?????t 2','Ng??y thanh to??n ?????t n']
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','PO No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(gcode =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['Stt'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['Stt'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(gcodeban=row['Gcode'],contractno__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
                        if Supplier.objects.filter(suppliercode=row['Supplier']).count()<=0:
                            message = format_html("Supplier '{}' doesn't exist at <b>index Stt {}</b>, you shall import Supplier before importing again"
                            " at link: <a href='{}'>Create Supplier</a>",row['Supplier'],row['Stt'],reverse('gcodedb:supplier_list'))
                            messages_.append(message)
                        if GDV.objects.filter(gdvcode=row['GDV']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index Stt {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao d???ch vi??n'],row['Stt'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                df['Ext Price (currency)'] = df['Quantity mua']*df['Unit pirce (currency)']
                for r in range(0, df.shape[0]):
                    if Nhaplieumua.objects.filter(g2code__gcodeban=df.loc[r,'Gcode'],pono=df.loc[r,'PO No.']).count()>0:
                        ????????g2code
????????pono
????????gdvpo??
????????supplier
????????datesignpo
????????deliveryterm
????????qhxk
????????deadlinegatvam
????????pamhvamts
????????nttd1
????????stttd1
????????nttd2
????????stttd2
????????nttdn
????????stttdn
????????descriptionmua
????????MNFmua
????????origin
????????Pnmua
????????unitmua
????????qtymua
????????currency
????????unitprice
????????thueVAT
????????certificate
????????danhgiagcode
????????reasondelay
????????ctrrkt
????????vdkk
????????ykcpal
????????ykcsales
????????ttgqkk
????????datesignpoplan
????????budget
????????nguoicapnhat
????????dateupdate
                        nlm.dateupdate = date.today()
                        nlm.save()
                    else:
                        nlm = Nhaplieumua(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__gcode = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            motapo = df.loc[r,'M?? t???'],
                            kymahieupo = df.loc[r,'Part number'],
                            unitpo =df.loc[r,'????n v???'],
                            qtypo = df.loc[r,'S??? l?????ng'],
                            supplier =Supplier.objects.get(suppliercode = df.loc[r,'Supplier']),
                            xuatxupo = df.loc[r,'Xu???t x???'],
                            nsxpo = df.loc[r,'NSX'],
                            dongiamuapo = df.loc[r,'????n gi?? mua'],
                            ghichu = str(df.loc[r,'Ghi Ch??']),
                            gdvpo = GDV.objects.get(gdvcode=df.loc[r,'Giao d???ch vi??n']),
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
            df = pd.read_excel(new_persons, sheet_name='Nh???p kho')
        except Exception as e: 
            if e == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['Stt','PO No.','Contract No.','Gcode','S??? l?????ng',
            '????n gi?? freight','Ng??y h??ng v??? kho','Ghi Ch??','Giao d???ch vi??n']
            list_column_required = ['Stt','PO No.','Contract No.','Gcode','S??? l?????ng',
            '????n gi?? freight','Ng??y h??ng v??? kho','Giao d???ch vi??n']
            list_column_float = ['S??? l?????ng','????n gi?? freight']
            list_column_date = ['Ng??y h??ng v??? kho']
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','PO No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(gcode =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['Stt'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['Stt'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__gcode=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
                        elif Nhaplieumua.objects.filter(g2code__g1code__gcode__gcode=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                            warn = format_html("Gcode-Contract '{}-{}' doesn't exist in PO detail at <b>index Stt {}</b>, you can import it"
                            " at link: <a href='{}'>Create Gcode in PO</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:nlm_list'))
                            warnings.append(warn)
                        if GDV.objects.filter(gdvcode=row['Giao d???ch vi??n']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index Stt {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao d???ch vi??n'],row['Stt'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                df['Th??nh ti???n freight'] = df['S??? l?????ng']*df['????n gi?? freight']
                for r in range(0, df.shape[0]):
                    if Nhaplieunhapkhau.objects.filter(g2code__g1code__gcode__gcode = df.loc[r,'Gcode'],g2code__contract__contractcode= df.loc[r,'Contract No.']).count()>0:
                        kho = Nhaplieunhapkhau.objects.get(g2code__g1code__gcode__gcode = df.loc[r,'Gcode'],g2code__contract__contractcode= df.loc[r,'Contract No.'])
                        kho.dongiafreight = (df.loc[r,'????n gi?? freight']*df.loc[r,'S??? l?????ng']+kho.qtykho * kho.dongiafreight)/(kho.qtykho + df.loc[r,'S??? l?????ng']),
                        kho.qtykho = kho.qtykho + df.loc[r,'S??? l?????ng'],
                        kho.ngaynhapkho = df.loc[r,'Ng??y h??ng v??? kho'],
                        kho.ghichu = df.loc[r,'Ghi Ch??'],
                        kho.gdvkho = GDV.objects.get(gdvcode=df.loc[r,'Giao d???ch vi??n']),
                        kho.dateupdate = date.today()
                        kho.save()
                    else:
                        kho = Nhaplieunhapkhau(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__gcode = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            qtykho = df.loc[r,'S??? l?????ng'],
                            dongiafreight = df.loc[r,'????n gi?? freight'],
                            ngaynhapkho = df.loc[r,'Ng??y h??ng v??? kho'],
                            ghichu = df.loc[r,'Ghi Ch??'],
                            gdvkho = GDV.objects.get(gdvcode=df.loc[r,'Giao d???ch vi??n']),
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
            df = pd.read_excel(new_persons, sheet_name='Phat')
        except Exception as e: 
            if str(e) == 'myfile':
                message = format_html("No File chosen")
            else:
                message = format_html("Import File Error: {}",e)
            messages_.append(message)
        else:
            list_column = ['Stt','Contract No.','Gcode','S??? l?????ng',
            'T???ng ph???t','L?? do ph???t','Ghi Ch??','Giao d???ch vi??n']
            list_column_required = ['Stt','Contract No.','Gcode','S??? l?????ng',
            'T???ng ph???t','L?? do ph???t','Giao d???ch vi??n']
            list_column_float = ['S??? l?????ng','T???ng ph???t']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(gcode =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['Stt'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['Stt'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__gcode=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
                        else:
                            if Nhaplieumua.objects.filter(g2code__g1code__gcode__gcode=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                                warn = format_html("Gcode-Contract '{}-{}' doesn't exist in PO detail at <b>index Stt {}</b>, you can import it"
                                " at link: <a href='{}'>Create Gcode in PO</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:nlm_list'))
                                warnings.append(warn)
                            if Nhaplieunhapkhau.objects.filter(g2code__g1code__gcode__gcode=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                                warn = format_html("Gcode-Contract '{}-{}' doesn't exist in FREIGHT & WAREHOUSE at <b>index Stt {}</b>, you can import it"
                                " at link: <a href='{}'>Create Gcode in FREIGHT & WAREHOUSE</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:kho_list'))
                                warnings.append(warn)
                            if Nhaplieunhapkhau.objects.filter(g2code__g1code__gcode__gcode=row['Gcode'],g2code__contract__contractcode=row['Contract No.']).count()<=0:
                                warn = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                                " at link: <a href='{}'>Create Gcode in Delivery</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:giaohang_list'))
                                warnings.append(warn)
                        if GDV.objects.filter(gdvcode=row['Giao d???ch vi??n']).count()<=0:
                            message = format_html("Seller '{}' doesn't exist at <b>index Stt {}</b>, you shall import Seller before importing again"
                            " at link: <a href='{}'>Create Seller</a>",row['Giao d???ch vi??n'],row['Stt'],reverse('gcodedb:gdv_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                for r in range(0, df.shape[0]):
                    if Phat.objects.filter(g2code__g1code__gcode__gcode = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.']).count()>0:
                        punishment = Phat.objects.get(g2code__g1code__gcode__gcode = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.'])
                        punishment.qtyphat = punishment.qtyphat + df.loc[r,'S??? l?????ng']
                        punishment.tongphat = punishment.tongphat + df.loc[r,'T???ng ph???t']
                        punishment.lydophat = df.loc[r,'L?? do ph???t']
                        if df.loc[r,'Ghi Ch??'] != "":
                            punishment.ghichu = punishment.ghichu + '\n' + str(df.loc[r,'Ghi Ch??'])
                        punishment.gdvphat = GDV.objects.get(gdvcode=df.loc[r,'Giao d???ch vi??n'])
                        punishment.dateupdate = date.today()
                        punishment.save()
                    else:  
                        punishment = Phat(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__gcode = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            qtyphat = df.loc[r,'S??? l?????ng'],
                            tongphat = df.loc[r,'T???ng ph???t'],
                            lydophat = df.loc[r,'L?? do ph???t'],
                            ghichu = str(df.loc[r,'Ghi Ch??']),
                            gdvphat = GDV.objects.get(gdvcode=df.loc[r,'Giao d???ch vi??n']),
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
            list_column = ['Stt','PO No.','Contract No.','Client','Gcode','M?? t???','Part number','????n v???',
            'NSX','Xu???t x???','Supplier','S??? l?????ng','????n gi?? ti???n v???','Th??nh ti???n','Ghi Ch??']
            list_column_required = ['Stt','Contract No.','Gcode','S??? l?????ng','????n gi?? ti???n v???']
            list_column_float = ['S??? l?????ng','????n gi?? ti???n v???']
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode','Contract No.'],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(gcode =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['Stt'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                        elif Contract.objects.filter(contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Contract '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Contract</a>",row['Contract No.'],row['Stt'],reverse('gcodedb:contractdetail_list'))
                            messages_.append(message)
                        elif Nhaplieuban.objects.filter(g1code__gcode__gcode=row['Gcode'],contract__contractcode=row['Contract No.']).count()<=0:
                            message = format_html("Gcode-Contract '{}-{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing ACCOUNTING again"
                            " at link: <a href='{}'>Create Gcode in Contract</a>",row['Gcode'],row['Contract No.'],row['Stt'],reverse('gcodedb:nlb_list'))
                            messages_.append(message)
            if len(messages_) <=0:
                df[list_column_float]= df[list_column_float].astype('float64')
                for r in range(0, df.shape[0]):
                    if Tienve.objects.filter(g2code__g1code__gcode__gcode = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.']).count()>0:
                        tienve = Phat.objects.get(g2code__g1code__gcode__gcode = df.loc[r,'Gcode'],g2code__contract__contractcode = df.loc[r,'Contract No.'])
                        tienve.qtytienve = df.loc[r,'S??? l?????ng']
                        tienve.dongiatienve = df.loc[r,'????n gi?? ti???n v???']
                        if df.loc[r,'Ghi Ch??']!='':
                            tienve.ghichu = tienve.ghichu + '\n' + str(df.loc[r,'Ghi Ch??'])
                        tienve.save()
                    else:  
                        tienve = Tienve(
                            g2code = Nhaplieuban.objects.get(g1code__gcode__gcode = df.loc[r,'Gcode'],contract__contractcode= df.loc[r,'Contract No.']),
                            qtytienve = df.loc[r,'S??? l?????ng'],
                            dongiatienve = df.loc[r,'????n gi?? ti???n v???'],
                            ghichu = str(df.loc[r,'Ghi Ch??']),
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
    df = pd.DataFrame(columns=['Stt','Contract No.','Gcode','M?? t???','Part number','????n v???','NSX','Xu???t x???','Supplier','S??? l?????ng b??n',
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

        df = df.append(pd.DataFrame({'Stt':[stt],'Contract No.':[contract],'Gcode':[item.gcode],'M?? t???':[item.mota],
        'Part number':[item.kymahieu],'????n v???':[item.unit],'NSX':[item.nsx],'Xu???t x???':[item.xuatxu],'Supplier':[item.supplier],
        'S??? l?????ng b??n':[item.qty],'S??? l?????ng mua':[item.qtypo],'S??? l?????ng nh???p kho':[item.qtykho],
        'S??? l?????ng giao':[item.qtygiaohang],'S??? l?????ng ph???t':[item.qtyphat],'????n gi?? b??n':[item.dongiachaonlb],
        '????n gi?? mua offer':[item.dongiamuainq],'????n gi?? mua PO':[item.dongiamuapo] ,'????n gi?? freight':[item.dongiafreight],
        'T???ng ph???t':[item.tongphat],'L???i nhu???n ch??a ?????t h??ng':[lncdh],'L???i nhu???n ch??a v??? kho':[lncvk],
        'L???i nhu???n ch??a giao h??ng':[lncgh],'L???i nhu???n th???c t???':[lntt],
        'L???i nhu???n t???ng':[lntong],'Ti???n v??? th???c t???':[item.tongtienve],'Ti???n v??? d??? ki???n':[tvdk]}))
        stt +=1
    df.loc['Total']= df.sum(numeric_only=True, axis=0)
    df.loc['Total','Stt']='Total'
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
            list_column = ['Stt','Gcode']
            list_column_required = ['Stt','Gcode']
            list_column_float = []
            list_column_date = []
            messages_.extend(msgcheckimport(df,list_column,list_column_required,list_column_float,list_column_date))
            if len(messages_) <=0:
                df_obj = df.select_dtypes(['object'])
                df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
                duplicateRowsDF = df[df.duplicated(subset=['Gcode',],keep=False)]
                if duplicateRowsDF.shape[0]:
                    message = format_html("Data Import is duplicate at <b>index Stt {}</b>",df.loc[duplicateRowsDF.index.to_list(),'Stt'].tolist())
                    messages_.append(message)
                else:
                    scanorder = ScanOrder()
                    scanorder.save()
                    for index,row in df.iterrows():
                        if Gcode.objects.filter(gcode =row['Gcode']).count()<=0:
                            message = format_html("Gcode '{}' doesn't exist at <b>index Stt {}</b>, you shall import Gcode before importing again"
                            " at link: <a href='{}'>Create Gcode</a>",row['Gcode'],row['Stt'],reverse('gcodedb:gcode_list'))
                            messages_.append(message)
                            df_copy.drop([index],inplace=True)
                        else:
                            g1code = G1code.objects.filter(gcode__gcode=row['Gcode']).order_by('-gcode__ngaywin','-gcode__ngayout')[0]
                            df_copy.loc[index,'Inquiry'] = g1code.inquiry.inquirycode
                            df_copy.loc[index,'Kh??ch h??ng'] = g1code.inquiry.client.clientcode
                            df_copy.loc[index,'M?? t???'] = g1code.gcode.mota
                            df_copy.loc[index,'Part number'] = g1code.gcode.PNban
                            df_copy.loc[index,'????n v???'] = g1code.unitinq
                            df_copy.loc[index,'S??? l?????ng'] = g1code.qtyinq
                            df_copy.loc[index,'NSX'] = g1code.nsxinq
                            df_copy.loc[index,'Xu???t x???'] = g1code.xuatxuinq
                            df_copy.loc[index,'Supplier'] = g1code.supplier.suppliercode
                            df_copy.loc[index,'????n gi?? mua'] = g1code.dongiamuainq
                            df_copy.loc[index,'Th??nh ti???n mua'] = g1code.dongiamuainq * g1code.qtyinq
                            df_copy.loc[index,'Ng??y submit th???u'] = g1code.inquiry.datesubmitbid
                            df_copy.loc[index,'????n gi?? ch??o'] = g1code.dongiachaoinq
                            df_copy.loc[index,'Th??nh ti???n ch??o'] = g1code.dongiachaoinq * g1code.qtyinq
                            df_copy.loc[index,'H??? s??? mark up'] = g1code.markupinq
                            df_copy.loc[index,'Result'] = g1code.resultinq
                            for item in g1code.lydowin.all():
                                df_copy.loc[index,item.lydowincode] = 'Yes'
                            for item in g1code.lydoout.all():
                                df_copy.loc[index,item.lydooutcode] = 'Yes'
                            scanorder.gcode.add(Gcode.objects.get(gcode=row['Gcode']))
                    scanorder.save()
                    df_copy = df_copy.replace({NaN: ''})
                    html = df_copy.to_html(index=False,justify='center')
                    msg = format_html("<a href='{}'>Click to Export Gcode Scan Results</a>",reverse('gcodedb:exportxls_scanorder', args=[scanorder.id]))
                    #msg=format_html("<a href='/'>Click to Export Gcode Scan Results</a>")
                    context = {'scanorder_list': html,'messages_':messages_,'msg':msg}
                    return render(request, 'gcodedb/scanorder_list.html', context)
    context = {'messages_':messages_}
    return render(request, 'gcodedb/scanorder_list.html', context)