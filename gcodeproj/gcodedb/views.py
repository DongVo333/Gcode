from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm, formsets, inlineformset_factory,modelformset_factory
from .models import Gcode,Inquiry,Client
from django.db import transaction
from .forms import GcodeForm
from django.contrib import messages
from tablib import Dataset
import csv
import xlwt

""" def list(request):
   Data = {'Gcodes': Gcode.objects.all().order_by('-id')}
   return render(request, 'gcodedb/show.html', Data) """
class PostListView(ListView):
   queryset = Gcode.objects.all().order_by('-ma')
   template_name = 'gcodedb/show.html'
   context_object_name = 'Gcodes'
class PostDetailView(DetailView):
   model = Gcode
   template_name = 'gcodedb/detail.html'
   context_object_name = 'gcodekey'

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="GcodeList.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Gcode', 'Mo ta','Markup dinh muc'])

    users = Gcode.objects.all().values_list('id', 'ma', 'mota','markupdinhmuc')
    for user in users:
        writer.writerow(user)

    return response
def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="GcodeList.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('GcodeList')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'Gcode', 'Mô tả', 'Xuất xứ','Markup dinh muc', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Gcode.objects.all().values_list('id', 'ma', 'mota','markupdinhmuc')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
def savedata(request):
    form = GcodeForm()
    if request.method == 'POST':
        form = GcodeForm(request.POST)
        if form.is_valid():
            counter = Gcode.objects.filter(ma=request.POST.get('ma')).count()
            if counter>0:
                gcode = Gcode.objects.get(ma=request.POST.get('ma'))
                gcode.mota = request.POST.get('mota')
                gcode.markupdinhmuc = request.POST.get('markupdinhmuc')
                gcode.save()
            else:
                form.save()
            return HttpResponseRedirect('/')
    return render(request, 'gcodedb/show.html', {'form': form})
def displaydata(request):
    results = Gcode.objects.all()
    return render(request, 'gcodedb/show.html',{'Gcodes':results})
def import_xls(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
            counter = Gcode.objects.filter(ma=data[1]).count()
            gcode = Gcode()
            if counter>0:
                gcode = Gcode.objects.get(ma=data[1])
                gcode.mote = data[2]
                gcode.markupdinhmuc = data[3]
                gcode.save()
            else:
        	    gcode = Gcode(
        		    data[0],
        		    data[1],
        		     data[2],
        		     data[3],
        		    )
        	    gcode.save()       
    return render(request, 'gcodedb/show.html')
def index(request,clientcode_id):
    client = Client.objects.get(pk=clientcode_id)
    #InquiryFormSet = modelformset_factory(Inquiry,fields=('inquirycode','datesubmitbid',))
    InquiryFormSet = inlineformset_factory(Client,Inquiry,fields=('inquirycode','datesubmitbid',),extra=1,max_num=2)
    if request.method == "POST":
        #formset = InquiryFormSet(request.POST,queryset=Inquiry.objects.filter(clientcode_id=client.clientcode))
        formset = InquiryFormSet(request.POST,instance = client)
        if formset.is_valid():
            formset.save()
            """ instances = formset.save(commit=False)
            for instance in instances:
                instance.clientcode_id = client.clientcode
                instance.save() """
            return redirect('index',clientcode_id = client.clientcode)
    #formset = InquiryFormSet(queryset=Inquiry.objects.filter(clientcode_id=client.clientcode))
    formset = InquiryFormSet(instance = client)
    return render(request,'gcodedb/entryclient.html', {'formset':formset})