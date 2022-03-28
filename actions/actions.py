import datetime
from datetime import date, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.events import Restarted
from rasa_sdk.events import AllSlotsReset
import os
import requests
import json
#url = "http://172.16.1.72/webservice-php-json/index.php"

url = "https://bot.movatec.cl/webservice-php-json/index.php"

global SiPaga
global NoPaga
global motivo
global tipo_contacto
global compromiso_p
global derivacion
global fecha_com
global entrega_info
SiPaga=None
NoPaga=None
motivo=None
tipo_contacto=0
compromiso_p=0
derivacion=None
fecha_com=None
entrega_info=None

def month_converter(i):
       month = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
       return month[i]


def ConverterDate():
     global mes
     global dia
     global anio
     global nombreMes 
     global hora
     now = datetime.datetime.now()
     dia=now.day
     mes=now.month
     anio=now.year
     nombreMes=month_converter(mes-1)
     hora=f'{now.hour}:{now.minute}'
     
def Querys(uniqueid):
        payload={'action': 'get','id': f'{uniqueid}'}
        files=[
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        my_bytes_value = response.content
        my_new_string = my_bytes_value.decode("utf-8").replace("'", '"')
        data = json.loads(my_new_string)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        global nombre
        global monto
        global fechaVencimiento
        global primernombre
        global rut
        global campania
        nombre=data["data"][0]["address1"]
        monto=data["data"][0]["address2"]
        fechaVencimiento=data["data"][0]["city"]
        primernombre=data["data"][0]["first_name"]
        rut=data["data"][0]["vendor_lead_code"]
        campania=data["data"][0]["campaign_name"]

"""
            "address1": "DANIELA HERNANDEZ",
            "address2": "26799",
            "campaign_name": "CLICK RECORDATORIO",
            "city": "28-02-21",
            "email": "",
            "first_name": "DANIELA",
            "lead_id": "134",
            "list_name": "CLICK RECORDATORIO",
            "owner": "78574270",
            "vendor_lead_code": "170099999"
"""

"""
curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/asdfasdfasdf

curl -XPOST http://localhost:5005/webhooks/rest/webhook   -H "Content-type: application/json"   -d '{"sender": "test", "message": "ok"}'

headers = {
    'Content-type': 'application/json',
}

data = '{"text":"Hello, World!"}'
data = '{"sender": "test", "message": "alo"}'

response = requests.post('https://hooks.slack.com/services/asdfasdfasdf', headers=headers, data=data)
response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
"""
def Updates(tipo_contacto,motivo,compromiso_p,derivacion,fecha_com,entrega_info,lead_id,rut):
          payload={'action': 'update',
          'tipo_contacto': f'{tipo_contacto}',
          'motivo': f'{motivo}',
          'compromiso_p': f'{compromiso_p}',
          'derivacion': f'{derivacion}',
          'fecha_com': f'{fecha_com}',
          'entrega_info': f'{entrega_info}',
          'lead_id': f'{lead_id}',
          'rut': f'{rut}'}
          files=[
          ]
          headers = {}
          response = requests.request("POST", url, headers=headers, data=payload, files=files)
          print(response.text)

class ActionHello(Action):
    def name(self):
        return "action_hello"
       
    def run(self, dispatcher, tracker, domain):
        global uniqueid
        uniqueid = tracker.sender_id
        t = datetime.datetime.now()
        if 23 >= int(t.hour) >= 12:
             dispatcher.utter_message(f'Buenas tarde, mi nombre es evva y soy un bot creado por movatec. Estoy entrenada para realizar varios procesos ¿Te gustaría una demostración? ')
        else:
             dispatcher.utter_message(f'Buenos días, mi nombre es evva y soy un bot creado por movatec. Estoy entrenada para realizar varios procesos ¿Te gustaría una demostración?')
        headers2 = {'Content-type': 'application/json'}
        data2 = '{"sender": f"test", "message": "alo"}'
        response2 = requests.post('http://10.3.0.5:5013/webhooks/rest/webhook', headers=headers2, data=data2)
        print(response2.text)
        #dispatcher.utter_message(response2.text)
        return []

class Consulta(Action):
    def name(self):
        return "action_ask_question"

    def run(self, dispatcher, tracker, domain):
        
        dispatcher.utter_message(f'Podría, por ejemplo, enviarte nuestra presentación a través de whatsApp, o correo electrónico. ¿Cuál prefieres?')
        return []


############################################################################################
###################################### Celular #############################################
############################################################################################

class ContactoCelular(Action):
    def name(self):
        return "action_dejar_mismo_contacto_celular"

    def run(self, dispatcher, tracker, domain):
      
        dispatcher.utter_message(f'Quieres que te contactemos a este mismo número? ')
        return []

class Contacto1(Action):
    def name(self):
        return "action_dejar_otro_contacto_celular"

    def run(self, dispatcher, tracker, domain):
        
        dispatcher.utter_message(f'Indicame el número al que desees que la enviemos')
        return []


class ActionRepetirNumero2(Action):

    def name(self) -> Text:
        return "action_el_numero_seria"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global uniqueid
        uniqueid = tracker.sender_id
        #numero = tracker.get_slot("numero")
        print("numero: ", uniqueid)
        dispatcher.utter_message(text=f"El numero sería {uniqueid}, estoy en lo correcto? ")
        return []

class ActionRepetirNumero3(Action):

    def name(self) -> Text:
        return "action_repiteme_numero"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global uniqueid
        uniqueid = tracker.sender_id
        dispatcher.utter_message(text=f"Uf! disculpa, repite el numero nuevamente ")
        return []




global numero
class ActionGuardarNumero(Action):

    def name(self) -> Text:
        return "action_te_enviamos_en_breve"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        #numero = tracker.get_slot("numero")
        global uniqueid
        uniqueid = tracker.sender_id
        print("numero: ", uniqueid)
        import requests
        #url2 = 'http://localhost:5002/webhooks/rest/webhook'
        #myobj = {'sender': 'test', 'message': 'alo'}
        #x = requests.post(url2, data = myobj)
        #print(x.text)
        dispatcher.utter_message(text=f"Ok! archivo enviado al numero {uniqueid} | WSP")
        return []


############################################################################################
###################################### Email ###############################################
############################################################################################


class ActionEmail(Action):

    def name(self) -> Text:
        return "action_dar_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=f"El correo que ingresaste en nuestra web es ,es correcto?")
        return []


class ActionEnviarEmail(Action):

    def name(self) -> Text:
        return "action_email_enviado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text=f"Ok! la infomación ah sido enviada")
        return []



class ActionRepetirEmail(Action):

    def name(self) -> Text:
        return "action_repiteme_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        uniqu
        dispatcher.utter_message(text=f"Uf! disculpa, me podrías indicar el correo nuevamente?")
        return []

global email
class ActionRecibirEmail(Action):

    def name(self) -> Text:
        return "action_dar_email2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        print("email: ", email)
        dispatcher.utter_message(text=f"El correo que ingresaste es {email}, es correcto?")
        return []

############################################################################################
###################################### Fecha y Hora ########################################
############################################################################################

class Fecha(Action):
    def name(self):
        return "action_fecha"

    def run(self, dispatcher, tracker, domain):
        ConverterDate()
        dispatcher.utter_message(f'Estamos a {dia} de {nombreMes} del {anio}')
        return []

class ActionDarHora(Action):
    def name(self):   
        return "action_dar_hora"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ConverterDate()
        t = datetime.datetime.now()
        if 23 >= int(t.hour) >= 12:
             t2 = "PM"
        else:
             t2 = "AM"
        dispatcher.utter_message(text=f"Son las {hora} {t2}, a que hora quieres que te contactemos?")
        
        return []

###############################################
################### Restart ###################
###############################################

class ActionRestart2(Action):
    """Resets the tracker to its initial state.
    Utters the restart template if available."""

    def name(self) -> Text:
        return "action_restart2"

    async def run(self, dispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [Restarted()]

class ActionSlotReset(Action):  
    def name(self):         
        return 'action_slot_reset'  
    def run(self, dispatcher, tracker, domain):
        return[AllSlotsReset()]
