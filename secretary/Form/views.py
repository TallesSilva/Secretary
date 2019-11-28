from django.shortcuts import render
from .forms import ContactForm

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form)
            pass  # does nothing, just trigger the validation
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})



