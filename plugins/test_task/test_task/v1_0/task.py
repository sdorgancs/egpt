from distributed import get_worker
from time import sleep
def execute(data):
    sleep(5)
    return "I am worker {}, {}".format(get_worker().address, data)