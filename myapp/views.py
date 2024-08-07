from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from .models import DidesCategory, HarpCategory, AdmeCategory, Report
from .forms import ReportForm

def index(request):
    return render(request, 'index.html')

def ypersyndesmos_view(request):
    unclassified_network = DidesCategory.objects.filter(category='unclassified')
    classified_network = DidesCategory.objects.filter(category='classified')
    harp_categories = HarpCategory.objects.all()
    adme_categories = AdmeCategory.objects.all()
    
    context = {
        'unclassified_network': unclassified_network,
        'classified_network': classified_network,
        'harp_categories': harp_categories,
        'adme_categories': adme_categories,
    }
    
    return render(request, 'ypersyndesmos.html', context)

def anafora_aks_ipiresias(request):
    return render(request, 'anafora_aks_ipiresias.html')

def epilochias_view(request):
    return render(request, 'epilochias.html')

def ipiresies_view(request):
    services = Service.objects.all()
    return render(request, 'ipiresies.html', {'services': services})

def report_view(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            # Παραμένουμε στην ίδια σελίδα και προσθέτουμε ένα μήνυμα επιτυχίας
            return render(request, 'anafora_ipiresia.html', {'form': form, 'success': True})
    else:
        form = ReportForm()
    return render(request, 'anafora_ipiresia.html', {'form': form})

def render_to_pdf(template_src, context_dict={}):
    template = render_to_string(template_src, context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(template, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + template + '</pre>')
    return response

def download_pdf(request, pk):
    report = Report.objects.get(pk=pk)
    context = {'report': report}
    return render_to_pdf('anafora_ipiresia.html', context)