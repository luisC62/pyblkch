#! /usr/bin/python3

import requests
import argparse
from prettytable import PrettyTable
from os import system, name
import datetime
import sys


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

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

def getSingleTx(hash):
    ratings=getBTCratings()
    print("BTC ratings")
    showBTCratings(ratings)
    USDperBTC=ratings[0]
    EURperBTC=ratings[1]
    SATperBTC=100000000
    url="https://blockchain.info/rawtx/" + hash
    try:
        response=requests.get(url)
        stdata=response.json()
    except:
        print(f"No se puede encontrar el recurso: {url}")
        print("Saliendo.....")
        sys.exit(0)
    t=PrettyTable(['Variable', 'Value'])
    t.add_row(['hash', stdata['hash']])
    t.add_row(['Fee', stdata['fee']])
    dt = datetime.datetime.fromtimestamp(stdata['time'])
    t.add_row(['Time', dt])
    t.add_row(['size', stdata['size']])
    t.add_row(['weight', stdata['weight']])
    print("GENERAL")
    print(t)
    #---------------------------------------------------------
    ti=PrettyTable(['Address', 'BTC', 'USD', 'EUR'])
    totalValueBTC=0
    for i in range(0, len(stdata['inputs'])):
        address=stdata['inputs'][i]['prev_out']['addr']
        value=stdata['inputs'][i]['prev_out']['value']
        valueBTC=value / SATperBTC
        valueUSD=valueBTC * USDperBTC
        valueEUR=valueBTC * EURperBTC
        fValueUSD=f"{valueUSD:.2f}"
        fValueEUR=f"{valueEUR:.2f}"
        ti.add_row([address, valueBTC, fValueUSD, fValueEUR])
        totalValueBTC=totalValueBTC + valueBTC
    totalValueUSD=totalValueBTC * USDperBTC
    totalValueEUR=totalValueBTC * EURperBTC
    ftotalValueUSD=f"{totalValueUSD:.2f}"
    ftotalValueEUR=f"{totalValueEUR:.2f}"
    ti.add_row(['Total:', totalValueBTC, ftotalValueUSD, ftotalValueEUR])
    print("INPUTS")
    print(ti)
    #---------------------------------------------------------
    to=PrettyTable(['Address', 'BTC', 'USD', 'EUR'])
    totalValueBTC=0
    for i in range(0, len(stdata['out'])):
        address=stdata['out'][i]['addr']
        value=stdata['out'][i]['value']
        valueBTC=value / SATperBTC
        valueUSD=valueBTC * USDperBTC
        valueEUR=valueBTC * EURperBTC
        fValueUSD=f"{valueUSD:.2f}"
        fValueEUR=f"{valueEUR:.2f}"
        to.add_row([address, valueBTC, fValueUSD, fValueEUR])
        totalValueBTC=totalValueBTC + valueBTC
    totalValueUSD=totalValueBTC * USDperBTC
    totalValueEUR=totalValueBTC * EURperBTC
    ftotalValueUSD=f"{totalValueUSD:.2f}"
    ftotalValueEUR=f"{totalValueEUR:.2f}"
    to.add_row(['Total:', totalValueBTC, ftotalValueUSD, ftotalValueEUR])
    print("OUTPUTS")
    print(to)

parser = argparse.ArgumentParser()
parser.add_argument("hash", 
                    help="Hash of the transaction", 
                    type=str)
args = parser.parse_args()

clear()

getSingleTx(args.hash)

#example: python 01_singleTX.py fd10cf0f4f0ff01c41225535a113b64efc8fb43fa39e34e42561f8007bf617ce
