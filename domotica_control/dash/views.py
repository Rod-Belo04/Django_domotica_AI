from django.http import HttpResponse
from django.shortcuts import render
from .models import Thermo, Irrigazione, ConsumoElettrico
from django.utils import timezone

def home(request):
    return render(request, 'dash/home.html')

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


