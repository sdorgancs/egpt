from bottle import get, post, run, request, HTTPError
from dataclasses import dataclass, field
from typing import List, Any, Dict
from multiprocessing import Process
import  time
import json

breakpoints:Dict[str , Breakpoint]={}



@dataclass
class Breakpoint:
    state: str
    name: str
    processes: List[RemoteProcess] = field(default_factory=list)

@dataclass
class RemoteProcess:
    hostname: str
    pid: int
    ident: str
    ppid: int
    
    

def tojson(obj:Any) -> str:
    return json.dumps(obj, default=lambda o: o.__dict__)

@get('/breakpoints')
def _getbps() -> str:
   result = []
   for _, b in breakpoints.items():
       result.append(b)
   return tojson(result)

@get('/breakpoints/state/<name>')
def _getbp(name:str) -> str:
    if name in breakpoints:
        return breakpoints[name].state
    raise HTTPError(404)

@post('/breakpoints/state/<name>')
def _setbp(name: str):
    # pylint: disable=E1136
    state = request.forms["state"]
    breakpoints[name]=Breakpoint(name, state)

@post('/breakpoints/process/<name>')
def _setprocess(name:str):
    if name not in breakpoints:
        raise HTTPError(404)
    js = json.load(request.body)
    p = RemoteProcess(
        hostname=js["hostname"],
        pid=js["pid"], 
        ppid= js["ppid"],
        ident=name+"-"+str(len(breakpoints[name].processes)))
    print("set "+name)
    breakpoints[name].processes.append(p)

@get('/breakpoints/process/<name>')
def _getprocess(name: str):
    if name not in breakpoints:
        raise HTTPError(404)
   
    return tojson(breakpoints[name].processes)

def _start():
    run(host='localhost', port=12345)

def init() -> Process:
    p = Process(target=_start)
    p.start()
    time.sleep(1)
    return p
