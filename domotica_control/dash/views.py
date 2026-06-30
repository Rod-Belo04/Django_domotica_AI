from django.shortcuts import render
from .models import Thermo, Irrigazione, ConsumoElettrico
import datetime

def home(request):
    return render(request, 'dash/home.html')
def post(request):
    if request.method == 'POST':
        field = request.POST.get('field')
        if field == 'thermo':
            temp = request.POST.get('temp')
            date = datetime.datetime.now()
            Thermo.objects.create(temperature=temp, date=date)
        elif field == 'irrigazione':
            status = request.POST.get('status')
            date = datetime.datetime.now()
            Irrigazione.objects.create(status=status, date=date)
        elif field == 'consumo_elettrico':
            power = request.POST.get('power')
            date = datetime.datetime.now()
            ConsumoElettrico.objects.create(power=power, date=date)


