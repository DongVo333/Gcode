from django.urls import path,include
from . import views,importxls,exportxls
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404,handler500
app_name = "gcodedb"

urlpatterns = [
    path('offer/insert/', views.offer_form,name='offer_insert'),
    path('offer/', importxls.importxls_offer,name='importxls_offer'),
    path('offer/update/<int:id>/', views.offer_form,name='offer_update'), 
    path('offer/delete/<int:id>/',views.offer_delete,name='offer_delete'),
    path('offer/export/xls', exportxls.exportxls_offer, name='exportxls_offer'),

    path('hdb/insert/', views.hdb_form,name='hdb_insert'),
    path('hdb/', views.hdb_list,name='hdb_list'),
    path('hdb/update/<int:id>/', views.hdb_form,name='hdb_update'), 
    path('hdb/delete/<int:id>/',views.hdb_delete,name='hdb_delete'),
    path('hdb/import/xls', importxls.importxls_hdb, name='importxls_hdb'),
    path('hdb/export/xls/<int:id>', exportxls.exportxls_hdb, name='exportxls_hdb'),

    path('po/insert/', views.po_form,name='po_insert'),
    path('po/', views.po_list,name='po_list'),
    path('po/update/<int:id>/', views.po_form,name='po_update'), 
    path('po/delete/<int:id>/',views.po_delete,name='po_delete'),
    path('po/import/xls', importxls.importxls_po, name='importxls_po'),
    path('po/export/xls/<str:po>', exportxls.exportxls_po, name='exportxls_po'),

    path('giaohang/insert/', views.giaohang_form,name='giaohang_insert'),
    path('giaohang/', views.giaohang_list,name='giaohang_list'),
    path('giaohang/update/<int:id>/', views.giaohang_form,name='giaohang_update'), 
    path('giaohang/delete/<int:id>/',views.giaohang_delete,name='giaohang_delete'),
    path('giaohang/import/xls', importxls.importxls_giaohang, name='importxls_giaohang'),
    path('giaohang/export/xls/<str:contract>', exportxls.exportxls_giaohang, name='exportxls_giaohang'),

    path('phat/insert/', views.phat_form,name='phat_insert'),
    path('phat/', views.phat_list,name='phat_list'),
    path('phat/update/<int:id>/', views.phat_form,name='phat_update'), 
    path('phat/delete/<int:id>/',views.phat_delete,name='phat_delete'),
    path('phat/import/xls', importxls.importxls_phat, name='importxls_phat'),
    path('phat/export/xls/<str:contract>', exportxls.exportxls_phat, name='exportxls_phat'),


    path('tienve/insert/', views.tienve_form,name='tienve_insert'),
    path('tienve/', views.tienve_list,name='tienve_list'),
    path('tienve/update/<int:id>/', views.tienve_form,name='tienve_update'), 
    path('tienve/delete/<int:id>/',views.tienve_delete,name='tienve_delete'),
    path('tienve/import/xls', importxls.importxls_tienve, name='importxls_tienve'),
    path('tienve/export/xls/<str:contract>', exportxls.exportxls_tienve, name='exportxls_tienve'),

    path('danhgiancc/insert/', views.danhgiancc_form,name='danhgiancc_insert'),
    path('danhgiancc/', views.danhgiancc_list,name='danhgiancc_list'),
    path('danhgiancc/update/<int:id>/', views.danhgiancc_form,name='danhgiancc_update'), 
    path('danhgiancc/delete/<int:id>/',views.danhgiancc_delete,name='danhgiancc_delete'),
    path('danhgiancc/import/xls', importxls.importxls_danhgiancc, name='importxls_danhgiancc'),
    path('danhgiancc/export/xls/<str:contract>', exportxls.exportxls_danhgiancc, name='exportxls_danhgiancc'),

    path('sales/insert/', views.sales_form,name='sales_insert'),
    path('sales/', views.sales_list,name='offer_list'),
    path('sales/update/<int:id>/', views.sales_form,name='sales_update'), 
    path('sales/delete/<int:id>/',views.sales_delete,name='sales_delete'),
    path('sales/import/xls', importxls.importxls_sales, name='importxls_sales'),
    path('sales/export/xls', exportxls.exportxls_sales, name='exportxls_sales'),

    path('danhgiacode/insert/', views.danhgiacode_form,name='danhgiacode_insert'),
    path('danhgiacode/', views.danhgiacode_list,name='offer_list'),
    path('danhgiacode/update/<int:id>/', views.danhgiacode_form,name='danhgiacode_update'), 
    path('danhgiacode/delete/<int:id>/',views.danhgiacode_delete,name='danhgiacode_delete'),
    path('danhgiacode/import/xls', importxls.importxls_danhgiacode, name='importxls_danhgiacode'),
    path('danhgiacode/export/xls', exportxls.exportxls_danhgiacode, name='exportxls_danhgiacode'),

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

   
    path('contractdetail/insert/', views.contractdetail_form,name='contractdetail_insert'),
    path('contractdetail/', views.contractdetail_list,name='contractdetail_list'),
    path('contractdetail/update/<int:id>/', views.contractdetail_form,name='contractdetail_update'), 
    path('contractdetail/delete/<int:id>/',views.contractdetail_delete,name='contractdetail_delete'),
    path('contractdetail/import/xls', importxls.importxls_contractdetail, name='importxls_contractdetail'),
    path('contractdetail/export/xls', exportxls.exportxls_contractdetail, name='exportxls_contractdetail'),
    
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
    path('kho/export/xls/<str:po>', exportxls.exportxls_kho, name='exportxls_kho'),
    
    path('profit/', views.profit_list,name='profit_list'),
    path('profit/show/<str:contract>', importxls.profit_show,name='profit_show'),
    path('profit/export/xls/<str:contract>', exportxls.exportxls_profit,name='exportxls_profit'),
    path('reportseller/', views.reportseller_list,name='reportseller_list'),
    path('scanorder/', views.scanorder_list,name='scanorder_list'),
    path('scanorder/import/xls', importxls.importxls_scanorder,name='importxls_scanorder'),
    path('scanorder/export/xls/<int:id>', exportxls.exportxls_scanorder,name='exportxls_scanorder'),

    path('', views.home, name='home'),
    path('login/',views.loginpage, name="loginpage"),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
]

handler404 = 'gcodedb.views.error404'
#handler500 = 'gcodedb.views.error500'