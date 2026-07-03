import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Thermo, Irrigazione, ConsumoElettrico
from django.utils import timezone
from . import data_process
from . import tools
from openai import OpenAI
client = OpenAI()

def home(request, ai_message=''):
    page_data = data_process.get_sensor_data()
    page_data['ai_message'] = ai_message  # Aggiungi il messaggio AI al contesto della pagina
    return render(request, 'dash/home.html', page_data) #i dat dei sensori, definiti nel file data_process


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


'''questa funzione gestisce le richieste POST provenienti dagli user che usano le funzioni AI,
la richiesta POST contiene il messaggio dell' utente, che poi viene passato al modello AI che 
la elabora e chiama un tool e/o fornisce una risposta.'''
def ai_calls(request):
    if request.method == 'POST':
        messaggio_utente = request.POST.get('ai_request')
        if messaggio_utente == "":
            return redirect('home', ai_message="Errore: richiesta AI vuota.")
        response = client.responses.create(
            model="gpt-5.4-mini",
            tools=tools.tools,
            input=messaggio_utente
        )
        for item in response.output:
            if item.type == 'function_call':
                if item.name == 'change_tapp_pos':
                    args = json.loads(item.arguments)
                    position = int(args["position"])
                    tools.change_tapp_pos(position)
                    ai_message = f"Posizione tapparelle cambiata a {position}."
                if item.name == 'start_irrigation':
                    result = tools.start_irrigation()
                    ai_message = f"Irrigazione avviata. Risultato: {result}"
                if item.name == 'get_temp':
                    temperature = tools.get_temp()
                    ai_message = f"La temperatura attuale e {temperature}."
                if item.name == 'get_irrigation_date':
                    irrigation_date = tools.get_irrigation_date()
                    ai_message = f"L'ultima irrigazione risale a {irrigation_date}."
                if item.name == 'get_electric_consumption':
                    consumption = tools.get_electric_consumption()
                    ai_message = f"Il consumo elettrico attuale e {consumption} Kw."
                return home(request, ai_message=ai_message)
            elif item.type == 'message':
                ai_message = item.content[0].text
                return home(request, ai_message=ai_message)
    return home(request, ai_message="Errore nella richiesta AI.")
        


