from django.http import HttpResponse
from django.template import loader
import openpyxl
from .models import Task, TimeTable, Supplier, Backlog, Customer
from tablib import Dataset
from django.shortcuts import render
from scheduler_agent.manage_backlog import *
from datetime import datetime
import requests
from json import loads, dumps
from django.utils.timezone import datetime,timedelta


def index(request):
    '''           LOAD PAGE          '''
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
    print('ImportBacklog')
    '''           LOAD PAGE          '''
    template = loader.get_template('schedule/ImportBacklog.html')
    status_import = ''
    backlogs = Backlog.objects()
    context = {
        'backlogs': backlogs,
        'status_import': status_import,
    }
    return HttpResponse(template.render(context, request))

def Calendario(request):
    '''           LOAD PAGE          '''
    template = loader.get_template('schedule/Calendario.html')

    suppliers = Supplier.objects.order_by('nome')

    events = [
  {
    "title": "Trocar Modem",
    "start": "2019-11-18",
    "textColor": "rgb(52, 108, 176)",
    "backgroundColor": "rgba(52, 108, 176, .12)",
    "borderColor": "rgb(52, 108, 176)"
  }
]

    context = {

        'suppliers': suppliers,
        'teste':events

    }
        
    return HttpResponse(template.render(context, request))

def AgendamentoAutomatico(request):
    print('AgendamentoAutomatico')
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
                payload_mes = {"text": str(backlog.id),
                               "sender": "user"}
                r = requests.post('http://192.168.0.190:5005/conversations/{}/execute'.format(conversation_id),
                                  params = params,
                                  data = dumps(payload))
                r2 = requests.post('http://192.168.0.190:5005/conversations/{}/messages'.format(conversation_id),
                                   params = params,
                                   data = dumps(payload_mes))
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
    print('UploadBacklog')
    '''           LOAD FUNCTION BUTTON UPLOAD EXCEL FILE TO MONGO          '''
    try:
        template = loader.get_template('schedule/ImportBacklog.html')
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
            print(deadline_start_date)
            print(deadline_end_date)
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



   



    


