import json
import os

from urllib.request import urlopen
from contextlib import closing
from twilio.rest import Client


api_key = os.environ['API_KEY']
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'] )
recipients = ['+14152715288']

def check_stock(symbol, lowerbound, upperbound, volume_limit):
    with closing(urlopen("https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={apikey}".format(symbol=symbol, apikey=api_key))) as responseData:
        jsonData = responseData.read()
        deserialisedData = json.loads(jsonData)[0]
        price = deserialisedData['price']
        print("The price for {symbol} is ${price}".format(symbol=symbol, price=price))

        if price < lowerbound:   
            notify_recipients("The price for {symbol} is ${price}, which exceeds the lower bound of ${lowerbound}".format(symbol=symbol, price=price, lowerbound=lowerbound))
            return

        if price > upperbound:   
            notify_recipients("The price for {symbol} is ${price}, which exceeds the upper bound of ${upperbound}".format(symbol=symbol, price=price, upperbound=upperbound))
            return
        
        volume = deserialisedData['volume']
        if volume > volume_limit:
            notify_recipients("The volume for {symbol} is {volume}, which exceeds the volume limit of {volume_limit}".format(symbol=symbol, volume=volume, volume_limit=volume_limit))
            return


def send_sms(recipient, msg):
    try:
        message = client.messages.create(body=msg, from_='+16028334820', to=recipient)
        print("Message sent to {recipient} {message_sid}".format(recipient=recipient, message_sid=message.sid))
    except:
        print("Unable to send message to {recipient}".format(recipient=recipient))

def notify_recipients(msg):
    for recipient in recipients:
        send_sms(recipient, msg)


def lambda_handler(event, context):
    check_stock("GME", 0, 400, 100000000)
    check_stock("AMC", 0, 30, 600000000)

