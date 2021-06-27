from django.urls import path
from . import views

urlpatterns = [
   path('', views.index),
   path('contract/', views.contract),
   path('po/', views.po),
]