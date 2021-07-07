from django.urls import path,include
from . import views,importxls,exportxls

app_name = "gcodedb"

urlpatterns = [
    path('offer/insert/', views.offer_form,name='offer_insert'),
    path('offer/', views.offer_list,name='offer_list'),
    path('offer/update/<int:id>/', views.offer_form,name='offer_update'), 
    path('offer/delete/<int:id>/',views.offer_delete,name='offer_delete'),
    path('offer/import/xls', importxls.importxls_offer, name='importxls_offer'),
    path('offer/export/xls', exportxls.exportxls_offer, name='exportxls_offer'),


    path('searchclient/',views.NestedSearch, name='searchclient'),
    path('create/', views.create, name="create"),
    path('list/', views.list, name="list"),
    path('search/', views.search, name='search'),  

    path('inquiry/insert/', views.inquiry_form,name='inquiry_insert'),
    path('inquiry/', views.inquiry_list,name='inquiry_list'),
    path('inquiry/update/<int:id>/', views.inquiry_form,name='inquiry_update'), 
    path('inquiry/delete/<int:id>/',views.inquiry_delete,name='inquiry_delete'),
    path('inquiry/import/xls', importxls.importxls_inquiry, name='importxls_inquiry'),
    path('inquiry/export/xls', exportxls.exportxls_inquiry, name='exportxls_inquiry'), 

    path('client/insert/', views.client_form,name='client_insert'),
    path('client/', views.client_list,name='client_list'),
    path('client/update/<int:id>/', views.client_form,name='client_update'), 
    path('client/delete/<int:id>/',views.client_delete,name='client_delete'),
    path('client/import/xls', importxls.importxls_client, name='importxls_client'),
    path('client/export/xls', exportxls.exportxls_client, name='exportxls_client'),
   
    path('gcode/insert/', views.gcode_form,name='gcode_insert'),
    path('gcode/', views.gcode_list,name='gcode_list'),
    path('gcode/update/<int:id>/', views.gcode_form,name='gcode_update'), 
    path('gcode/delete/<int:id>/',views.gcode_delete,name='gcode_delete'),
    path('gcode/import/xls', importxls.importxls_gcode, name='importxls_gcode'),
    path('gcode/export/xls', exportxls.exportxls_gcode, name='exportxls_gcode'),
   
    path('gdv/insert/', views.gdv_form,name='gdv_insert'),
    path('gdv/', views.gdv_list,name='gdv_list'),
    path('gdv/update/<int:id>/', views.gdv_form,name='gdv_update'), 
    path('gdv/delete/<int:id>/',views.gdv_delete,name='gdv_delete'),
    path('gdv/import/xls', importxls.importxls_gdv, name='importxls_gdv'),
    path('gdv/export/xls', exportxls.exportxls_gdv, name='exportxls_gdv'),
  
    path('supplier/insert/', views.supplier_form,name='supplier_insert'),
    path('supplier/', views.supplier_list,name='supplier_list'),
    path('supplier/update/<int:id>/', views.supplier_form,name='supplier_update'), 
    path('supplier/delete/<int:id>/',views.supplier_delete,name='supplier_delete'),
    path('supplier/import/xls', importxls.importxls_supplier, name='importxls_supplier'),
    path('supplier/export/xls', exportxls.exportxls_supplier, name='exportxls_supplier'),

   
    path('contract/insert/', views.contract_form,name='contract_insert'),
    path('contract/', views.contract_list,name='contract_list'),
    path('contract/update/<int:id>/', views.contract_form,name='contract_update'), 
    path('contract/delete/<int:id>/',views.contract_delete,name='contract_delete'),
    path('contract/import/xls', importxls.importxls_contract, name='importxls_contract'),
    path('contract/export/xls', exportxls.exportxls_contract, name='exportxls_contract'),
    
    path('lydowin/insert/', views.lydowin_form,name='lydowin_insert'),
    path('lydowin/', views.lydowin_list,name='lydowin_list'),
    path('lydowin/update/<int:id>/', views.lydowin_form,name='lydowin_update'), 
    path('lydowin/delete/<int:id>/',views.lydowin_delete,name='lydowin_delete'),
    path('lydowin/import/xls', importxls.importxls_lydowin, name='importxls_lydowin'),
    path('lydowin/export/xls', exportxls.exportxls_lydowin, name='exportxls_lydowin'),
      
    path('lydoout/insert/', views.lydoout_form,name='lydoout_insert'),
    path('lydoout/', views.lydoout_list,name='lydoout_list'),
    path('lydoout/update/<int:id>/', views.lydoout_form,name='lydoout_update'), 
    path('lydoout/delete/<int:id>/',views.lydoout_delete,name='lydoout_delete'),
    path('lydoout/import/xls', importxls.importxls_lydoout, name='importxls_lydoout'),
    path('lydoout/export/xls', exportxls.exportxls_lydoout, name='exportxls_lydoout'),
        
    path('kho/insert/', views.kho_form,name='kho_insert'),
    path('kho/',views.kho_list,name='kho_list'),
    path('kho/update/<int:id>/', views.kho_form,name='kho_update'), 
    path('kho/delete/<int:id>/',views.kho_delete,name='kho_delete'),
    path('kho/import/xls', importxls.importxls_kho, name='importxls_kho'),
    path('kho/export/xls', exportxls.exportxls_kho, name='exportxls_kho'),

    path('hdb/',views.SearchHDB,name='searchhdb'),
    path('display/', views.displaydata,name='display'),
    path('savedata/', views.savedata, name ='savedata'),
]
