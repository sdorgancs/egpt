from egpt.order import JobOrder
from egpt import tasks
from egpt.readers import read_task_inputs
from distributed import get_client
from egpt.processing import Result
from datetime import datetime
from distributed import Client
from importlib import invalidate_caches
from os import path

def execute(order: JobOrder) -> Result:

    #Find tasks
    load = tasks.find('load', '0.1')
    cos = tasks.find('apply-cos', '0.1')
    add = tasks.find('add', '0.1')
    store = tasks.find('store', '0.1')

    #Read inputs
    ds = read_task_inputs(load.__name__, load.__version__, order)

    dsk = {
        'load-1': (load.execute, ds.attrs["Oa01_radiance"]),
        'load-2': (load.execute, ds.attrs["Oa02_radiance"]),
        'load-3': (load.execute, ds.attrs["Oa03_radiance"]),
        'transform-1': (cos.execute, 'load-1'),
        'transform-2': (cos.execute, 'load-2'),
        'transform-3': (cos.execute, 'load-3'),
        'sum': (add.execute, "transform-1", "transform-2", "transform-3"),
        'store': (store, 'sum', "/SHARED/result.nc")
    }

    # Create result 
    res = Result()
    get_client().get(dsk, "store")
    res.stop = datetime.now()
    res.exit_code = 0
    res.output = ["/SHARED/result.nc"]

    return res
