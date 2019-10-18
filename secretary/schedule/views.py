from django.http import HttpResponse
from django.template import loader
import openpyxl
from .models import Task, TimeTable, Supplier, Backlog
from tablib import Dataset
from django.shortcuts import render
from scheduler_agent.manage_backlog import *
from datetime import datetime


def index(request):
    latest_task_list = Task.objects.order_by('descricao')
    
    template = loader.get_template('schedule/index.html')
    qtd_equipe = Supplier.objects.count()
    qtd_finalizadas = TimeTable.objects.filter(status = 'Finalizada').count()
    qtd_backlog = Backlog.objects.count()
    qtd_confirmados = TimeTable.objects.filter(status='Confirmado').count()
    qtd_reagendados = TimeTable.objects.filter(status='Reagendado').count()
    qtd_inconclusivos = TimeTable.objects.filter(status='Inconclusivo').count()
    qtd_cancelados_cli = TimeTable.objects.filter(status='Revogados').count()
    qtd_cancelados_sis = TimeTable.objects.filter(status='Interrompida').count()
    qtd_execucao = TimeTable.objects.filter(status='Acontecendo').count()
    qtd_pendentes = TimeTable.objects.filter(status='Pendente').count()
    qtd_pendentes = qtd_confirmados + qtd_reagendados + qtd_inconclusivos + qtd_execucao + qtd_pendentes
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
    qtd_backlog = Backlog.objects.count()
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
    try:
        template = loader.get_template('schedule/ImportBacklog.html')
        context = {
        }
        if "GET" == request.method:
            return HttpResponse(template.render(context, request))
        else:
            excel_file = request.FILES["excel_file"]
            # you may put validations here to check extension or file size
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            print(ws)
            row, column = excel.max_row_column(ws)
            for r in range(1, row+1):
                customer = excel.read_cell(ws, r, 1)
                supplier = excel.read_cell(ws, r, 2)
                task = excel.read_cell(ws, r, 3)
                start_date = excel.read_cell(ws, r, 4)
                if start_date is None:
                    start_date = None
                else:
                    start_date = start_date.strftime( "%Y-%m-%dT%H")
                    '''inserir data in mongo '''
                Backlog(
                    start_date = start_date,
                    status = 'backlog',
                    task = task,
                    supplier = supplier,
                    customer = customer,
                    company = '5d6020abd12e66a47a7888ed',
                    observacao = None,
                ).save()
            context = {
                'Alert' : False,
            }
            return HttpResponse(template.render(context, request))
    except:
        context = {
            'Alerta' : True,
        }
        return HttpResponse(template.render(context, request))

def GerarTimetable(request):
    try:
        if "POST" == request.method:
            print('aqui')
            return HttpResponse(template.render(context, request))
        else:
            
            template = loader.get_template('schedule/ImportBacklog.html')
            context = {
                'Alerta' : False,
            }
            date = request.GET['data-default-dates']
            start_date = datetime.strptime(date[0:10], "%Y-%m-%d")
            end_date = datetime.strptime(date[-10:], "%Y-%m-%d")
            excel.generate_timetable_with_backlog(start_date, end_date)
            return HttpResponse(template.render(context, request))
    except:
        template = loader.get_template('schedule/ImportBacklog.html')
        context = {
            'Alerta' : True,
        }
        return HttpResponse(template.render(context, request))

