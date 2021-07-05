from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm, formsets, inlineformset_factory,modelformset_factory,formset_factory
from django.views.generic import CreateView, ListView, UpdateView
from .models import Contract, G1code, G2code, GDV, Gcode,Inquiry,Client, Kho,Supplier,Lydowin,Lydoout
from django.db import transaction,IntegrityError
from .forms import GcodeForm, KhoForm, OfferForm, SearchQueryForm, ClientForm, InquiryForm,GDVForm,SupplierForm,ContractForm,LydooutForm,LydowinForm,OfferResultForm
from django.contrib import messages
from django.urls import reverse_lazy
from tablib import Dataset
from .filters import ClientFilter,G1codeFilter
from django.db.models import Q
from datetime import date
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
                        data.dateupdate = date.today()
                        data.save()
                        lydowins = offer.cleaned_data.get('lydowincode')
                        for lydoitem in lydowins:
                            data.lydowincode.add(lydoitem)
                            data.save()
                        lydoouts = offer.cleaned_data.get('lydooutcode')
                        for lydoitem in lydoouts:
                            data.lydooutcode.add(lydoitem)
                            data.save()
            except IntegrityError:
                print("Error Encountered")
			#return redirect('gcodedb:CreateOffer')
        else:
            print(form.errors)
            print(formset.errors)
    context['formset'] = formset
    context['form'] = form
    return render(request, 'gcodedb/createoffer.html', context)

def inquiry_list(request):
	inquiry_list = Inquiry.objects.all()
	return render(request, 'gcodedb/inquiry_list.html', {'inquiry_list':inquiry_list})

def inquiry_form(request, inquirycode=None):
    if request.method == "GET":
        if inquirycode == None:
            form = InquiryForm()
        else:
            inquiry = Inquiry.objects.get(pk=inquirycode)
            form = InquiryForm(instance=inquiry)
        return render(request, "gcodedb/inquiry_form.html", {'form': form})
    else:
        if inquirycode == None:
            form = InquiryForm(request.POST)
        else:
            inquiry = Inquiry.objects.get(pk=inquirycode)
            form = InquiryForm(request.POST,instance= inquiry)
        if form.is_valid():
            form.save()
        return redirect('/inquiry/')


def inquiry_delete(request,inquirycode):
    inquiry = Inquiry.objects.get(pk=inquirycode)
    inquiry.delete()
    return redirect('/inquiry/')

def client_list(request):
	client_list = Client.objects.all()
	return render(request, 'gcodedb/client_list.html', {'client_list':client_list})

def client_form(request, clientcode=None):
    if request.method == "GET":
        if clientcode == None:
            form = ClientForm()
        else:
            client = Client.objects.get(pk=clientcode)
            form = ClientForm(instance=client)
        return render(request, "gcodedb/client_form.html", {'form': form})
    else:
        if clientcode == None:
            form = ClientForm(request.POST)
        else:
            client = Client.objects.get(pk=clientcode)
            form = ClientForm(request.POST,instance= client)
        if form.is_valid():
            form.save()
        return redirect('/client/')


def client_delete(request,clientcode):
    client = Client.objects.get(pk=clientcode)
    client.delete()
    return redirect('/client/')

def gcode_list(request):
	gcode_list = Gcode.objects.all()
	return render(request, 'gcodedb/gcode_list.html', {'gcode_list':gcode_list})

def gcode_form(request, ma=None):
    if request.method == "GET":
        if ma == None:
            form = GcodeForm()
        else:
            gcode = Gcode.objects.get(pk=ma)
            form = GcodeForm(instance=gcode)
        return render(request, "gcodedb/gcode_form.html", {'form': form})
    else:
        if ma == None:
            form = GcodeForm(request.POST)
        else:
            gcode = Gcode.objects.get(pk=ma)
            form = GcodeForm(request.POST,instance= gcode)
        if form.is_valid():
            form.save()
        return redirect('/gcode/')


def gcode_delete(request,ma):
    gcode = Gcode.objects.get(pk=ma)
    gcode.delete()
    return redirect('/gcode/')

def gdv_list(request):
	gdv_list = GDV.objects.all()
	return render(request, 'gcodedb/gdv_list.html', {'gdv_list':gdv_list})

def gdv_form(request, gdvcode=None):
    if request.method == "GET":
        if gdvcode == None:
            form = GDVForm()
        else:
            gdv = GDV.objects.get(pk=gdvcode)
            form = GDVForm(instance=gdv)
        return render(request, "gcodedb/gdv_form.html", {'form': form})
    else:
        if gdvcode == None:
            form = GDVForm(request.POST)
        else:
            gdv = GDV.objects.get(pk=gdvcode)
            form = GDVForm(request.POST,instance= gdv)
        if form.is_valid():
            form.save()
        return redirect('/gdv/')


def gdv_delete(request,gdvcode):
    gdv = GDV.objects.get(pk=gdvcode)
    gdv.delete()
    return redirect('/gdv/')

def supplier_list(request):
	supplier_list = Supplier.objects.all()
	return render(request, 'gcodedb/supplier_list.html', {'supplier_list':supplier_list})

def supplier_form(request, suppliercode=None):
    if request.method == "GET":
        if suppliercode == None:
            form = SupplierForm()
        else:
            supplier = Supplier.objects.get(pk=suppliercode)
            form = SupplierForm(instance=supplier)
        return render(request, "gcodedb/supplier_form.html", {'form': form})
    else:
        if suppliercode == None:
            form = SupplierForm(request.POST)
        else:
            supplier = Supplier.objects.get(pk=suppliercode)
            form = SupplierForm(request.POST,instance= supplier)
        if form.is_valid():
            form.save()
        return redirect('/supplier/')


def supplier_delete(request,suppliercode):
    supplier = Supplier.objects.get(pk=suppliercode)
    supplier.delete()
    return redirect('/supplier/')

def contract_list(request):
	contract_list = Contract.objects.all()
	return render(request, 'gcodedb/contract_list.html', {'contract_list':contract_list})

def contract_form(request, contractcode=None):
    if request.method == "GET":
        if contractcode == None:
            form = ContractForm()
        else:
            contract = Contract.objects.get(pk=contractcode)
            form = ContractForm(instance=contract)
        return render(request, "gcodedb/contract_form.html", {'form': form})
    else:
        if contractcode == None:
            form = ContractForm(request.POST)
        else:
            contract = Contract.objects.get(pk=contractcode)
            form = ContractForm(request.POST,instance= contract)
        if form.is_valid():
            form.save()
        return redirect('/contract/')


def contract_delete(request,contractcode):
    contract = Contract.objects.get(pk=contractcode)
    contract.delete()
    return redirect('/contract/')

def lydowin_list(request):
	lydowin_list = Lydowin.objects.all()
	return render(request, 'gcodedb/lydowin_list.html', {'lydowin_list':lydowin_list})

def lydowin_form(request, lydowincode=None):
    if request.method == "GET":
        if lydowincode == None:
            form = LydowinForm()
        else:
            varlydowin = Lydowin.objects.get(pk=lydowincode)
            form = LydowinForm(instance=varlydowin)
        return render(request, "gcodedb/lydowin_form.html", {'form': form})
    else:
        if lydowincode == None:
            form = LydowinForm(request.POST)
        else:
            varlydowin = Lydowin.objects.get(pk=lydowincode)
            form = LydowinForm(request.POST,instance= varlydowin)
        if form.is_valid():
            form.save()
        return redirect('/lydowin/')

def lydowin_delete(request,lydowincode):
    varlydowin = Lydowin.objects.get(pk=lydowincode)
    varlydowin.delete()
    return redirect('/lydowin/')

def lydoout_list(request):
	lydoout_list = Lydoout.objects.all()
	return render(request, 'gcodedb/lydoout_list.html', {'lydoout_list':lydoout_list})

def lydoout_form(request, lydooutcode=None):
    if request.method == "GET":
        if lydooutcode == None:
            form = LydooutForm()
        else:
            varlydoout = Lydoout.objects.get(pk=lydooutcode)
            form = LydooutForm(instance=varlydoout)
        return render(request, "gcodedb/lydoout_form.html", {'form': form})
    else:
        if lydooutcode == None:
            form = LydooutForm(request.POST)
        else:
            varlydoout = Lydoout.objects.get(pk=lydooutcode)
            form = LydooutForm(request.POST,instance= varlydoout)
        if form.is_valid():
            form.save()
        return redirect('/lydoout/')

def lydoout_delete(request,lydooutcode):
    varlydoout = Lydoout.objects.get(pk=lydooutcode)
    varlydoout.delete()
    return redirect('/lydoout/')

def kho_list(request):
	kho_list = Kho.objects.all()
	return render(request, 'gcodedb/kho_list.html', {'kho_list':kho_list})

def kho_form(request, g2code_=None):
    if request.method == "GET":
        if g2code_ == None:
            form = KhoForm()
        else:
            g2codes = G2code.objects.filter(g2code = g2code_)
            kho = Kho.objects.get(pk=g2codes.g1code.id)
            form = KhoForm(instance=kho)
        return render(request, "gcodedb/kho_form.html", {'form': form})
    else:
        if g2code_ == None:
            form = KhoForm(request.POST)
        else:
            g2codes = G2code.objects.filter(g2code = g2code_)
            kho = Kho.objects.get(pk=g2codes.g1code.id)
            form = KhoForm(request.POST,instance= kho)
        if form.is_valid():
            form.save()
        return redirect('/kho/')

def kho_delete(request,g2code_):
    g2codes = G2code.objects.filter(g2code = g2code_)
    kho = Kho.objects.get(pk=g2codes.g1code.id)
    kho.delete()
    return redirect('/kho/')

def SearchHDB(request):
    g1code_list = G1code.objects.filter(resultinq='Win')
    g1code_filter = G1codeFilter(request.GET, queryset=g1code_list)
    g1code_temp = G1code.objects.filter(resultinq='Win',inquirycode=request.GET or None)
    for item in g1code_filter.qs:
        g1code_ = G1code.objects.get(pk = item.id)
        if G2code.objects.filter(g1code=g1code_).count()<=0:
            g2code = G2code.objects.create(g1code=g1code_, dateupdate = date.today())
    g2code_list = G2code.objects.all()
    return render(request, 'gcodedb/hdb.html', {'g2code_list': g2code_list, 'filter':g1code_filter})