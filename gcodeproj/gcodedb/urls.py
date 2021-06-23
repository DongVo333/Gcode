from django.urls import path
from . import views
urlpatterns = [
    path('',views.PostListView.as_view(), name='gcodelist'),
    path('<int:pk>/', views.PostDetailView.as_view(),name='gcodedetail'),
    path('export/csv', views.export_users_csv, name='export_users_csv'),
    path('export/xls', views.export_users_xls, name='export_users_xls'),
    path('display/', views.displaydata),
    path('savedata/', views.savedata, name ='savedata'),
    path('import/xls', views.import_xls, name='import_xls')
]