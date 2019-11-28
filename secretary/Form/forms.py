from django import forms

class ContactForm(forms.Form):
    Nome = forms.CharField(label='Seu nome',
                       max_length=100,
                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    Assunto = forms.CharField(label='Assunto *',
                       max_length=100,
                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    Pergunta = forms.CharField(label='Pergunta *',
                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    Resposta = forms.CharField(label='Resposta *',
                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        Nome = cleaned_data.get('Nome')
        Assunto = cleaned_data.get('Assunto')
        Pergunta = cleaned_data.get('Pergunta')
        Resposta = cleaned_data.get('Resposta')
        if not Nome and not Assunto and not Pergunta and not Resposta:
            raise forms.ValidationError('You have to write something!')