
from egpt.order import JobOrder, IpfConf, JobOrder, SensingTime, Input, FileNameType, TimeInterval, IpfProc
from distributed import Client # type: ignore
from dataclasses import dataclass, field
from datetime import datetime
from egpt import workflows
from egpt import order as order
from typing import List, Union, Optional, cast

@dataclass
class Result:
    start: datetime = datetime.now()
    stop: Optional[datetime] = None
    exit_code : int = 0
    exit_status : Optional[str] = None
    outputs : List[str] =  field(default_factory=list)

def submit(job: Union[JobOrder, str]) -> Result:
    if type(job) is JobOrder:
        o = cast(JobOrder, job)
    elif type(job) is str:
        o = order.parse(cast(str, job))
    wf = workflows.find(o.ipf_conf.processor_name, o.ipf_conf.version)
    return wf.execute(o)# type: ignore