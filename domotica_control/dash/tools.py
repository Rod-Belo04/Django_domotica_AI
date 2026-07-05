from openai import OpenAI
import requests
from .data_process import get_sensor_data

tools = [
    {
        "type": "function",
        "name": "change_tapp_pos",
        "description": (
            "Change the global curtain/shutter position. The position must be an exact value "
            "from 0 to 100, where 0 means fully open and 100 means fully closed. If the user "
            "asks to open the curtains, use 0. If the user asks to close them, use 100. If the "
            "user gives an unclear amount such as 'a little' or 'partially', ask for a specific "
            "value from 0 to 100 instead of calling this function."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "position": {
                    "type": "integer",
                    "description": "Curtain position from 0 fully open to 100 fully closed.",
                    "minimum": 0,
                    "maximum": 100,
                }
            },
            "required": ["position"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "start_irrigation",
        "description": (
            "Start the irrigation system immediately. The system only supports turning "
            "irrigation on now. It does not support scheduling, durations, or stopping. If the "
            "user asks for a duration or schedule, explain that only immediate start is supported "
            "and ask whether they want to start irrigation now."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_temp",
        "description": "Get the latest temperature value from the database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_irrigation_date",
        "description": "Get the date and time of the latest irrigation reading from the database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_electric_consumption",
        "description": "Get the latest electric consumption value from the database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


'''dice al microcontrollore di cambiare la posizione delle tapparelle. Se l'utente non specifica
una posizione precisa, ma dice cose come "apri/chiudi le tapparelle", il valore inviato sara
0(aperto) oppure 100(chiuso). Se l'utente indica una quantita vaga, ad esempio "apri le tapparelle poco",
il modello deve chiedere un valore specifico da 0 a 100, senza chiamare questa funzione'''
def change_tapp_pos(position: int):
    if position < 0 or position > 100:
        return "Invalid"
    try:
        response = requests.post("rimpiazza_con_tuo_ip", data={"position": position}, timeout=0.8)
    except requests.RequestException:
        return "Failed"
    return "Success" if response.status_code == 200 else "Failed" 


'''dice al microcontrollore di avviare il sistema di irrigazione. Il sistema attuale non supporta
schedulazione, durata dell'irrigazione o altre funzioni oltre all'accensione. Se l'utente dice
"irriga per 10 minuti", l'AI deve spiegare che l'unico comando supportato e l'avvio immediato
del sistema, e deve chiedere di nuovo all'utente se vuole avviarlo o no'''
def start_irrigation():
    try:
        response = requests.post("rimpiazza_con_tuo_ip", data={"start": True}, timeout=0.8)
    except requests.RequestException:
        return "Failed"
    return "Success" if response.status_code == 200 else "Failed"

'''mostra l'ultimo valore di temperatura salvato nel database'''
def get_temp():
    temp = get_sensor_data()
    return temp['ult_temp'].Temperatura

'''mostra la data dell'ultima irrigazione salvata nel database'''
def get_irrigation_date():
    irrigation_data = get_sensor_data()
    return irrigation_data['ult_Irrigazione'].Data

'''mostra l'ultimo valore di consumo elettrico salvato nel database'''
def get_electric_consumption():
    consumption_data = get_sensor_data()
    return consumption_data['ult_ConsumoElettrico'].Consumo
