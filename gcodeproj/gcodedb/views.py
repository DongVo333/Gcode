from django import forms
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView,FormView
from django.http import HttpResponse,HttpResponseRedirect
from django.forms import ModelForm, formsets, inlineformset_factory,modelformset_factory,formset_factory
from django.views.generic import CreateView, ListView, UpdateView
from .models import Contract, Danhgiagcode, G1code, Nhaplieuban, GDV, Gcode, Inquiry,Client, Nhaplieunhapkhau, Nhaplieumua, Phat, Sales,Supplier,Lydowin,Lydoout, Tienve
from django.db import transaction,IntegrityError
from .forms import DanhgiagcodeForm, GcodeForm, NlbForm, NlnkForm, MyForm, OfferForm, NlmForm, PhatForm, SalesForm, ClientForm, InquiryForm,GDVForm,SupplierForm,ContractForm,LydooutForm,LydowinForm, TienveForm
from .filters import ClientFilter
from django.db.models import Q
from datetime import date
import csv
from django.utils.html import format_html
import pandas as pd
import numpy as np
from django.urls import reverse
from fuzzywuzzy import fuzz,process
from django.contrib.auth.decorators import login_required
from .decorators import allowed_permission
from  django.contrib.auth import authenticate,login
from django.template import Context, loader

""" class PostListView(ListView):
   queryset = Gcode.objects.all().order_by('-ma')
   template_name = 'gcodedb/show.html'
   context_object_name = 'Gcodes'
class PostDetailView(DetailView):
   model = Gcode
   template_name = 'gcodedb/detail.html'
   context_object_name = 'gcodekey'
 """

""" def savedata(request):
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
    return render(request, 'gcodedb/createoffer.html', context) """

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_inquiry'})
def inquiry_list(request):
	inquiry_list = Inquiry.objects.all()
	return render(request, 'gcodedb/inquiry_list.html', {'inquiry_list':inquiry_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_inquiry'})
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_inquiry'})
def inquiry_delete(request,id):
    inquiry = Inquiry.objects.get(pk=id)
    inquiry.delete()
    return redirect('/inquiry/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_client'})
def client_list(request):
	client_list = Client.objects.all()
	return render(request, 'gcodedb/client_list.html', {'client_list':client_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_client'})
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_client'})
def client_delete(request,id):
    client = Client.objects.get(pk=id)
    client.delete()
    return redirect('/client/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_gcode'})
def gcode_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        gcode_set = set()
        code_list = Gcode.objects.values_list('ma',flat=True)
        kymahieu_list = Gcode.objects.values_list('kymahieuinq',flat=True)
        description_list = Gcode.objects.values_list('mota',flat=True)
        ratio_code = process.extract(request.POST.get("gcodesearch"),code_list)
        ratio_kymahieu = process.extract(request.POST.get("gcodesearch"),kymahieu_list)
        ratio_des = process.extract(request.POST.get("gcodesearch"),description_list)
        for ratio in ratio_code:
            if ratio[1] >= 90:
                gcode_set.add(Gcode.objects.get(ma = ratio[0]).ma)
        for ratio in ratio_kymahieu:
            if ratio[1] >= 90:
                gcode_set.add(Gcode.objects.get(kymahieuinq = ratio[0]).ma)
        for ratio in ratio_des:
            if ratio[1] >= 90:
                gcode_set.add(Gcode.objects.get(mota = ratio[0]).ma)
        df = pd.DataFrame(columns=['Gcode','K?? m?? hi???u','M?? t???']) 
        if len(gcode_set)>0:
            for item in gcode_set:
                gcode = Gcode.objects.get(ma=item)
                df = df.append(pd.DataFrame({'Gcode':[gcode.ma],
                                            'K?? m?? hi???u':[gcode.kymahieuinq],
                                            'M?? t???':[gcode.mota]}))
            msgresult = format_html("Have <b>{}</b> results for your search query as the below:<br>",len(gcode_set))
            html = df.to_html(index=False,justify='center')
            context = {'gcode_list': html,'msgresult':msgresult}
            return render(request, 'gcodedb/gcode_list.html', context)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/gcode_list.html', {'msgresult':msgresult})


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_gcode'})                        
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_gcode'})
def gcode_delete(request,id):
    gcode = Gcode.objects.get(pk=id)
    gcode.delete()
    return redirect('/gcode/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_seller'})
def gdv_list(request):
	gdv_list = GDV.objects.all()
	return render(request, 'gcodedb/gdv_list.html', {'gdv_list':gdv_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_seller'})
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_seller'})
def gdv_delete(request,id):
    gdv = GDV.objects.get(pk=id)
    gdv.delete()
    return redirect('/gdv/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_supplier'})
def supplier_list(request):
	supplier_list = Supplier.objects.all()
	return render(request, 'gcodedb/supplier_list.html', {'supplier_list':supplier_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_supplier'})
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


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_supplier'})
def supplier_delete(request,id):
    supplier = Supplier.objects.get(pk=id)
    supplier.delete()
    return redirect('/supplier/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_contract'})
def contract_list(request):
	return render(request, 'gcodedb/contract_list.html')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_contract'})
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
        return redirect('contract')


@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_contract'})
def contract_delete(request,id):
    contract = Contract.objects.get(pk=id)
    contract.delete()
    return redirect('/contract/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_reasonwin'})
def lydowin_list(request):
    lydowin_list = Lydowin.objects.all()
    myform_ = MyForm()
    return render(request, 'gcodedb/lydowin_list.html', {'lydowin_list':lydowin_list, 'myform':myform_})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_reasonwin'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_reasonwin'})
def lydowin_delete(request,id):
    varlydowin = Lydowin.objects.get(pk=id)
    varlydowin.delete()
    return redirect('/lydowin/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_reasonout'})
def lydoout_list(request):
	lydoout_list = Lydoout.objects.all()
	return render(request, 'gcodedb/lydoout_list.html', {'lydoout_list':lydoout_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_reasonout'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_reasonout'})
def lydoout_delete(request,id):
    varlydoout = Lydoout.objects.get(pk=id)
    varlydoout.delete()
    return redirect('/lydoout/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_warehouse'})
def nlnk_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        nlm_set = set()
        podetail_list = Nhaplieumua.objects.filter(g2code__pono__icontains=request.POST.get("ponosearch")).values_list('g2code', flat=True)
        for g2code in podetail_list:
            nlm_set.add(Nhaplieuban.objects.get(pk=g2code).pono)
        if len(nlm_set)> 0: 
            msgresult = format_html("Have <b>{}</b> results for your search query as the below:<br>",len(nlm_set))
            for item in nlm_set:
                g2code_list = Nhaplieumua.objects.filter(g2code__pono=item)
                message = format_html("PO No. <b>'{}'</b> has {} Gcodes <a href='{}'>Click to export Excel</a>",
                item,g2code_list.count(),reverse('gcodedb:exportxls_nlnk', args=[item]))
                msg.append(message)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/nlnk_list.html', {'msg':msg,'msgresult':msgresult})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_warehouse'})
def nlnk_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = NlnkForm()
        else:
            nlnk = Nhaplieunhapkhau.objects.get(pk=id)
            form = NlnkForm(instance=nlnk)
        return render(request, "gcodedb/nlnk_form.html", {'form': form})
    else:
        if id == None:
            form = NlnkForm(request.POST)
        else:
            nlnk = Nhaplieunhapkhau.objects.get(pk=id)
            form = NlnkForm(request.POST,instance= nlnk)
        if form.is_valid():
            nlnk_ = form.save(commit=False)
            nlnk_.dateupdate = date.today()
            nlnk_.save()
        return redirect('/nlnk/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_warehouse'})
def nlnk_delete(request,id):
    nlnk = Nhaplieunhapkhau.objects.get(pk=id)
    nlnk.delete()
    return redirect('/nlnk/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_g1code'})
def offer_list(request):
	offer_list = G1code.objects.all()
	return render(request, 'gcodedb/offer_list.html', {'offer_list':offer_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_g1code'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_g1code'})
def offer_delete(request,id):
    g1codes = G1code.objects.filter(pk = id)
    g1codes.delete()
    return redirect('/offer/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_sales'})
def sales_list(request):
	sales_list = Sales.objects.all()
	return render(request, 'gcodedb/sales_list.html', {'sales_list':sales_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_sales'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_sales'})
def sales_delete(request,id):
    varsales = Sales.objects.get(pk=id)
    varsales.delete()
    return redirect('/sales/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_g2code'})       
def nlb_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        inquiry_list = Inquiry.objects.filter(inquirycode__icontains=request.POST.get("inquirysearch"))
        if inquiry_list.count() > 0: 
            msgresult = format_html("Have <b>{}</b> results for your search query as the below:<br>",inquiry_list.count())
            for item in inquiry_list:
                g1code_list = G1code.objects.filter(inquiry=item, resultinq ="Win")
                message = format_html("Inquiry <b>'{}'</b> has {} Gcodes <a href='{}'>Click to export Excel</a>",
                item.inquirycode,g1code_list.count(),reverse('gcodedb:exportxl_nlb', args=[item.id]))
                msg.append(message)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/nlb_list.html', {'msg':msg,'msgresult':msgresult})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_g2code'})
def nlb_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = NlbForm()
        else:
            g2codes = Nhaplieuban.objects.get(pk = id)
            form = NlbForm(instance=g2codes)
        return render(request, "gcodedb/nlb_form.html", {'form': form})
    else:
        if id == None:
            form = NlbForm(request.POST)
        else:
            g2codes = Nhaplieuban.objects.get(pk = id)
            form = NlbForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.g2code = g2codes.g1code.gcode.ma +"-"+ g2codes.contract.contractcode
            g2codes.save()
        else:
            print(form.add_error)
        return redirect('/nlb/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_g2code'})
def nlb_delete(request,id):
    g2codes = Nhaplieuban.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/nlb/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_podetail'})
def nlm_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        contract_list = Nhaplieuban.objects.filter(contractno__contractcode__icontains=request.POST.get("contractsearch")).values_list('contractno', flat=True)
        nlm_set =set(contract_list)
        if len(nlm_set)> 0: 
            msgresult = format_html("Have <b>{}</b> result for your search query as the below:<br>",len(nlm_set))
            for item in nlm_set:
                contract_list = Nhaplieuban.objects.filter(contractno=item)
                contractname = Contract.objects.get(id = item ).contractcode
                message = format_html("Contract No. <b>'{}'</b> has {} Gcodes <a href='{}'>Click to export Excel</a>",
                contractname,contract_list.count(),reverse('gcodedb:exportxls_nlm',args=[item,]))
                msg.append(message)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/nlm_list.html', {'msg':msg,'msgresult':msgresult})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_nlm'})
def nlm_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = NlmForm()
        else:
            g2codes = Nhaplieumua.objects.get(pk = id)
            form = NlmForm(instance=g2codes)
        return render(request, "gcodedb/nlm_form.html", {'form': form})
    else:
        if id == None:
            form = NlmForm(request.POST)
        else:
            g2codes = Nhaplieumua.objects.get(pk = id)
            form = NlmForm(request.POST,instance= g2codes)
        if form.is_valid():
            g2codes = form.save(commit=False)
            g2codes.dateupdate = date.today()
            g2codes.save()
        else:
            print(form.add_error)
        return redirect('/po/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_podetail'})
def nlm_delete(request,id):
    g2codes = Nhaplieumua.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/po/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_accounting'})
def tienve_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        contract_set = set()
        contract_list = Nhaplieuban.objects.filter(contract__contractcode__icontains=request.POST.get("contractsearch")).values_list('g2code', flat=True)
        for g2code in contract_list:
            contract_set.add(Nhaplieuban.objects.get(g2code=g2code).contract.contractcode)
        if len(contract_set)> 0: 
            msgresult = format_html("Have <b>{}</b> results for your search query as the below:<br>",len(contract_set))
            for item in contract_set:
                g2code_list = Nhaplieuban.objects.filter(contract__contractcode=item)
                message = format_html("Contract No. <b>'{}'</b> has {} Gcodes <a href='{}'>Click to export Excel</a>",
                item,g2code_list.count(),reverse('gcodedb:exportxls_tienve', args=[item]))
                msg.append(message)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/tienve_list.html', {'msg':msg,'msgresult':msgresult})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_accounting'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_accounting'})
def tienve_delete(request,id):
    g2codes = Tienve.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/tienve/')



@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_danhgiacode'})
def danhgiacode_list(request):
	danhgiacode_list = Danhgiagcode.objects.all()
	return render(request, 'gcodedb/danhgiacode_list.html', {'danhgiacode_list':danhgiacode_list})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_danhgiacode'})
def danhgiacode_form(request, id=None):
    if request.method == "GET":
        if id == None:
            form = DanhgiagcodeForm()
        else:
            g2codes = Danhgiagcode.objects.get(pk = id)
            form = DanhgiagcodeForm(instance=g2codes)
        return render(request, "gcodedb/danhgiacode_form.html", {'form': form})
    else:
        if id == None:
            form = DanhgiagcodeForm(request.POST)
        else:
            g2codes = Danhgiagcode.objects.get(pk = id)
            form = DanhgiagcodeForm(request.POST,instance= g2codes)
        if form.is_valid():
            form.save()
        else:
            print(form.add_error)
        return redirect('/danhgiacode/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_danhgiacode'})
def danhgiacode_delete(request,id):
    g2codes = Danhgiagcode.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/danhgiacode/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_punishment'})
def phat_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        contract_set = set()
        contract_list = Nhaplieunhapkhau.objects.filter(g2code__contractno__contractcode__icontains=request.POST.get("contractsearch")).values_list('g2code', flat=True)
        for g2code in contract_list:
            contract_set.add(Nhaplieuban.objects.get(pk=g2code).contractno.contractcode)
        if len(contract_set)> 0: 
            msgresult = format_html("Have <b>{}</b> results for your search query as the below:<br>",len(contract_set))
            for item in contract_set:
                g2code_list = Nhaplieunhapkhau.objects.filter(g2code__contract__contractcode=item)
                message = format_html("Contract No. <b>'{}'</b> has {} Gcodes <a href='{}'>Click to export Excel</a>",
                item,g2code_list.count(),reverse('gcodedb:exportxls_phat', args=[item]))
                msg.append(message)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/phat_list.html', {'msg':msg,'msgresult':msgresult})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_punishment'})
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

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.delete_punishment'})
def phat_delete(request,id):
    g2codes = Phat.objects.filter(pk = id)
    g2codes.delete()
    return redirect('/phat/')

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_profit'})
def profit_list(request):
    msg = []
    msgresult = ""
    if request.method == "POST":
        contract_set = set()
        contract_list = Nhaplieuban.objects.filter(contractno__contractcode__icontains=request.POST.get("contractsearch")).values_list('contract', flat=True)
        for contract in contract_list:
            contract_set.add(Contract.objects.get(pk=contract).contractcode)
        if len(contract_set)> 0: 
            msgresult = format_html("Have <b>{}</b> results for your search query as the below:<br>",len(contract_set))
            for item in contract_set:
                g2code_list = Nhaplieuban.objects.filter(contract__contractcode=item)
                message = format_html("Contract No. <b>'{}'</b> has {} Gcodes <a href='{}'>Click to view detail</a>",
                item,g2code_list.count(),reverse('gcodedb:profit_show', args=[item]))
                msg.append(message)
        else: 
            msgresult = format_html("No results could be found for your search query")
    return render(request, 'gcodedb/profit_list.html', {'msg':msg,'msgresult':msgresult})

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_sellerreport'})
def reportseller_list(request):
    df = pd.DataFrame(columns=['Gcode-Inquiry','Result','Giao d???ch vi??n'])
    for item in G1code.objects.all():
        df = df.append(pd.DataFrame({'Gcode-Inquiry':[item.g1code],'Result':[item.resultinq],
        'Giao d???ch vi??n':[item.gdvinq.gdvcode]}))
    dfpivot = pd.pivot_table(df, values='Gcode-Inquiry', index='Giao d???ch vi??n',columns='Result', aggfunc='count')
    html = dfpivot.to_html(justify='center')
    context = {'reportseller_list':html}
    return render(request, 'gcodedb/reportseller_list.html', context)

@login_required(login_url='gcodedb:loginpage')
@allowed_permission(allowed_roles={'gcodedb.view_scanorder','gcodedb.export_scanorder'})
def scanorder_list(request):
    return render(request, 'gcodedb/scanorder_list.html')

@login_required(login_url='gcodedb:loginpage')
def home(request):
    return render(request,'gcodedb/home.html')

def loginpage(request):
    message = []
    if request.user.is_authenticated:
        return redirect('gcodedb:home')
    else:
        if request.method == 'POST':
            name = request.POST.get('Username')
            pw = request.POST.get('Password')
            user = authenticate(username=name, password=pw)
            if user is not None:
                login(request,user)
                return redirect('gcodedb:home')
            else:
                msg = format_html('<i>Username or password is wrong<i>')
                message.append(msg)
                print(msg)
    context = {'message':message}
    return render(request,'gcodedb/login.html',context)

def error404(request, exception):
    return render(request, 'gcodedb/404.html')


def error404(request,*args,**argv):
    return render(request,"gcodedb/404.html")
def error500(request):
    return render(request,"gcodedb/500.html")