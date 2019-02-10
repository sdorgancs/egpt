from egpt.order import JobOrder
from egpt import tasks
from egpt.readers import read_task_inputs
from distributed import get_client,wait
from egpt.processing import Result
from datetime import datetime
from distributed import Client
from importlib import invalidate_caches
from prettyprinter import cpprint
import egpt.tasks

def execute(order: JobOrder) -> Result:
    cpprint(order)
    t = tasks.find("egpt_test_task", "1.0")
    r = get_client().submit(t.execute, "coucou")
    wait([r])
    res = Result()
    res.exit_code = 0
    res.exit_status = "OK"
    res.outputs = []
    return res
