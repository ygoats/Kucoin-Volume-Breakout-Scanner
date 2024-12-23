#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 05:17:10 2020

@ygoats
"""

from kucoin.client import Client
from kucoin.asyncio import KucoinSocketManager

import apiKCS

import telegram_send

from time import sleep

from datetime import datetime, timedelta

from requests import exceptions

####KCS IS OCHL####
####KCS IS OCHL####
####KCS IS OCHL####
####KCS IS OCHL####
###OPEN
###CLOSE
###HIGH
###LOW

##############################################################################################
#############PARSING SELENIUM#################################################################
##############################################################################################


#####################################################

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC1
from selenium.webdriver.common.by import By

##############################################################################################

import os

########################this is transcribing your list from KCS so always updated#####################
########################this is transcribing your list from KCS so always updated#####################

client = Client(apiKCS.api_key, apiKCS.api_secret, apiKCS.api_passphrase)
symbols = client.get_symbols()

lensymbol = len(symbols)

usdt = 'USDT'

usdtList = [] ###for kcs list grab usdt components
usdtListTV = [] ###TRADINGVIEW modified list

for s in range(lensymbol):
    string = symbols[s]['symbol']
    if usdt in string:
        usdtList.append(string)
        tradeString = string.replace('-','')
        usdtListTV.append(tradeString)
        
symbol_list = usdtList
symbol_listR = usdtListTV

lensymb = len(symbol_list)

#print(int(lensymb))

#start1 = 0
#start2 = int(lensymb*1)
#start3 = int(lensymb*2)
#start4 = int(lensymb*3)
#start5 = int(lensymb*4)
#start6 = int(lensymb*5)

spreadList = []
spreadListR = []

######(START1,START2)              FORIP1
######(START2,START3)              FORIP2
######(START3,START4)              FORIP3
######(START4,START5)              FORIP4
######(START5,START6)              FORIP5

for ss in range(lensymb):      #####controlling mechanism for starting list creation from ip points
    spreadList.append(symbol_list[ss])
    spreadListR.append(symbol_listR[ss])

symbol_list=spreadList
symbol_listR=spreadListR

#print(symbol_list)
#print(symbol_listR)
    
########################this is transcribing your list from KCS so always updated#####################
########################this is transcribing your list from KCS so always updated#####################

def listUpdate():
    now = datetime.now()
    tt = now.strftime("%H:%M:%S")
            
    if tt >= "18:00:00" and tt <= "18:00:30":
        #print('Resetting Symbol List')
        client = Client(apiKCS.api_key, apiKCS.api_secret, apiKCS.api_passphrase)
        symbols = client.get_symbols()
        
        lensymbol = len(symbols)
        
        usdt = 'USDT'
        
        usdtList = [] ###for kcs list grab usdt components
        usdtListTV = [] ###TRADINGVIEW modified list
        
        for s in range(lensymbol):
            string = symbols[s]['symbol']
            if usdt in string:
                usdtList.append(string)
                tradeString = string.replace('-','')
                usdtListTV.append(tradeString)
                
        symbol_list = usdtList
        symbol_listR = usdtListTV
        
        lensymb = len(symbol_list)
        
        #print(int(lensymb))
        
        #start1 = 0
        #start2 = int(lensymb*1)
        #start3 = int(lensymb*2)
        #start4 = int(lensymb*3)
        #start5 = int(lensymb*4)
        #start6 = int(lensymb*5)
        
        spreadList = []
        spreadListR = []
        
        for ss in range(lensymb):      #####controlling mechanism for starting list creation from ip points
            spreadList.append(symbol_list[ss])
            spreadListR.append(symbol_listR[ss])
        
        symbol_list=spreadList
        symbol_listR=spreadListR
        
        #print(symbol_list)
        #print(symbol_listR)
        #print('Job is done')

def trade():
    lenList = len(symbol_list)
    LITR = True
    conNode = False
    
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    
    tt = now.today() - timedelta(days=30, hours=0, minutes=0)
    #####HERE WE GET THE START POINT FOR DATA && ENDPOINT FOR DATA
    fromStamp = int(datetime.timestamp(tt))
    toStamp = int(time.time())
    
    # =============================================================================
    #     #print(t)
    #     #print(tt)
    #     #print(fromStamp)
    #     #print(toStamp)
    # =============================================================================
    
    for s in range(lenList):
        sleep(1)
        #print(symbol_list[s])
        atrList = []
        volList = []
        klines = []
        try:
            client = Client(apiKCS.api_key, apiKCS.api_secret, apiKCS.api_passphrase)
            klines = client.get_kline_data(symbol_list[s],'1day', fromStamp, toStamp)
        except IndexError as e:
            #print(e)
            lenList = float(lenList) - 1 
            continue
        except Exception as e:
            pd = open('logs/volBreaker.log', 'a')
            pd.write("\n" + str(t) + str(e))
            pd.close()
            #print(str(e))
            sleep(3)
            conNode = True
            
        while conNode == True:
            try:
                client = Client(apiKCS.api_key, apiKCS.api_secret, apiKCS.api_passphrase)
                klines = client.get_kline_data(symbol_list[s],'1day', fromStamp, toStamp)
            except IndexError as e:
                #print(e)
                lenList = float(lenList) - 1 
                continue
            except Exception as e:
                pd = open('logs/volBreaker.log', 'a')
                pd.write("\n" + str(t) + str(e))
                pd.close()
                #print(str(e))
                sleep(3)
                conNode = True

        try:
            for b in range(21):
                volNodeFinder = float(klines[b+1][6])
                volList.append(volNodeFinder)

        except IndexError as e:
            #print(e)
            lenList = float(lenList) - 1 
            continue
        except KeyError as e:
            #print(e)
            lenList = float(lenList) - 1 
            continue

        indexVol = float(max(volList))

        #print(symbol_list[s])
        currentVol = float(klines[0][6])
        currentVol1 = float(klines[0][5])
        currentClose = float(klines[0][2])
        currentOpen = float(klines[0][1])

        #print('todays supposed volume '+ str(currentVol))
        #print('test ' + str(currentVol1))
        #print('indexVolNode ' + str(indexVol))

        if currentVol > indexVol and currentClose > currentOpen:
            
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            wait_time = 25 # a very long wait time
            options = webdriver.ChromeOptions()
            options.headless = True
            options.add_argument(f'user-agent={user_agent}')
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument("--disable-extensions")
            options.add_argument("--proxy-server='direct://'")
            options.add_argument("--proxy-bypass-list=*")
            options.add_argument("--start-maximized")
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            
            driver = webdriver.Chrome(executable_path="/home/chasehome/liteScanners/66/chromedriver", options=options)
            
            sleep(1)
            
            driver.get ("https://in.tradingview.com/chart/?symbol=" + str(symbol_listR[s]))
            
            driver.maximize_window()
            sleep(1)
            ActionChains(driver).send_keys('1').perform()
            sleep(1)
            ActionChains(driver).send_keys('d').perform()
            sleep(1)
            ActionChains(driver).key_down(Keys.ENTER).perform()
            sleep(1)
            ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.ALT).key_down('s').perform()
            
            #element = WebDriverWait(driver, wait_time).until(EC1.element_to_be_clickable((By.LINK_TEXT, 'Save image')))
            #element.click()
            time.sleep(1)
            driver.close()
            
            filelist= list([file for file in os.listdir('/home/chasehome/liteScanners/66/') if file.endswith('.png')])
            
            with open(filelist[0], "rb") as f:
            	telegram_send.send(disable_web_page_preview=True, conf='channel2.conf', images=[f], captions=["Volume Breakout " + str(symbol_list[s]) + " " + str(currentClose) \
                                    + "\n" + "https://m.kucoin.com/markets/symbol/" + str(symbol_list[s])])
            
            os.remove(filelist[0])

            filelist = []
                
            symbol_list.remove(symbol_list[s])
            symbol_listR.remove(symbol_listR[s])
            break

def Main():        
    now = datetime.now()
    t = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    print("Connection Established")
    print(str(t))

    lenList = len(symbol_list)
    LITR = True
    conNode = False

    now = datetime.now()
    t = now.strftime("%H:%M:%S")

    tt = now.today() - timedelta(days=30, hours=0, minutes=0)
    #####HERE WE GET THE START POINT FOR DATA && ENDPOINT FOR DATA
    fromStamp = int(datetime.timestamp(tt))
    toStamp = int(time.time())

    # =============================================================================
    #     #print(t)
    #     #print(tt)
    #     #print(fromStamp)
    #     #print(toStamp)
    # =============================================================================

    for s in range(lenList):
        sleep(1)
        #print(symbol_list[s])
        atrList = []
        volList = []
        klines = []
        try:
            client = Client(apiKCS.api_key, apiKCS.api_secret, apiKCS.api_passphrase)
            klines = client.get_kline_data(symbol_list[s],'1day', fromStamp, toStamp)
        except IndexError as e:
            #print(e)
            lenList = float(lenList) - 1
            continue
        except Exception as e:
            pd = open('logs/volBreaker.log', 'a')
            pd.write("\n" + str(t) + str(e))
            pd.close()
            #print(str(e))
            sleep(3)
            conNode = True

        while conNode == True:
            try:
                client = Client(apiKCS.api_key, apiKCS.api_secret, apiKCS.api_passphrase)
                klines = client.get_kline_data(symbol_list[s],'1day', fromStamp, toStamp)
            except IndexError as e:
                #print(e)
                lenList = float(lenList) - 1
                continue
            except Exception as e:
                pd = open('logs/volBreaker.log', 'a')
                pd.write("\n" + str(t) + str(e))
                pd.close()
                #print(str(e))
                sleep(3)
                conNode = True

        try:
            for b in range(21):
                volNodeFinder = float(klines[b+1][6])
                volList.append(volNodeFinder)

        except IndexError as e:
            #print(e)
            lenList = float(lenList) - 1
            continue
        except KeyError as e:
            #print(e)
            lenList = float(lenList) - 1
            continue

        indexVol = float(max(volList))

        print(symbol_list[s])
        currentVol = float(klines[0][6])
        currentVol1 = float(klines[0][5])
        currentClose = float(klines[0][2])
        currentOpen = float(klines[0][1])

        #print('todays supposed volume '+ str(currentVol))
        #print('test ' + str(currentVol1))
        #print('indexVolNode ' + str(indexVol))

        if currentVol > indexVol and currentClose > currentOpen:

            symbol_list.remove(symbol_list[s])
            symbol_listR.remove(symbol_listR[s])
            continue

    conNode = False  
    
    while conNode == False:
        trade()
        listUpdate()
        
if __name__ == '__main__':
    Main()
