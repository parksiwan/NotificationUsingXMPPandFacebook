#!/usr/bin/env python

import sys
import fbchat
from xmpp import *
from pyowm import OWM
#from datetime import datetime
from dateutil import tz


def send_message_facebook(contents, receiver_name):
    """
        Hae Eun Park id : 100001757400874
        Haejung Park id : 100006868175078
        Siwan Park id : 1351875930
    """
    receivers = {'siwan': 1351875930, 'haeeun': 100001757400874, 'haejung': 100006868175078}
    client = fbchat.Client("parksiwan@gmail.com", "Unst3426fx1101ok714")
    sent = client.send(receivers[receiver_name], contents)


def send_message(contents, receiver_name):
    if receiver_name == 'haeeun' or receiver_name == 'haejung':
        send_message_facebook(contents, receiver_name)
        return

    username = 'siwan.park'
    password = 'psw1101714'
    receivers = {'siwan':'parksiwan@gmail.com', 'sujin':'gain0615@gmail.com',
                 'haeeun':'haeeun1999@gmail.com', 'haehung':'haejungrox@gmail.com'}

    client = Client('ubiquoss.com.au')
    client.connect(server=('talk.google.com', 5223), use_srv=False)
    client.auth(username, password, 'botty' )
    client.sendInitPresence()
    message = Message(receivers[receiver_name], contents)
    message.setAttr('type', 'chat')
    client.send(message)


def generate_contents(option, target):
    if option == '1':
        content =  'RE: Rent fee by this week'
	receiver = 'siwan'
    elif option == '2':
        content = 'RE: Report Austudy status to Centrelink by today'
	receiver = 'siwan'
    elif option == '3':
        (content1, content2, content3) = get_current_weather()
        content = 'Good Morning! \n' + 'Current weather is ' + content2 + ' and temperature is ' + content3 \
                  + '\n' + 'at ' + content1 + '\n'
        content = content + forecast_weather()
	receiver = target

    return (content, receiver)


def utc_to_local(reference_time):
    """
    change utc time format to local time
    """
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = reference_time

    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime("%Y-%m-%d %H:%M")


def get_current_weather():
    API_key = '81249d57f1ea44e7d3e41cb62f492156'
    owm = OWM(API_key)
    obs = owm.weather_at_place('Sydney,au')
    w = obs.get_weather()

    forecast_time = utc_to_local(w.get_reference_time(timeformat='date'))
    forecast_details = w.get_detailed_status()
    forecast_temp = w.get_temperature(unit='celsius')['temp']
    return (str(forecast_time), str(forecast_details), str(forecast_temp))


def forecast_weather():
    API_key = '81249d57f1ea44e7d3e41cb62f492156'
    owm = OWM(API_key)
    fc = owm.three_hours_forecast('Sydney,au')
    f = fc.get_forecast()
    forecast = ''
    number_of_forcast = 0
    for weather in f:
        forecast_time = utc_to_local(weather.get_reference_time(timeformat='date'))
        forecast_details = weather.get_detailed_status().encode("utf-8")
        forecast_temp = weather.get_temperature(unit='celsius')['temp']
        forecast = forecast + str(forecast_time) + ' ' + str(forecast_details) + ' ' + str(forecast_temp) + '\n'
        number_of_forcast += 1
        if number_of_forcast == 5:
            break

    return forecast


if __name__ == '__main__':
    (contents, receiver_name) = generate_contents(sys.argv[1], sys.argv[2])
    send_message(contents, receiver_name)
