"""
bumpServer.py - loop through each token and channel and appropriately bump on an interval
"""

__author__ = "Seraph#9999"

import requests, json, threading, functools
from colorama import init, Fore, Style
init()

with open('info.json') as f:
    accts = json.load(f)



def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def bumpServer(token, channelID, message):
    baseURL = "https://discordapp.com/api/channels/{}/messages".format(channelID)
    headers = { "Authorization":"{}".format(token),
            "User-Agent":"Mozilla: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3 Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4",
            "Content-Type":"application/json", }
    POSTedJSON =  json.dumps({"content":message})
    r = requests.post(baseURL, headers = headers, data = POSTedJSON)
    decResponse = json.loads(r.content.decode('utf-8'))
    try:
        if (decResponse['message'] == '401: Unauthorized'):
            print(f'{Fore.RED}[ALERT] {Style.RESET_ALL}INVALID TOKEN: {token}')
            return
    except Exception as e:
        pass
    print(f'{Fore.CYAN}[INFO] {Style.RESET_ALL}Sent {message} to {str(channelID)} with {token}')
    
for key, value in accts.items():
    set_interval(functools.partial(bumpServer, key, value, '!d bump'), 10)
    print(f"{Fore.CYAN}[INFO] {Style.RESET_ALL}Beginning messaging with {key} on {value} \n")
