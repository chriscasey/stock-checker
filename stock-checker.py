import json
import os
import boto3

from urllib.request import urlopen
from contextlib import closing
from twilio.rest import Client


API_KEY = os.environ['API_KEY']
TWILIO_CLIENT = Client(
    os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
SSM = boto3.client('ssm')


def check_stock(stock_param):
    stock = json.loads(stock_param['Value'])
    with closing(urlopen("https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={apikey}".format(symbol=stock['symbol'], apikey=API_KEY))) as responseData:
        jsonData = responseData.read()
        if jsonData is None:
            print("Unable to fetch data for {symbol}".format(
                symbol=stock['symbol']))
            return

        deserialisedData = json.loads(jsonData)[0]
        price = deserialisedData['price']
        print("The price for {symbol} is ${price}".format(
            symbol=stock['symbol'], price=price))

        if price < stock['price_lowerbound']:
            notify_recipients("The price for {symbol} is ${price}, which exceeds the lower bound of ${price_lowerbound}"\
                .format(
                    symbol=stock['symbol'],
                    price=price,
                    price_lowerbound=stock['price_lowerbound']),
                stock['recipients'])
            return

        if price > stock['price_upperbound']:
            notify_recipients("The price for {symbol} is ${price}, which exceeds the upper bound of ${price_upperbound}"\
                .format(
                    symbol=stock['symbol'], 
                    price=price, 
                    price_upperbound=stock['price_upperbound']), 
                stock['recipients'])
            return

        volume = deserialisedData['volume']
        if volume > stock['volume_upperbound']:
            notify_recipients("The volume for {symbol} is {volume}, which exceeds the volume limit of {volume_upperbound}"\
                .format(
                    symbol=stock['symbol'], 
                    volume=volume, 
                    volume_upperbound=stock['volume_upperbound']), 
                stock['recipients'])
            return


def send_sms(recipient, msg):
    try:
        message = TWILIO_CLIENT.messages.create(
            body=msg, from_='+16028334820', to=recipient)
        print("Message sent to {recipient} {message_sid}".format(
            recipient=recipient, message_sid=message.sid))
    except:
        print("Unable to send message to {recipient}".format(
            recipient=recipient))


def notify_recipients(msg, recipients):
    for recipient in recipients:
        send_sms(recipient, msg)


def get_parameters_by_path(next_token=None):
    params = {
        'Path': '/prod/stocks',
        'Recursive': False,
        'WithDecryption': True
    }
    if next_token is not None:
        params['NextToken'] = next_token
    return SSM.get_parameters_by_path(**params)


def stocks():
    next_token = None
    while True:
        response = get_parameters_by_path(next_token)
        parameters = response['Parameters']
        if len(parameters) == 0:
            break
        for parameter in parameters:
            yield parameter
        if 'NextToken' not in response:
            break
        next_token = response['NextToken']


def lambda_handler(event, context):
    for stock in stocks():
        check_stock(stock)
