from django.urls import path,include
from . import views,importxls,exportxls
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django import views as myapp_views

app_name = "gcodedb"

urlpatterns = [
    path('offer/insert/', views.offer_form,name='offer_insert'),
    path('offer/', importxls.importxls_offer,name='importxls_offer'),
    path('offer/update/<int:id>/', views.offer_form,name='offer_update'), 
    path('offer/delete/<int:id>/',views.offer_delete,name='offer_delete'),
    path('offer/export/xls', exportxls.exportxls_offer, name='exportxls_offer'),

    path('nlb/insert/', views.nlb_form,name='nlb_insert'),
    path('nlb/', views.nlb_list,name='importxls_nlb'),
    path('nlb/update/<int:id>/', views.nlb_form,name='nlb_update'), 
    path('nlb/delete/<int:id>/',views.nlb_delete,name='nlb_delete'),
    path('nlb/export/xls/', exportxls.exportxls_nlb, name='exportxls_nlb'),

    path('nlm/insert/', views.nlm_form,name='nlm_insert'),
    path('nlm/', views.nlm_list,name='nlm_list'),
    path('nlm/update/<int:id>/', views.nlm_form,name='nlm_update'), 
    path('nlm/delete/<int:id>/',views.nlm_delete,name='nlm_delete'),
    path('nlm/import/xls', importxls.importxls_nlm, name='importxls_nlm'),
    path('nlm/export/xls/<str:nlm>', exportxls.exportxls_nlm, name='exportxls_nlm'),

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

    path('sales/insert/', views.sales_form,name='sales_insert'),
    path('sales/', views.sales_list,name='offer_list'),
    path('sales/update/<int:id>/', views.sales_form,name='sales_update'), 
    path('sales/delete/<int:id>/',views.sales_delete,name='sales_delete'),
    path('sales/import/xls', importxls.importxls_sales, name='importxls_sales'),
    path('sales/export/xls', exportxls.exportxls_sales, name='exportxls_sales'),

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
        
    path('nlnk/insert/', views.nlnk_form,name='nlnk_insert'),
    path('nlnk/',views.nlnk_list,name='nlnk_list'),
    path('nlnk/update/<int:id>/', views.nlnk_form,name='nlnk_update'), 
    path('nlnk/delete/<int:id>/',views.nlnk_delete,name='nlnk_delete'),
    path('nlnk/import/xls', importxls.importxls_nlnk, name='importxls_nlnk'),
    path('nlnk/export/xls/<str:po>', exportxls.exportxls_nlnk, name='exportxls_nlnk'),
    
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
