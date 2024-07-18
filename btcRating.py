#! /usr/bin/python3
import requests
from prettytable import PrettyTable
import sys


def getBTCratings():
    url="https://blockchain.info/ticker"
    try:
        response=requests.get(url)
        jsondata=response.json()
    except:
        print(f"No se puede encontrar el recurso: {url}")
        print("Saliendo.....")
        sys.exit(0)
    
    USDperBTC=jsondata['USD']['last']
    EURperBTC=jsondata['EUR']['last']
    BTCratings=[USDperBTC, EURperBTC]
    return BTCratings
    
def showBTCratings(inputratings):
    t=PrettyTable(['USD', 'EUR'])
    t.add_row([inputratings[0], inputratings[1]])
    print("Cotizaciones BTC")
    print(t)

ratings=getBTCratings()
showBTCratings(ratings)

