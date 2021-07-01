from django.urls import path
from . import views

app_name = "gcodedb"

urlpatterns = [
    path('offer/',views.CreateOffer, name='createoffer'),
    path('searchclient/',views.NestedSearch),
    path('create/', views.create, name="create"),
    path('list/', views.list, name="list"),
    path('search/', views.search, name='search'),
    path('<int:pk>/', views.PostDetailView.as_view(),name='gcodedetail'),
    path('export/csv', views.export_users_csv, name='export_users_csv'),
    path('export/xls', views.export_users_xls, name='export_users_xls'),
    path('display/', views.displaydata),
    path('savedata/', views.savedata, name ='savedata'),
    path('import/xls', views.import_xls, name='import_xls'),
]