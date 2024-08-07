from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ypersyndesmos/', views.ypersyndesmos_view, name='ypersyndesmos'),
    path('anafora_aks_ipiresias/', views.anafora_aks_ipiresias, name='anafora_aks_ipiresias'),
    path('epilochias/', views.epilochias_view, name='epilochias'),
    path('report/', views.report_view, name='report'),
    path('download_pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('anafora_ipiresia/', views.report_view, name='anafora_ipiresia'),
]
