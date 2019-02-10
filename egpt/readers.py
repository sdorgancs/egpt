
from typing import List, Optional, Any, cast
from types import ModuleType
from dataclasses import dataclass, field
from egpt.order import Output, Input, FileNameType, TimeInterval, JobOrder, SensingTime
from os import path
import json
import glob
import os
from . import modules
import types
import xarray as xr
from datetime import datetime
from enum import Enum
import re
import importlib



class PeriodRelation(Enum):
    IsBefore = 0
    OverlapBefore = 1
    IsInside = 2
    OverlapAfter = 3
    IsAfter = 4
    Includes = 5


@dataclass
class Period:
    start: Optional[datetime] = None
    stop: Optional[datetime] = None

    def is_empty(self):
        return self.start >= self.stop

    def contains(self, other) -> bool:
        return other.start >= self.start and self.stop >= other.stop


def _getpath(pth: str, type: Optional[FileNameType]) -> str:
    if FileNameType.Regexp == type:
        dir, regex = path.split(pth)
        rec = re.compile(regex)
        for f in os.listdir(dir):
            if rec.match(f) is None:
                return f
        raise FileNotFoundError()
    else:
        return pth

def read_task_inputs(task_name:str, task_version: str, order:JobOrder) -> List[Any]:
    inputs:List[Input] = []
    for p in order.list_of_ipf_procs:
        if p.task_name == task_name and p.task_version == task_version:
            inputs = p.list_of_inputs
            break
    if not inputs:
        return []
    sensing_time = None
    objects: List[Any] = []
    if order.ipf_conf is not None and order.ipf_conf.sensing_time is not None:
        sensing_time = order.ipf_conf.sensing_time
        for input in inputs:
            objects.append(read(input, sensing_time))
    return objects
    

def find_file(input: Input, sensing_time: SensingTime) -> str:
    if not input.list_of_time_intervals:
        return _getpath(input.list_of_file_names[0], input.file_type_name)
   
    period = Period(sensing_time.start, sensing_time.stop)
    intervals = []
    #find intervals that covers the period
    for ti in input.list_of_time_intervals:
        validity_interval = Period(ti.start, ti.stop)
        if validity_interval.contains(period):
            intervals.append(ti)
    #select interval that start the latest
    interval = None
    for ti in intervals:
        if interval is None or ti.start > interval.start:
            interval = ti
    if interval is None:
        raise FileNotFoundError()
    if interval.file_name is None:
        raise FileNotFoundError()
    return _getpath(interval.file_name, input.file_type_name)

def read(input: Input, sensing_time: SensingTime) -> Any:
    fname = find_file(input, sensing_time)
    reader = find(fname, input.file_type_name)
    return cast(Any, reader).read(fname)

def find(file_name: str, file_name_type: Optional[FileNameType]) -> ModuleType:
    readers = modules.list_readers()
    if not readers:
        raise ModuleNotFoundError("No reader plugin found")
    the_reader = None
    for reader in readers:
        if file_name_type in reader["Formats"]:
            the_reader = reader
            break
        _, ext = path.splitext(file_name)
        if ext in reader["Extensions"]:
            the_reader = reader

    if the_reader is None:
        raise ModuleNotFoundError(f"No reader plugin found for {file_name}")
    
    m = modules.find(cast(str, the_reader["Name"]), None, "READER")
    if hasattr(reader, "read"):
        return m
    raise ModuleNotFoundError(f"No reader plugin found for {file_name}")