from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm, formsets, inlineformset_factory,modelformset_factory,formset_factory
from .models import G1code, Gcode,Inquiry,Client
from django.db import transaction,IntegrityError
from .forms import GcodeForm, OfferForm, SearchQueryForm, ClientForm, InquiryForm
from django.contrib import messages
from tablib import Dataset
from .filters import ClientFilter
from django.db.models import Q
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
    InquiryFormSet = inlineformset_factory(Client,Inquiry,fields=('inquirycode','datesubmitbid',),extra=1)
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
class NestedSearch(FormView):
    form_class = formset_factory(SearchQueryForm)
    template_name = 'gcodedb/searchclient.html'
    success_url = ''

    def form_valid(self, form):
        # Build the query chain
        qs = []
        for form_query in form.cleaned_data:
            q = {'{0}__{1}'.format(form_query['query_field'], form_query['lookup']): form_query['query']}
            qs.append(Q(**q))

        results = Client.objects.filter(*qs)

        return self.render_to_response(self.get_context_data(results=results, form=form))

def create(request):
	context = {}
	InquiryFormSet = modelformset_factory(Inquiry, form=InquiryForm)	
	form = ClientForm(request.POST or None)
	formset = InquiryFormSet(request.POST or None, queryset= Inquiry.objects.none(), prefix='fk_Inquiryclient')
	if request.method == "POST":
		if form.is_valid() and formset.is_valid():
			try:
				with transaction.atomic():
					client = form.save(commit=False)
					client.save()

					for inquiry in formset:
						data = inquiry.save(commit=False)
						data.clientcode = client
						data.save()
			except IntegrityError:
				print("Error Encountered")

			return redirect('gcodedb:list')


	context['formset'] = formset
	context['form'] = form
	return render(request, 'gcodedb/create.html', context)

def list(request):
	datas = Client.objects.all()
	return render(request, 'gcodedb/list.html', {'datas':datas})
def search(request):
    client_list = Client.objects.all()
    client_filter = ClientFilter(request.GET, queryset=client_list)
    return render(request, 'gcodedb/search.html', {'filter': client_filter})
def CreateOffer(request):
	context = {}
	OfferFormSet = modelformset_factory(G1code, form=OfferForm)	
	form = InquiryForm(request.POST or None)
	formset = OfferFormSet(request.POST or None, queryset= G1code.objects.none(), prefix='fk_g1codeinquiry')
	if request.method == "POST":
		if form.is_valid() and formset.is_valid():
			try:
				with transaction.atomic():
					inquiry = form.save(commit=False)
					inquiry.save()

					for offer in formset:
						data = offer.save(commit=False)
						data.inquirycode = inquiry
						data.save()
			except IntegrityError:
				print("Error Encountered")
			#return redirect('gcodedb:CreateOffer')

	context['formset'] = formset
	context['form'] = form
	return render(request, 'gcodedb/createoffer.html', context)