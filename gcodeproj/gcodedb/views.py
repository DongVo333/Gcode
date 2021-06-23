from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import HttpResponse,HttpResponseRedirect
from .models import Gcode
from .forms import GcodeForm
from django.contrib import messages
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
    writer.writerow(['ID', 'Gcode', 'Mo ta', 'Xuatxu','Markup dinh muc'])

    users = Gcode.objects.all().values_list('id', 'ma', 'mota', 'xuatxu','markupdinhmuc')
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

    rows = Gcode.objects.all().values_list('id', 'ma', 'mota', 'xuatxu','markupdinhmuc')
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
                gcode.xuatxu = request.POST.get('xuatxu')
                gcode.markupdinhmuc = request.POST.get('markupdinhmuc')
                gcode.save()
            else:
                form.save()
            return HttpResponseRedirect('/')
    return render(request, 'gcodedb/show.html', {'form': form})
def displaydata(request):
    results = Gcode.objects.all()
    return render(request, 'gcodedb/show.html',{'Gcodes':results})