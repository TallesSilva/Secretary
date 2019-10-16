from __future__ import print_function
import datetime
import pickle
import os.path
from os import remove
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS = 'scheduler_agent/credentials.json'

def clean_up(exception):
    print("Uma exceção foi lançada:\n{} Os arquivos de credenciais foram "
          "apagados. O arquivo `credentials.json` deve ser buscado novamente"
          "".format(exception))
    remove('token.pickle')
    setup_interface()
        

def setup_interface():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as ex:
        clean_up(ex)

def date_to_str(date):
        return date.strftime("%Y-%m-%dT%H:%M:%S")

def fill_event_document(customer: dict,
                       start_date: str,
                       end_date: str):
    return {
        'summary': 'Visita técnica',
        'location': customer.get("address"),
        'description': 'Visita técnica à casa de um {}'.format(customer.get("name")),
        'start': {
            'dateTime': start_date,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_date,
            'timeZone': 'America/Sao_Paulo',  
        },
    }
    
def create_event(customer, start_date):
    service = setup_interface()
    
    end_date = date_to_str(start_date + datetime.timedelta(minutes=30))
    start_date = date_to_str(start_date)
    
    event = fill_event_document(customer, start_date, end_date)
    try:
        service.events().insert(calendarId='primary', body=event).execute()
    except Exception as ex:
        raise