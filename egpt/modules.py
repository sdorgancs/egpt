import importlib
from os import path
import os
from types import ModuleType
from prettyprinter import cpprint # type: ignore
import subprocess
from typing import List, Tuple, Dict,  Union, Optional
import glob
from functools import cmp_to_key


ModuleProperties = Dict[str, Union[str, List[str]]]

def pythonize(name:str):
    nname = name.replace("-", "_")
    nname = nname.replace(".", "_")
    return nname

def list_modules() -> List[ModuleProperties]:
   modules = []
   dist_info_dirs = glob.glob(path.expanduser("~/.egpt/plugins/*.dist-info"))
   for mod_info in dist_info_dirs:
        meta = load_meta(mod_info)
        modules.append(meta)
   return modules

def load_meta(mod_info) -> ModuleProperties:
    meta: ModuleProperties = dict()
    with open(path.join(mod_info, "METADATA")) as f:
        fmeta = f.readlines()
        for smeta in fmeta:
            if smeta.startswith("Classifier"):
                tokens = smeta.split("::")
                if len(tokens) < 2: continue
                ctype = tokens[0]
                value = tokens[1].strip()
                if ctype.startswith("Classifier: Type"):
                    meta["Type"] = value
                elif ctype.startswith("Classifier: Formats"):
                    meta["Formats"] = value.split(",")
                elif ctype.startswith("Classifier: Extensions"):
                    meta["Extensions"] = value.split(",")
            else:
                tokens = smeta.split(":")
                if len(tokens) < 2: continue
                meta[tokens[0].strip()] = tokens[1].strip()
    with open(path.join(mod_info, "top_level.txt")) as f:
        meta["Package"] = f.readline().strip()
    return meta

def filter_modules_by_type(modules: List[ModuleProperties], mtype: str) -> List[ModuleProperties]:
    return [mod for mod in modules if mod["Type"] == f"EGPT-{mtype}"]

def get_module_by_name(modules: List[ModuleProperties], name: str) -> ModuleProperties:
    mods = [mod for mod in modules if mod["Name"] == name]
    if len(mods) == 1:
        return mods[0]
    raise ModuleNotFoundError(f"{name} is not an EGPT plugin")

def list_workflows()  -> List[ModuleProperties]:
   return filter_modules_by_type(list_modules(), "WORKFLOW")
    
def list_tasks() -> List[ModuleProperties]:
   return filter_modules_by_type(list_modules(), "TASK")

def list_readers() -> List[ModuleProperties]:
    return filter_modules_by_type(list_modules(), "READER")

def list_writers() -> List[ModuleProperties]:
    return filter_modules_by_type(list_modules(), "WRITER")

def read_version(v):
    return ".".join( v[1:].split("_"))

def is_version_dir(v):
    return v.startswith("v")

def cmp_version(v1: str, v2: str) -> int:
    v1nums = [int(vi) for vi in v1.split(".")]
    v2nums = [int(vi) for vi in v2.split(".")]
    for i in range(min(len(v1nums), len(v2nums))):
        li = v1nums[i] - v2nums[i]
        if li != 0:
            return li
    return len(v1nums) - len(v2nums)

def available_versions(name) -> List[str]:
    dirs = os.listdir(path.join(path.expanduser("~/.egpt/plugins"), pythonize(name)))
    versions = [read_version(d) for d in dirs if is_version_dir(d)]
    return sorted(versions, key=cmp_to_key(cmp_version))

def find(name: str, version: Optional[str], mtype: str) -> ModuleType:
    m = get_module_by_name(list_modules(), name)
    if m["Type"] != f"EGPT-{mtype}":
        raise ModuleNotFoundError(f"{name} is not a {mtype} module")
    if version is None:
        version = available_versions(m["Package"])[0]
    pkg = f"{m['Package']}.v{pythonize(version)}"
    importlib.invalidate_caches()
    return importlib.import_module(pkg)

if __name__ == "__main__":
    for m in list_modules():
       cpprint(m)
    print("-- WORkFLOWS ---")
    for m in list_workflows():
        cpprint(m)
        cpprint(available_versions(m["Package"]))
    print("-- TASKS ---")
    for m in list_tasks():
        cpprint(m)
        cpprint(available_versions(m["Package"]))
    print("-- READER ---")
    for m in list_readers():
        cpprint(m)
        cpprint(available_versions(m["Package"]))
    print("-- WRITERS ---")
    for m in list_writers():
        cpprint(m)
        cpprint(available_versions(m["Package"]))