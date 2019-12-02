import requests
import openpyxl

from django.http import HttpResponse
from django.template import loader
from .models import Task, TimeTable, Supplier, Backlog, Customer
from tablib import Dataset
from django.shortcuts import render
from scheduler_agent.manage_backlog import *
from datetime import datetime, timedelta
from json import loads, dumps
from django.utils.timezone import datetime,timedelta


def index(request):
    '''           LOAD PAGE          '''
    latest_task_list = Task.objects.order_by('descricao')
    
    template = loader.get_template('schedule/index.html')
    qtd_equipe = Supplier.objects.count()
    qtd_finalizadas = TimeTable.objects.filter(status = 'Finalizada').count()
    qtd_backlog = Backlog.objects.count()
    qtd_Perguntadentes = TimeTable.objects.filter(status='Pendente').count()
    qtd_pendentes = qtd_confirmados + qtd_reagendados + qtd_inconclusivos + qtd_execucao + qtd_pendentes
    qtd_canceladas = qtd_cancelados_cli + qtd_cancelados_sis
    AgendamentoAutomatico = False
    dpToday = datetime.today().strftime( "%d %b")
    dpYesterday = (datetime.today() - timedelta(days=1)).strftime( "%d %b")
    dpWeek = (datetime.today() - timedelta(days=int(datetime.today().strftime( "%w")))).strftime( "%d") + ' - ' + datetime.today().strftime( "%d %b")
    dpMonth = '1' + ' - ' + datetime.today().strftime( "%d %b")
    dpYear = datetime.today().strftime( "%Y")

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
        'dpToday': dpToday,
        'dpYesterday': dpYesterday,
        'dpWeek': dpWeek,
        'dpMonth': dpMonth,
        'dpYear': dpYear,
    }
    return HttpResponse(template.render(context, request))

def ImportBacklog(request):
    '''           LOAD PAGE          '''
    template = loader.get_template('schedule/ImportBacklog.html')
    status_import = ''
    backlogs = Backlog.objects()
    des_deadline = '["' + datetime.today().strftime("%d-%m-%Y") + '" , " ' + ((datetime.today() + timedelta(days=7)).strftime("%d-%m-%Y") ) + '"]'
    [13-11-2019 , 20-11-2019]
    ["01-10-2019", "31-10-2019"]
    print(des_deadline)
    context = {
        'backlogs': backlogs,
        'status_import': status_import,
        'des_deadline' : des_deadline
    }
    return HttpResponse(template.render(context, request))

def Calendario(request):
    '''           LOAD PAGE          '''
    template = loader.get_template('schedule/Calendario.html')

    suppliers = Supplier.objects.order_by('nome')
    timetables = TimeTable.objects()

    json_calendario = '['
    i = 1
    for timetable in timetables:
        json_calendario = json_calendario + '{'
        json_calendario = json_calendario + '"title": "' + timetable.task + '",'
        json_calendario = json_calendario + '"start": "' + timetable.start_date + '",'
        json_calendario = json_calendario + '"end": "' + timetable.end_date + '",'
        if timetable.status == 'Confirmado' or timetable.status == 'Reagendado' :
            json_calendario = json_calendario + '"textColor": "rgb(0, 162, 138)",'
            json_calendario = json_calendario + '"backgroundColor": "rgba(0, 162, 138, .12)",'
            json_calendario = json_calendario + '"borderColor": "rgb(0, 162, 138)"'
        elif timetable.status == 'Revogado':
            json_calendario = json_calendario + '"textColor": "rgb(183, 107, 163)",'
            json_calendario = json_calendario + '"backgroundColor": "rgba(183, 107, 163, .12)",'
            json_calendario = json_calendario + '"borderColor": "rgb(183, 107, 163)"'
        else:
            json_calendario = json_calendario + '"textColor": "rgb(249, 172, 47)",'
            json_calendario = json_calendario + '"backgroundColor": "rgba(249, 172, 47, .12)",'
            json_calendario = json_calendario + '"borderColor": "rgb(249, 172, 47)"'
            
        
        if i == len(timetables):
            json_calendario = json_calendario + '}'
        else :
            json_calendario = json_calendario + '},'
        
        i = i + 1
    json_calendario = json_calendario +']'

    events = json_calendario
    context = {

        'suppliers': suppliers,
        'teste':events

    }
        
    return HttpResponse(template.render(context, request))

def AgendamentoAutomatico(request):
    '''           LOAD FUNCTION BUTTON ACIONAR CONTACT CLIENT          '''
    try:
        template = loader.get_template('schedule/AgendamentoAutomatico.html')
        context = {
        }
        if "POST" == request.method:
            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('schedule/AgendamentoAutomatico.html')
            context = {
                'Alerta' : False,
            }

            backlogs= Backlog.objects()

            for backlog in backlogs:
                params = {'include_events': 'ALL',
                      'output_channel': 'telegram',
}
                conversation_id = backlog.customer.contato.telegram
                payload = {"name": "utter_greet"}
                backlog_number = str(backlog.id)
                payload_mes = {"text": backlog_number,
                               "sender": "user"}
                r2 = requests.post('http://localhost:5005/conversations/{}/messages'.format(conversation_id),
                                   params = params,
                                   data = dumps(payload_mes))
                r = requests.post('http://localhost:5005/conversations/{}/execute'.format(conversation_id),
                                  params = params,
                                  data = dumps(payload))
                print('AgendamentoAutomatico2') 
                print(backlog.id)

            return HttpResponse(template.render(context, request))
    except NameError:
        print (NameError)
        template = loader.get_template('schedule/Erro.html')
        context = {
            'Alerta' : True,
        }
        return HttpResponse(template.render(context, request))

def UploadBacklog(request):
    '''           LOAD FUNCTION BUTTON UPLOAD EXCEL FILE TO MONGO          '''
    try:
        template = loader.get_template('schedule/UploadBacklog.html')
        context = {
        }
        status_import = ''
        if "GET" == request.method:
            return HttpResponse(template.render(context, request))
        else:
            excel_file = request.FILES["excel_file"]
            date = request.POST['data-default-dates']
            deadline_start_date = datetime.strptime(date[0:10], "%d-%m-%Y")
            deadline_end_date = datetime.strptime(date[-10:], "%d-%m-%Y")
            # you may put validations here to check extension or file size
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            
            row, column = excel.max_row_column(ws)
            for r in range(1, row+1):
                customer = excel.read_cell(ws, r, 1)
                supplier = excel.read_cell(ws, r, 2)
                task = excel.read_cell(ws, r, 3)
                start_date = excel.read_cell(ws, r, 4)
                if start_date is None or start_date == '' :
                    start_date = ''
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
                    deadline_start_date = deadline_start_date.strftime( "%Y-%m-%dT%H"),
                    deadline_end_date = deadline_end_date.strftime( "%Y-%m-%dT%H")
                ).save()
            status_import = 'Success'
            backlogs = Backlog.objects()
            context = {
                'backlogs': backlogs,
                'Alert' : False,
                'status_import': status_import,
            }
            return HttpResponse(template.render(context, request))
    except:
        status_import = 'Success'
        context = {
            'Alerta' : True,
            'status_import': status_import,
        }
        return HttpResponse(template.render(context, request))

def Clientes(request):
    template = loader.get_template('schedule/Clientes.html')

    customers = Customer.objects()

    context = {
        'customers': customers
    }
    return HttpResponse(template.render(context, request))

def Form(request):
    template = loader.get_template('schedule/Form.html')

    customers = Form.objects()

    context = {
        'customers': customers
    }

    return HttpResponse(template.render(context, request))

