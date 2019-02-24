from distributed import get_worker
def execute(data):
  return "I am worker {}, {}".format(get_worker().address, data)