from django.http import HttpResponse
from django.template import loader

from .models import Task, TimeTable, Supplier
from tablib import Dataset

def index(request):
    latest_task_list = Task.objects.order_by('descricao')
    
    template = loader.get_template('schedule/index.html')
    qtd_equipe = Supplier.objects.count()
    qtd_finalizadas = TimeTable.objects.filter(status = 'Finalizados').count()
    qtd_backlog = TimeTable.objects.filter(status='Backlog').count()
    qtd_confirmados = TimeTable.objects.filter(status='Confirmado').count()
    qtd_reagendados = TimeTable.objects.filter(status='Reagendado').count()
    qtd_inconclusivos = TimeTable.objects.filter(status='Inconclusivo').count()
    qtd_cancelados_cli = TimeTable.objects.filter(status='Revogados').count()
    qtd_cancelados_sis = TimeTable.objects.filter(status='Interrompidas').count()
    qtd_execucao = TimeTable.objects.filter(status='Acontecendo').count()
    qtd_pendentes = qtd_backlog + qtd_confirmados + qtd_reagendados + qtd_inconclusivos + qtd_execucao
    qtd_canceladas = qtd_cancelados_cli + qtd_cancelados_sis
    

    context = {
        'latest_task_list': latest_task_list,
        'qtd_equipe' : qtd_equipe,
        'qtd_pendentes' : qtd_pendentes,
        'qtd_finalizadas' : qtd_finalizadas,
        'qtd_canceladas' : qtd_canceladas,
        'qtd_execucao' : qtd_execucao,
        'qtd_backlog': qtd_backlog,
        'qtd_confirmados': qtd_confirmados,
        'qtd_reagendados': qtd_reagendados,
        'qtd_inconclusivos': qtd_inconclusivos,
        'qtd_cancelados_cli': qtd_cancelados_cli,
        'qtd_cancelados_sis': qtd_cancelados_sis, 
    }
    return HttpResponse(template.render(context, request))

def impt_backlog(request):
    template = loader.get_template('schedule/impt_backlog.html')
    context = {
    }
    return HttpResponse(template.render(context, request))




def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')