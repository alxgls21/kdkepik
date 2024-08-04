from django.shortcuts import render
from .models import DidesCategory, HarpCategory, AdmeCategory

def index(request):
    return render(request, 'index.html')

def ypersyndesmos(request):
    dides_categories = DidesCategory.objects.all()
    harp_categories = HarpCategory.objects.all()
    adme_categories = AdmeCategory.objects.all()
    return render(request, 'ypersyndesmos.html', {
        'dides_categories': dides_categories,
        'harp_categories': harp_categories,
        'adme_categories': adme_categories
    })

def anafora_aks_ipiresias(request):
    return render(request, 'anafora_aks_ipiresias.html')