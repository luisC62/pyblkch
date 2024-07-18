#! /usr/bin/python3

import requests
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

def getUnconfirmedTransactions():
    ratings=getBTCratings()
    showBTCratings(ratings)
    USDperBTC=ratings[0]
    EURperBTC=ratings[1]
    SATperBTC=100000000
    url="https://blockchain.info/unconfirmed-transactions?format=json"
    try:
        response=requests.get(url)
        utdata=response.json()
    except:
        print(f"No se puede encontrar el recurso: {url}")
        print("Saliendo.....")
        sys.exit(0)
    t=PrettyTable(['#', 'HASH', 'BTC', 'USD', 'EUR'])
    for i in range(0, len(utdata['txs'])):
        totalValue=0
        for j in range(0, len(utdata['txs'][i]['inputs'])):
            totalValue = totalValue + utdata['txs'][i]['inputs'][j]['prev_out']['value']
        totalValueBTC=totalValue / SATperBTC
        totalValueUSD=totalValueBTC * USDperBTC
        totalValueEUR=totalValueBTC * EURperBTC
        fValueUSD=f"{totalValueUSD:.2f}"
        fValueEUR=f"{totalValueEUR:.2f}"
        tx_hash=utdata['txs'][i]['hash']
        t.add_row([i, 
                   tx_hash, 
                   totalValueBTC, 
                   fValueUSD, 
                   fValueEUR])
    print(t)
    seleccion = input("¿Quieres ver una transacción? (s/n)")
    if seleccion=="s": 
        ntx  = input("Introduce el número de transacción: ")
        newhash=utdata['txs'][int(ntx)]['hash']
        #print(f"Me pides el hash: {newhash}")
        getSingleTx(newhash)


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

clear()
getUnconfirmedTransactions()
 
