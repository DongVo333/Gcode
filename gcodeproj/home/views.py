from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
   return render(request, 'home/home.html')
def contract(request):
   return render(request, 'home/contract.html')
def po(request):
   return render(request, 'home/po.html')