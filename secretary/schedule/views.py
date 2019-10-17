from django.http import HttpResponse
from django.template import loader
import openpyxl
from .models import Task, TimeTable, Supplier
from tablib import Dataset
from django.shortcuts import render

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
    qtd_pendentes = qtd_confirmados + qtd_reagendados + qtd_inconclusivos + qtd_execucao
    qtd_canceladas = qtd_cancelados_cli + qtd_cancelados_sis
    AgendamentoAutomatico = False

    context = {
        'AgendamentoAutomatico' : AgendamentoAutomatico,
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

def ImportBacklog(request):
    template = loader.get_template('schedule/ImportBacklog.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def AgendamentoAutomatico(request):
    template = loader.get_template('schedule/index.html')
    latest_task_list = Task.objects.order_by('descricao')
    qtd_equipe = Supplier.objects.count()
    qtd_finalizadas = TimeTable.objects.filter(status = 'Finalizados').count()
    qtd_backlog = TimeTable.objects.filter(status='Backlog').count()
    qtd_confirmados = TimeTable.objects.filter(status='Confirmado').count()
    qtd_reagendados = TimeTable.objects.filter(status='Reagendado').count()
    qtd_inconclusivos = TimeTable.objects.filter(status='Inconclusivo').count()
    qtd_cancelados_cli = TimeTable.objects.filter(status='Revogados').count()
    qtd_cancelados_sis = TimeTable.objects.filter(status='Interrompidas').count()
    qtd_execucao = TimeTable.objects.filter(status='Acontecendo').count()
    qtd_pendentes = qtd_confirmados + qtd_reagendados + qtd_inconclusivos + qtd_execucao
    qtd_canceladas = qtd_cancelados_cli + qtd_cancelados_sis
    AgendamentoAutomatico = True
    context = {
        'AgendamentoAutomatico' : AgendamentoAutomatico,
        'AgendamentoAutomatico' : AgendamentoAutomatico,
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

def UploadBacklog(request):
    template = loader.get_template('schedule/ImportBacklog.html')
    context = {
    }

    if "GET" == request.method:
        print('get')
        return HttpResponse(template.render(context, request))
    else:
        print('post')

        excel_file = request.FILES["excel_file"]
        
        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb.active
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
                print(cell)
            excel_data.append(row_data)
        return HttpResponse(template.render(context, request))