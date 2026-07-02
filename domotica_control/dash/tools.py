from openai import OpenAI
import requests
from .data_process import get_sensor_data

tools = [{
    
}]


'''tells the microcontroller to change the position of the tapparelle, if the user does not specify a
specific position, and instead says things like "apri/chiudi le tapparelle", then the value to be sent 
will be either 0(open) or 100(closed). If the user gives a "broad" range, like "apri le tapparelle poco,
 then the model must ask the user a specific value from 0 to 100, without calling this function'''
def change_tapp_pos(position: int):
    try:
        response = requests.post("http://192.168.1.100/tapp_control", data={"position": position}, timeout=0.8)
    except requests.RequestException:
        return "Failed"
    return "Success" if response.status_code == 200 else "Failed" 


'''Tells the microcontroller to start the irrigation system. The current system does not support scheduling
or irrigation duration (or any other function other than turning it on), so if the user says "irriga per 10 minuti" then the AI will tell the user that 
the only supported command is to turn on the system, and will have to ask the user again if they
want to turn it on or not'''
def start_irrigation():
    try:
        response = requests.post("http://192.168.1.100/irrigation", data={"start": True}, timeout=0.8)
    except requests.RequestException:
        return "Failed"
    return "Success" if response.status_code == 200 else "Failed"

'''displays the latest temperature value from the database'''
def get_temp():
    temp = get_sensor_data()
    return temp['ult_temp'].Temperatura

'''displays the latest irrigation date from the database'''
def get_irrigation_date():
    irrigation_data = get_sensor_data()
    return irrigation_data['ult_Irrigazione'].Data

'''displays the latest electric consumption value from the database'''
def get_electric_consumption():
    consumption_data = get_sensor_data()
    return consumption_data['ult_ConsumoElettrico'].Consumo