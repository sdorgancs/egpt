from datetime import datetime
from typing import List, NamedTuple, Optional, cast
from dataclasses import dataclass, field
from enum import Enum, unique
import xml.etree.ElementTree as ET
from os import path
from datetime import datetime

@dataclass
class ProcessingParameter:
    name: Optional[str] = None
    value: Optional[str] = None

@dataclass
class SensingTime:
    start: Optional[datetime] = None
    stop: Optional[datetime] = None

@dataclass
class IpfConf:
    processor_name: str
    version: str
    stdout_log_level: Optional[str] = None
    stderr_log_level: Optional[str] = None
    test: bool = False
    breakpoint_enable: bool = False
    acquisition_station: Optional[str] = None
    processing_station: Optional[str] = None
    config_files : List[str] = field(default_factory=list)
    sensing_time: Optional[SensingTime] = None
    dynamic_processing_parameters: List[ProcessingParameter] = field(default_factory=list)

@dataclass
class TimeInterval:
    start: Optional[datetime] = None
    stop: Optional[datetime] = None
    file_name: Optional[str] = None

@unique
class FileNameType(Enum):
    Unknown = -1
    Physical = 0
    Logical = 1
    Stem = 2
    Regexp = 3
    Directory = 4

@dataclass
class Input:
    file_type: Optional[str] = None
    file_type_name: Optional[FileNameType] = None
    list_of_file_names: List[str] = field(default_factory=list)
    list_of_time_intervals: List[TimeInterval] = field(default_factory=list)

@dataclass
class Output:
    file_type: Optional[str]  = None
    file_name_type: Optional[FileNameType] = None
    file_name: Optional[str]  = None

@dataclass
class IpfProc:
    task_name: Optional[str] = None
    task_version: Optional[str] = None
    breakpoint: Optional[BreakPoint] = None
    list_of_inputs: List[Input] = field(default_factory=list)
    list_of_output: List[Output] = field(default_factory=list)

@dataclass
class BreakPointFile:
    enable: bool = False
    file_type: Optional[str] = None
    file_name_type: Optional[FileNameType] = None
    file_name: Optional[str] = None

@dataclass
class BreakPoint:
    break_point_files: List[BreakPointFile] = field(default_factory=list)


@dataclass
class JobOrder:
    identifier: str
    ipf_conf: IpfConf
    list_of_ipf_procs: List[IpfProc] = field(default_factory=list)

class JobOrderParseError(Exception):
    pass

def _ctext(tag: ET.Element, name: str) -> Optional[str]:
    child = tag.find(name)
    return _text(child)

def _text(elt: Optional[ET.Element]) -> Optional[str]:
    if elt is None:
        return None
    return elt.text

def _cbool(tag: ET.Element, name: str) -> bool:
    t = _ctext(tag, name)
    return t == "true"

def _cfile_name_type(tag: ET.Element, name: str) -> Optional[FileNameType]:
    t = _ctext(tag, name)
    if t is None:
        return None
    return FileNameType[t]

def _cdatetime(elt: ET.Element, name: str) -> Optional[datetime]:
    t = _ctext(elt, name)
    if t is None:
        return None
    return datetime.strptime(t,'%Y%m%d_%H%M%S%f')

def _datetime(elt: Optional[ET.Element]) -> Optional[datetime]:
    t = _text(elt)
    if t is None:
        return None
    return datetime.strptime(t,'%Y%m%d_%H%M%S%f')

def _parse_input(xinput: ET.Element) -> Input:
    input = Input()
    input.file_type = _ctext(xinput, 'File_Type')
    input.file_type_name = _cfile_name_type(xinput, 'File_Name_Type')
    xfiles_names_elt = xinput.find('List_of_File_Names')
    if xfiles_names_elt is not None:
        xfiles_names = xfiles_names_elt.findall('File_Name')
        if xfiles_names is not None:
            for xfile_name in xfiles_names:
                name = _text(xfile_name)
                if name is not None:
                    input.list_of_file_names.append(name)
    xtime_intervals_elt = xinput.find('List_of_Time_Intervals')
    if xtime_intervals_elt is not None:
        xtime_intervals = xtime_intervals_elt.findall('Time_Interval')
        if xtime_intervals is not None:
            for xinterval in xtime_intervals:
                ti = TimeInterval()
                ti.start = _cdatetime(xinterval, 'Start')
                ti.stop = _cdatetime(xinterval, 'Stop')
                ti.file_name = _ctext(xinterval, 'File_Name')
                input.list_of_time_intervals.append(ti)
    return input

def _parse_output(xoutput: ET.Element) -> Output:
    output = Output()
    output.file_name = _ctext(xoutput, 'File_Name')
    output.file_name_type = _cfile_name_type(xoutput, 'File_Name_Type')
    output.file_type = _ctext(xoutput, 'File_Type')
    return output

def _parse_ipf_conf(xipf_conf: ET.Element) -> IpfConf:
    ipf_conf = IpfConf(
        processor_name= cast(str,_ctext(xipf_conf, 'Processor_Name')),
        version = cast(str,_ctext(xipf_conf, 'Version'))
    )
    ipf_conf.stdout_log_level = _ctext(xipf_conf, 'Stdout_Log_Level')
    ipf_conf.stderr_log_level = _ctext(xipf_conf, 'Stderr_Log_Level')
    ipf_conf.test = _cbool(xipf_conf, 'Test')
    ipf_conf.breakpoint_enable = _cbool(xipf_conf, 'Breakpoint_Enable')
    ipf_conf.acquisition_station = _ctext(xipf_conf, 'Acquisition_Station')
    ipf_conf.processing_station = _ctext(xipf_conf, 'Processing_Station')
    xconfig_files = xipf_conf.find('Config_Files')
    if xconfig_files is not None:
        xfile_names = xconfig_files.findall('Conf_File_Name')
        for xfile_name in xfile_names:
            name = _text(xfile_name)
            if name is not None:
                ipf_conf.config_files.append(name)

    xsensing_time = xipf_conf.find('Sensing_Time')
    if xsensing_time is not None:
        start = _datetime(xsensing_time.find('Start'))
        stop = _datetime(xsensing_time.find('Stop'))
        ipf_conf.sensing_time = SensingTime(start=start, stop=stop)

    xprocessing_parameters_elt = xipf_conf.find('Dynamic_Processing_Parameters')
    if xprocessing_parameters_elt is not None:
        xprocessing_parameters = xprocessing_parameters_elt.findall('Processing_Parameter')
        if xprocessing_parameters is not None:
            for xparam in xprocessing_parameters:
                p = ProcessingParameter(name=_ctext(xparam, 'Name'), value=_ctext(xparam, 'Value'))
                ipf_conf.dynamic_processing_parameters.append(p)
    return ipf_conf

def _parse_breakpoint(xbreak_point: ET.Element) -> BreakPoint:
    breakpoint = BreakPoint()
    xlist_of_breakpoint_files = xbreak_point.find('List_of_Brk_Files')
    if xlist_of_breakpoint_files is None:
        return breakpoint
    xbrk_files = xlist_of_breakpoint_files.findall('Brk_File')
    if xbrk_files is None:
        return breakpoint
    for xbrk_file in xbrk_files:
        brk_file = BreakPointFile()
        brk_file.enable = _cbool(xbrk_file, 'Enable')
        brk_file.file_type = _ctext(xbrk_file, 'File_Type')
        brk_file.file_name_type = _cfile_name_type(xbrk_file, 'File_Name_Type')
        brk_file.file_name= _ctext(xbrk_file, 'File_Name')
        breakpoint.break_point_files.append(brk_file)
    return breakpoint

def _parse_ipf_proc(xipf_proc: ET.Element) -> IpfProc:
    ipf_proc = IpfProc()
    ipf_proc.task_name = _ctext(xipf_proc, 'Task_Name')
    ipf_proc.task_version = _ctext(xipf_proc, 'Task_Version')
    xbreak_point = xipf_proc.find('BreakPoint')
    if xbreak_point is not None:
        ipf_proc.breakpoint = _parse_breakpoint(xbreak_point)
    
    xlist_of_inputs_elt = xipf_proc.find('List_of_Inputs')
    if xlist_of_inputs_elt is not None:
        xlist_of_inputs = xlist_of_inputs_elt.findall('Input')
        if xlist_of_inputs is not None:
            for xinput in xlist_of_inputs:
                ipf_proc.list_of_inputs.append(_parse_input(xinput))

    xlist_of_outputs_elt = xipf_proc.find('List_of_Outputs')
    if xlist_of_outputs_elt is not None:
        xlist_of_outputs = xlist_of_outputs_elt.findall('Output')
        if xlist_of_outputs is not None:
            for xoutput in xlist_of_outputs:
                ipf_proc.list_of_output.append(_parse_output(xoutput))

    return ipf_proc

def parse(filename: str) -> JobOrder:
    tokens = filename.split(".")
    tree = ET.parse(filename)
    root = tree.getroot()
    xipf_conf_list = root.findall('Ipf_Conf')
    if len(xipf_conf_list) != 1:
        raise JobOrderParseError(f"a job order should contains exactly one Ipf_Conf tag: {len(xipf_conf_list)} found")
    xipf_conf = xipf_conf_list[0]
    result = JobOrder(tokens[1], _parse_ipf_conf(xipf_conf))
    xipf_proc_list = root.findall('List_of_Ipf_Procs')
    if len(xipf_proc_list) != 1:
        raise JobOrderParseError(f"a job order should contains exactly one List_of_Ipf_Procs tag: {len(xipf_proc_list)} found")
    # xipf_procs_elt = xipf_proc_list[0]
    # xipf_procs= xipf_procs_elt.findall('Ipf_Proc')
    if xipf_proc_list is not None:
        for xipf_proc in xipf_proc_list:
            result.list_of_ipf_procs.append(_parse_ipf_proc(xipf_proc))
    return result