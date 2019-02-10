import egpt.modules as mods
from types import ModuleType
from dataclasses import dataclass, field
from typing import List
import xarray as xr

def find(name:str, version:str) -> ModuleType:
   return mods.find(name, version, "TASK")
  
