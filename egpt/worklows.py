from . import modules as mods
from types import ModuleType

def find(name:str, version:str) -> ModuleType:
    return mods.find(name, version, "WORKFLOW")