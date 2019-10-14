from django.http import HttpResponse
from django.template import loader

from .models import Task


def index(request):
    latest_task_list = Task.objects.order_by('descricao')
    template = loader.get_template('schedule/index.html')
    context = {
        'latest_task_list': latest_task_list,
    }
    return HttpResponse(template.render(context, request))
