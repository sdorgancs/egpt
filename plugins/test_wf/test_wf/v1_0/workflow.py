from egpt.order import JobOrder
from egpt import tasks
from egpt.readers import read_task_inputs
from distributed import get_client,wait
from egpt.processing import Result
from datetime import datetime
from distributed import Client
from importlib import invalidate_caches
from prettyprinter import cpprint
from datetime import datetime
from tempfile import NamedTemporaryFile
import egpt.tasks

def write(s1, s2, s3):
    with NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("{}\n{}\n{}\n".format(s1, s2, s3))
        f.flush()
        return f.name

def execute(order: JobOrder) -> Result:
    t = tasks.find("test-task", "1.0")

    dsk = {
        'say-1': (t.execute, 'Hello 1 {}'.format(datetime.now())),
        'say-2': (t.execute, 'Hello 1 {}'.format(datetime.now())),
        'say-3': (t.execute, 'Hello 1 {}'.format(datetime.now())),
        'collect': (write, 'say-1', 'say-2', 'say-3')
    }


    r = get_client().get(dsk, 'collect')

    res = Result()
    res.exit_code = 0
    res.exit_status = "OK"
    res.outputs = [r]
    return res
