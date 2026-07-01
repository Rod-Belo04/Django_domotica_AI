from django.http import HttpResponse
from django.shortcuts import render
from .models import Thermo, Irrigazione, ConsumoElettrico
from django.utils import timezone
from . import data_process

def home(request):
    sensor_data = data_process.get_sensor_data()
    return render(request, 'dash/home.html', sensor_data) #i dat dei sensori, definiti nel file data_process


''' questa funzione gestisce le richieste POST mandate dai microcontrollori smart
    e le immagazzina nel DB, restituisce un messaggio HTTP se i dati risultano congrui,
    altrimenti restituisce un codice errore. Se si vuole aggiungere o cambiare un dato, è
    consigliato cambiare i modelli e apportare le modifiche a questo file ed al file 
    utility data_process.py
'''
def post(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        if field == 'thermo':
            temp = float(request.POST.get('temp'))
            date = timezone.now()
            Thermo.objects.create(Temperatura=temp, Data=date)
            return HttpResponse("OK", status=200)
        elif field == 'irrigazione':
            status = request.POST.get('status') == 'true'
            date = timezone.now()
            Irrigazione.objects.create(valido=status, Data=date)
            return HttpResponse("OK", status=200)
        elif field == 'consumo_elettrico':
            power = float(request.POST.get('power'))
            date = timezone.now()
            ConsumoElettrico.objects.create(Consumo=power, Data=date)
            return HttpResponse("OK", status=200)
        
    return HttpResponse("Errore", status=405)


