import time
import requests
from . import RDB_URL
import traceback
import ifaddr
import os
import socket
import json
from typing import Dict, Any

class HTTPError(Exception):
        def __init__(self, code):
            self.code = code

def getips() -> str:
    return socket.gethostname()

def breakpoint(name: str):
    configure(name)
    while is_activated(name):
        time.sleep(1)

def activate(name: str):
    url = "{}/breakpoints/state/{}".format(RDB_URL, name)
    requests.post(url,{"state":"active"})

def deactivate(name: str):
    url = "{}/breakpoints/state/{}".format(RDB_URL, name)
    requests.post(url,{"state":""})

def configure(name: str):
    url = "{}/breakpoints/process/{}".format(RDB_URL, name)
    requests.post(url,json={"pid":os.getpid(), "ppid":os.getppid(), "hostname":socket.gethostname()})


def all() -> Dict[str, Any]:
    url = "{}/breakpoints".format(RDB_URL)
    r = requests.get(url)
    return r.json()

def remoteprocess(name: str) -> Dict[str, Any]:
    url = "{}/breakpoints/process/{}".format(RDB_URL, name)
    r = requests.get(url)
    if r.status_code != 200:
        raise HTTPError(r.status_code)
    return r.json() 

def is_activated(name: str) -> bool:
    url = "{}/breakpoints/state/{}".format(RDB_URL, name)
    r = requests.get(url)
    if r.status_code != 200:
        return False
    else:
        return r.text == "active"
