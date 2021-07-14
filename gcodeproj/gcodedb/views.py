from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm, formsets, inlineformset_factory,modelformset_factory,formset_factory
from django.views.generic import CreateView, ListView, UpdateView
from .models import Contract, DanhgiaNSX, Danhgiacode, G1code, G2code, GDV, Gcode, Giaohang,Inquiry,Client, Kho, POdetail, Phat, Sales,Supplier,Lydowin,Lydoout, Tienve
from django.db import transaction,IntegrityError
from .forms import DanhgiaNSXForm, DanhgiacodeForm, GcodeForm, GiaohangForm, HDBForm, KhoForm, OfferForm, POForm, PhatForm, SalesForm, SearchQueryForm, ClientForm, InquiryForm,GDVForm,SupplierForm,ContractForm,LydooutForm,LydowinForm, TienveForm
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
						data.client = client
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

def inquiry_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = InquiryForm()
        else:
            inquiry = Inquiry.objects.get(pk=id)
            form = InquiryForm(instance=inquiry)
        return render(request, "gcodedb/inquiry_form.html", {'form': form})
    else:
        if id == None:
            form = InquiryForm(request.POST)
        else:
            inquiry = Inquiry.objects.get(pk=id)
            form = InquiryForm(request.POST,instance= inquiry)
        if form.is_valid():
            form.save()
        return redirect('/inquiry/')


def inquiry_delete(request,id):
    inquiry = Inquiry.objects.get(pk=id)
    inquiry.delete()
    return redirect('/inquiry/')

def client_list(request):
	client_list = Client.objects.all()
	return render(request, 'gcodedb/client_list.html', {'client_list':client_list})

def client_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = ClientForm()
        else:
            client = Client.objects.get(pk=id)
            form = ClientForm(instance=client)
        return render(request, "gcodedb/client_form.html", {'form': form})
    else:
        if id == None:
            form = ClientForm(request.POST)
        else:
            client = Client.objects.get(pk=id)
            form = ClientForm(request.POST,instance= client)
        if form.is_valid():
            form.save()
        return redirect('/client/')


def client_delete(request,id):
    client = Client.objects.get(pk=id)
    client.delete()
    return redirect('/client/')

def gcode_list(request):
	gcode_list = Gcode.objects.all()
	return render(request, 'gcodedb/gcode_list.html', {'gcode_list':gcode_list})

def gcode_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = GcodeForm()
        else:
            gcode = Gcode.objects.get(pk=id)
            form = GcodeForm(instance=gcode)
        return render(request, "gcodedb/gcode_form.html", {'form': form})
    else:
        if id == None:
            form = GcodeForm(request.POST)
        else:
            gcode = Gcode.objects.get(pk=id)
            form = GcodeForm(request.POST,instance= gcode)
        if form.is_valid():
            form.save()
        return redirect('/gcode/')


def gcode_delete(request,id):
    gcode = Gcode.objects.get(pk=id)
    gcode.delete()
    return redirect('/gcode/')

def gdv_list(request):
	gdv_list = GDV.objects.all()
	return render(request, 'gcodedb/gdv_list.html', {'gdv_list':gdv_list})

def gdv_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = GDVForm()
        else:
            gdv = GDV.objects.get(pk=id)
            form = GDVForm(instance=gdv)
        return render(request, "gcodedb/gdv_form.html", {'form': form})
    else:
        if id == None:
            form = GDVForm(request.POST)
        else:
            gdv = GDV.objects.get(pk=id)
            form = GDVForm(request.POST,instance= gdv)
        if form.is_valid():
            form.save()
        return redirect('/gdv/')


def gdv_delete(request,id):
    gdv = GDV.objects.get(pk=id)
    gdv.delete()
    return redirect('/gdv/')

def supplier_list(request):
	supplier_list = Supplier.objects.all()
	return render(request, 'gcodedb/supplier_list.html', {'supplier_list':supplier_list})

def supplier_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = SupplierForm()
        else:
            supplier = Supplier.objects.get(pk=id)
            form = SupplierForm(instance=supplier)
        return render(request, "gcodedb/supplier_form.html", {'form': form})
    else:
        if id == None:
            form = SupplierForm(request.POST)
        else:
            supplier = Supplier.objects.get(pk=id)
            form = SupplierForm(request.POST,instance= supplier)
        if form.is_valid():
            form.save()
        return redirect('/supplier/')


def supplier_delete(request,id):
    supplier = Supplier.objects.get(pk=id)
    supplier.delete()
    return redirect('/supplier/')

def contract_list(request):
	contract_list = Contract.objects.all()
	return render(request, 'gcodedb/contract_list.html', {'contract_list':contract_list})

def contract_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = ContractForm()
        else:
            contract = Contract.objects.get(pk=id)
            form = ContractForm(instance=contract)
        return render(request, "gcodedb/contract_form.html", {'form': form})
    else:
        if id == None:
            form = ContractForm(request.POST)
        else:
            contract = Contract.objects.get(pk=id)
            form = ContractForm(request.POST,instance= contract)
        if form.is_valid():
            form.save()
        return redirect('/contract/')


def contract_delete(request,id):
    contract = Contract.objects.get(pk=id)
    contract.delete()
    return redirect('/contract/')

def lydowin_list(request):
	lydowin_list = Lydowin.objects.all()
	return render(request, 'gcodedb/lydowin_list.html', {'lydowin_list':lydowin_list})

def lydowin_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = LydowinForm()
        else:
            varlydowin = Lydowin.objects.get(pk=id)
            form = LydowinForm(instance=varlydowin)
        return render(request, "gcodedb/lydowin_form.html", {'form': form})
    else:
        if id == None:
            form = LydowinForm(request.POST)
        else:
            varlydowin = Lydowin.objects.get(pk=id)
            form = LydowinForm(request.POST,instance= varlydowin)
        if form.is_valid():
            form.save()
        return redirect('/lydowin/')

def lydowin_delete(request,id):
    varlydowin = Lydowin.objects.get(pk=id)
    varlydowin.delete()
    return redirect('/lydowin/')

def lydoout_list(request):
	lydoout_list = Lydoout.objects.all()
	return render(request, 'gcodedb/lydoout_list.html', {'lydoout_list':lydoout_list})

def lydoout_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = LydooutForm()
        else:
            varlydoout = Lydoout.objects.get(pk=id)
            form = LydooutForm(instance=varlydoout)
        return render(request, "gcodedb/lydoout_form.html", {'form': form})
    else:
        if id == None:
            form = LydooutForm(request.POST)
        else:
            varlydoout = Lydoout.objects.get(pk=id)
            form = LydooutForm(request.POST,instance= varlydoout)
        if form.is_valid():
            form.save()
        return redirect('/lydoout/')

def lydoout_delete(request,id):
    varlydoout = Lydoout.objects.get(pk=id)
    varlydoout.delete()
    return redirect('/lydoout/')

def kho_list(request):
	kho_list = Kho.objects.all()
	return render(request, 'gcodedb/kho_list.html', {'kho_list':kho_list})

def kho_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = KhoForm()
        else:
            kho = Kho.objects.get(pk=id)
            form = KhoForm(instance=kho)
        return render(request, "gcodedb/kho_form.html", {'form': form})
    else:
        if id == None:
            form = KhoForm(request.POST)
        else:
            kho = Kho.objects.get(pk=id)
            form = KhoForm(request.POST,instance= kho)
        if form.is_valid():
            kho_ = form.save(commit=False)
            kho_.dateupdate = date.today()
            kho_.save()
        return redirect('/kho/')

def kho_delete(request,id):
    kho = Kho.objects.get(pk=id)
    kho.delete()
    return redirect('/kho/')

def SearchHDB(request):
    g1code_list = G1code.objects.filter(resultinq='Win')
    g1code_filter = G1codeFilter(request.GET, queryset=g1code_list)
    for item in g1code_filter.qs:
        g1code_ = G1code.objects.get(pk = item.id)
        if G2code.objects.filter(g1code=g1code_).count()<=0:
            G2code.objects.create(g1code=g1code_,dongiachaohdb = g1code_.dongiachaoinq, dateupdate = date.today())
    g2code_list = G2code.objects.all()
    return render(request, 'gcodedb/hdb.html', {'g2code_list': g2code_list, 'filter':g1code_filter})

def offer_list(request):
	offer_list = G1code.objects.all()
	return render(request, 'gcodedb/offer_list.html', {'offer_list':offer_list})

def offer_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = OfferForm()
        else:
            g1codes = G1code.objects.get(pk = id)
            form = OfferForm(instance=g1codes)
        return render(request, "gcodedb/offer_form.html", {'form': form})
    else:
        if id == None:
            form = OfferForm(request.POST)
        else:
            g1codes = G1code.objects.get(pk = id)
            form = OfferForm(request.POST,instance= g1codes)
        if form.is_valid():
            g1code = form.save(commit=False)
            g1code.dateupdate = date.today()
            g1code.g1code = g1code.gcode.ma +"-"+g1code.inquiry.inquirycode
            g1code.save()
            lydowins = form.cleaned_data.get('lydowin')
            for lydoitem in lydowins:
                g1code.lydowin.add(lydoitem)
            lydoouts = form.cleaned_data.get('lydoout')
            for lydoitem in lydoouts:
                g1code.lydoout.add(lydoitem)
            
        else:
            print(form.add_error)
        return redirect('/offer/')

def offer_delete(request,id):
    g1codes = G1code.objects.filter(pk = id)
    g1codes.delete()
    return redirect('/offer/')

def sales_list(request):
	sales_list = Sales.objects.all()
	return render(request, 'gcodedb/sales_list.html', {'sales_list':sales_list})

def sales_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = SalesForm()
        else:
            varsales = Sales.objects.get(pk=id)
            form = SalesForm(instance=varsales)
        return render(request, "gcodedb/sales_form.html", {'form': form})
    else:
        if id == None:
            form = SalesForm(request.POST)
        else:
            varsales = Sales.objects.get(pk=id)
            form = SalesForm(request.POST,instance= varsales)
        if form.is_valid():
            form.save()
        return redirect('/sales/')

def sales_delete(request,id):
    varsales = Sales.objects.get(pk=id)
    varsales.delete()
    return redirect('/sales/')

def hdb_list(request):
    hdb_list = G2code.objects.none
    if request.method == "POST":
        g1code_list = G1code.objects.filter(resultinq='Win',inquiry__inquirycode__icontains=request.POST.get("inquirysearch"))
        if g1code_list.count() > 0: 
            for item in g1code_list:
                g1code_ = G1code.objects.get(pk = item.id)
                if G2code.objects.filter(g1code=g1code_).count()<=0:
                    G2code.objects.create(g1code=g1code_,dongiachaohdb = g1code_.dongiachaoinq, dateupdate = date.today())
            return render(request, 'gcodedb/hdb_list.html', {'hdb_list': hdb_list})
    return render(request, 'gcodedb/hdb_list.html', {'hdb_list': hdb_list})

def hdb_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = HDBForm()
        else:
            g2codes = G2code.objects.get(pk = id)
            form = HDBForm(instance=g2codes)
        return render(request, "gcodedb/hdb_form.html", {'form': form})
    else:
        if id == None:
            form = HDBForm(request.POST)
        else:
            g2codes = G2code.objects.get(pk = id)
            form = HDBForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.g2code = g2codes.g1code.gcode.ma +"-"+ g2codes.contract.contractcode
            g2codes.save()
        else:
            print(form.add_error)
        return redirect('/hdb/')

def hdb_delete(request,id):
    g2codes = G2code.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/hdb/')

def po_list(request):
	po_list = POdetail.objects.all()
	return render(request, 'gcodedb/po_list.html', {'po_list':po_list})

def po_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = POForm()
        else:
            g2codes = POdetail.objects.get(pk = id)
            form = POForm(instance=g2codes)
        return render(request, "gcodedb/po_form.html", {'form': form})
    else:
        if id == None:
            form = POForm(request.POST)
        else:
            g2codes = POdetail.objects.get(pk = id)
            form = POForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.save()
        else:
            print(form.add_error)
        return redirect('/po/')

def po_delete(request,id):
    g2codes = POdetail.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/po/')

def giaohang_list(request):
	giaohang_list = Giaohang.objects.all()
	return render(request, 'gcodedb/giaohang_list.html', {'giaohang_list':giaohang_list})

def giaohang_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = GiaohangForm()
        else:
            g2codes = Giaohang.objects.get(pk = id)
            form = GiaohangForm(instance=g2codes)
        return render(request, "gcodedb/giaohang_form.html", {'form': form})
    else:
        if id == None:
            form = GiaohangForm(request.POST)
        else:
            g2codes = Giaohang.objects.get(pk = id)
            form = GiaohangForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.save()
        else:
            print(form.add_error)
        return redirect('/giaohang/')

def giaohang_delete(request,id):
    g2codes = Giaohang.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/giaohang/')

def tienve_list(request):
	tienve_list = Tienve.objects.all()
	return render(request, 'gcodedb/tienve_list.html', {'tienve_list':tienve_list})

def tienve_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = TienveForm()
        else:
            g2codes = Tienve.objects.get(pk = id)
            form = TienveForm(instance=g2codes)
        return render(request, "gcodedb/tienve_form.html", {'form': form})
    else:
        if id == None:
            form = TienveForm(request.POST)
        else:
            g2codes = Tienve.objects.get(pk = id)
            form = TienveForm(request.POST,instance= g2codes)
        if form.is_valid():
            form.save()
        else:
            print(form.add_error)
        return redirect('/tienve/')

def tienve_delete(request,id):
    g2codes = Tienve.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/tienve/')

def danhgiansx_list(request):
	danhgiansx_list = DanhgiaNSX.objects.all()
	return render(request, 'gcodedb/danhgiansx_list.html', {'danhgiansx_list':danhgiansx_list})

def danhgiansx_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = DanhgiaNSXForm()
        else:
            g2codes = DanhgiaNSX.objects.get(pk = id)
            form = DanhgiaNSXForm(instance=g2codes)
        return render(request, "gcodedb/danhgiansx_form.html", {'form': form})
    else:
        if id == None:
            form = DanhgiaNSXForm(request.POST)
        else:
            g2codes = DanhgiaNSX.objects.get(pk = id)
            form = DanhgiaNSXForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.save()
            danhgiacodes = form.cleaned_data.get('danhgiacode')
            for item in danhgiacodes:
                g2codes.danhgiacode.add(item)
        else:
            print(form.add_error)
        return redirect('/danhgiansx/')

def danhgiansx_delete(request,id):
    g2codes = DanhgiaNSX.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/danhgiansx/')

def danhgiacode_list(request):
	danhgiacode_list = Danhgiacode.objects.all()
	return render(request, 'gcodedb/danhgiacode_list.html', {'danhgiacode_list':danhgiacode_list})

def danhgiacode_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = DanhgiacodeForm()
        else:
            g2codes = Danhgiacode.objects.get(pk = id)
            form = DanhgiacodeForm(instance=g2codes)
        return render(request, "gcodedb/danhgiacode_form.html", {'form': form})
    else:
        if id == None:
            form = DanhgiacodeForm(request.POST)
        else:
            g2codes = Danhgiacode.objects.get(pk = id)
            form = DanhgiacodeForm(request.POST,instance= g2codes)
        if form.is_valid():
            form.save()
        else:
            print(form.add_error)
        return redirect('/danhgiacode/')

def danhgiacode_delete(request,id):
    g2codes = Danhgiacode.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/danhgiacode/')

def phat_list(request):
	phat_list = Phat.objects.all()
	return render(request, 'gcodedb/phat_list.html', {'phat_list':phat_list})

def phat_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = PhatForm()
        else:
            g2codes = Phat.objects.get(pk = id)
            form = PhatForm(instance=g2codes)
        return render(request, "gcodedb/phat_form.html", {'form': form})
    else:
        if id == None:
            form = PhatForm(request.POST)
        else:
            g2codes = Phat.objects.get(pk = id)
            form = PhatForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.save()
        else:
            print(form.add_error)
        return redirect('/phat/')

def phat_delete(request,id):
    g2codes = Phat.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/phat/')

