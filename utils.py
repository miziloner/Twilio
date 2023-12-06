
import pandas as pd
from twilio.rest import Client
from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,PHONE_NUMBER,API_KEY_WAPI
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime
import pytz

#Function to cast epoch unix to timestamp Json fields
def epoch_to_mexico_timestamp(epoch_time, daylight_saving=True):
    try:
        mexico_timezone = pytz.timezone('America/Mexico_City')
        utc_datetime = datetime.utcfromtimestamp(epoch_time)
        mexico_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(mexico_timezone)
        timestamp_str = mexico_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
        return timestamp_str
    except Exception as e:
        return f"Error: {e}"

def get_date():
    input_date = datetime.now().strftime("%Y-%m-%d")
    return input_date

def request_wapi(api_key,query):
    url_clima = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}'
    try :
        response = requests.get(url_clima).json()
    except Exception as e:
        print(e)
    return response

def get_forecast(response):
    fecha = epoch_to_mexico_timestamp(response["dt"]).split()[0]
    amanecer = epoch_to_mexico_timestamp(response["sys"]["sunrise"]).split()[1]
    atardecer = epoch_to_mexico_timestamp(response["sys"]["sunset"]).split()[1]
    temp = round(response["main"]["temp"]-273.15,1)
    sensacion = round(response["main"]["feels_like"]-273.15,1)
    min = round(response["main"]["temp_min"]-273.15,1)
    max = round(response["main"]["temp_max"]-273.15,1)
    fecha,amanecer,atardecer,temp,sensacion,min,max
    datos = [{"Ciudad":query ,\
              "Fecha":fecha,\
              "Amanecer" : amanecer,\
              "Atardecer":atardecer,\
              "Temperarura":temp,\
              "Sensación":sensacion,\
              "Mínima":min,\
              "Máxima":max}]
    df = pd.DataFrame(datos)
    df_transposed = df.transpose()
    return df_transposed

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df,query):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body='\nHola ! \n\n\n El pronostico para el dia de hoy '+ input_date +' en ' + query +' es : \n\n\n ' + str(df),
                        from_=PHONE_NUMBER,
                        to='+xxxxxxx'
                    )

    return message.sid
