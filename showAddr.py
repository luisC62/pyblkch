#! /usr/bin/python3

import argparse
import requests
from os import system, name
from prettytable import PrettyTable
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
#-------------------------------------------------------------------
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
#-------------------------------------------------------------------
def showBTCratings(inputratings):
    t=PrettyTable(['USD', 'EUR'])
    t.add_row([inputratings[0], inputratings[1]])
    print("Cotizaciones BTC")
    print(t)
#-------------------------------------------------------------------
def getAddrInfo(addr):
    ratings=getBTCratings()
    showBTCratings(ratings)
    USDperBTC=ratings[0]
    EURperBTC=ratings[1]
    SATperBTC=100000000
    url="https://blockchain.info/rawaddr/" + addr
    try:
        response=requests.get(url)
        addrdata=response.json()
    except:
        print(f"No se puede encontrar el recurso: {url}")
        print("Saliendo.....")
        sys.exit(0)
    print(f"GENERAL dirección: {addr}")
    t=PrettyTable(['Valor', 'BTC', 'USD', 'EUR'])
    totalReceived=addrdata['total_received']
    totalSent=addrdata['total_sent']
    finalBalance=addrdata['final_balance']
    totalReceivedBTC=totalReceived / SATperBTC
    totalReceivedUSD=totalReceivedBTC * USDperBTC
    totalReceivedEUR=totalReceivedBTC * EURperBTC
    totalSentBTC=totalSent / SATperBTC
    totalSentUSD=totalSentBTC * USDperBTC
    totalSentEUR=totalSentBTC * EURperBTC
    finalBalanceBTC=finalBalance / SATperBTC
    finalBalanceUSD=finalBalanceBTC * USDperBTC
    finalBalanceEUR=finalBalanceBTC * EURperBTC
    ftotalReceivedUSD=f"{totalReceivedUSD:.2f}"
    ftotalReceivedEUR=f"{totalReceivedEUR:.2f}"
    ftotalSentUSD=f"{totalSentUSD:.2f}"
    ftotalSentEUR=f"{totalSentEUR:.2f}"
    ffinalBalanceUSD=f"{finalBalanceUSD:.2f}"
    ffinalBalanceEUR=f"{finalBalanceEUR:.2f}"
    t.add_row(["Total Recibido", totalReceivedBTC, ftotalReceivedUSD, ftotalReceivedEUR])
    t.add_row(["Total Enviado", totalSentBTC, ftotalSentUSD, ftotalSentEUR])
    t.add_row(["Balance Final", finalBalanceBTC, ffinalBalanceUSD, ffinalBalanceEUR])
    print(t)

    print(f"TRANSACCIONES. Número de transacciones: {len(addrdata['txs'])}")
    tx=PrettyTable(['#', 'HASH', 'Date', 'BTC', 'USD', 'EUR'])
    for i in range(0, len(addrdata['txs'])):
        txBalance=addrdata['txs'][i]['balance']
        txDate=datetime.datetime.fromtimestamp(addrdata['txs'][i]['time'])
        txBalanceBTC=txBalance / SATperBTC
        txBalanceUSD=txBalanceBTC * USDperBTC
        txBalanceEUR=txBalanceBTC * EURperBTC
        ftxBalanceUSD=f"{txBalanceUSD:.2f}"
        ftxBalanceEUR=f"{txBalanceEUR:.2f}"
        tx.add_row([i, addrdata['txs'][i]['hash'], txDate, txBalanceBTC, ftxBalanceUSD, ftxBalanceEUR])
    print(tx)
    
parser = argparse.ArgumentParser()
parser.add_argument("addr", 
                    help="Address to get info about", 
                    type=str)
args = parser.parse_args()

clear()

getAddrInfo(args.addr)

#ejemplo: python sohwAddr.py 3QiETomgUhPu573ZvhXbdofq7y5ocNS1ie