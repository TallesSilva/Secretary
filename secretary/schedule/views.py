from django.http import HttpResponse
from django.template import loader
import openpyxl
from .models import Task, TimeTable, Supplier, Backlog
from tablib import Dataset
from django.shortcuts import render
from scheduler_agent.manage_backlog import *


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

def Calendario(request):
    template = loader.get_template('schedule/calendario.html')

    suppliers = Supplier.objects.order_by('nome')
    context = {

        'suppliers': suppliers,

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
        ws = wb.active
        row, column = excel.max_row_column(ws)
        for r in range(1, row+1):
            customer = excel.read_cell(ws, r, 1)
            supplier = excel.read_cell(ws, r, 2)
            task = excel.read_cell(ws, r, 3)
            start_date = excel.read_cell(ws, r, 4)
            if start_date is None:
                payload = Manage.generate_none_payload_visit(customer, supplier, task)
            else:
                end_date = Manage.date_sum_hour(start_date, 1)
                payload = Manage.generate_available_payload_visit(customer, supplier, 'Backlog', 'Instalação de Modem', start_date, end_date)
            ''' inserir data in mongo '''
            Backlog.objects.filter(payload).update_one()

        # getting a particular sheet by name out of many sheets
        return HttpResponse(template.render(context, request))