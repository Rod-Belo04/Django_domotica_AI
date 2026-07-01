from django.shortcuts import render
from .models import Thermo, Irrigazione, ConsumoElettrico


''' questo file legge il DB e restituisce i dati che verranno poi passati
    contesto nella pagina web home, che poi verrà visualizzato dall'utente'''
def get_sensor_data():
    ult_temp = Thermo.objects.last()
    ult_Irrigazione = Irrigazione.objects.last()
    ult_ConsumoElettrico = ConsumoElettrico.objects.last()
    return {
        'ult_temp': ult_temp,
        'ult_Irrigazione': ult_Irrigazione,
        'ult_ConsumoElettrico': ult_ConsumoElettrico
    }
