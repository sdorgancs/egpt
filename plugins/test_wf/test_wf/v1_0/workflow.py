from datetime import datetime
from tempfile import NamedTemporaryFile

from distributed import get_client,wait

from egpt.order import JobOrder
from egpt.processing import Result
from egpt import tasks


def write(s1, s2, s3):
    with NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("{}\n{}\n{}\n".format(s1, s2, s3))
        f.flush()
        return f.name

def execute(order: JobOrder) -> Result:
    t = tasks.find("test-task", "1.0")

    dsk = {
        'say-1': (t.execute, 'Hello 1 {}'.format(datetime.now())),
        'say-2': (t.execute, 'Hello 2 {}'.format(datetime.now())),
        'say-3': (t.execute, 'Hello 3 {}'.format(datetime.now())),
        'collect': ['say-1', 'say-2', 'say-3']
    }

    r = get_client().get(dsk, 'collect')
    f = write(r[0], r[1], r[2])
    return Result(exit_code=0, exit_status="OK", outputs=[f])
