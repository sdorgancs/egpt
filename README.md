# EGPT

This project is developped in Python 3.7.1 and it is only a demonstration project to evaluate the use of dask to create a distributed prototyping environment to help EUMETSAT developpers and scientists to create applications that use satellite instrument data.

# Main dependencies
## dask>=1.0 and distributed>=1.25.1
dask.distributed is the central component of this projetc, it is used to distribute the computing load over a cluster of machine
## xarray>=0.11.0
xarray dataframe are used read, distribute and manipulate satellites instrument data over the dask.distributed cluster

# Installation
## Install Python and EGPT
On each machine participating to the cluster: 

- First install Python 3.7 with development headers, miniconda is a simple option

```bash
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
$ # Update your user profile to persit this change
$ export PATH=/miniconda/bin:${PATH}
$ conda update -y conda && conda create --name dev python=3.7.1 --channel conda-forge
```

- then clone this repository.

```bash
$ git clone https://github.com/sdorgancs/egpt.git
$ mkdir -p ~/.egpt/plugins
$ # Update your user profile to persit this change
$ export PYTHONPATH=$PYTHONPATH:~/.egpt/plugins
$ # Install egpt core modules
$ pip install egpt/

# (Optionnal) Install egpt test plugins
$ pip install egpt/plugins/nc_reader/ --target=$HOME/.egpt/plugins
$ pip install egpt/plugins/test_task/ --target=$HOME/.egpt/plugins
$ pip install egpt/plugins/test_wf/ --target=$HOME/.egpt/plugins

$ # (Optionnal) Test plugins installation
$ python egpt/egpt/modules.py
```
## Create the cluster
On the master machine run
```bash
$ dask-scheduler
```
On all the machine participating to the cluster (master included or not) run
```bash
$ dask-worker <master>:8786
```
where \<master> is the name or the ip address of the master host

# Play with docker
## Local install
Local install is very simple
```bash
$ git clone https://github.com/sdorgancs/egpt.git
$ cd egpt
$ docker build -t egpt
$ docker-compose up
```

## Build a swarm
### First create a swarm cluster:
On the master machine run
```bash
$ docker swarm init
Swarm initialized: current node (bvz81updecsj6wjz393c09vti) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx \
    172.17.0.2:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```
On the other machines run the command returned by swarm init to join the cluster

### Build egpt docker image
On each machine participating to the cluster:

```bash
$ git clone https://github.com/sdorgancs/egpt.git
$ cd egpt && docker build -t egpt
```

### Deploy stack
On the master machine:
```bash
$ docker stack deploy --compose-file egpt/docker-compose.yml egpt-cluster
Creating network egpt-cluster_cluster-net
Creating service egpt-cluster_worker1
Creating service egpt-cluster_worker2
Creating service egpt-cluster_worker3
Creating service egpt-cluster_scheduler
```
then run 
```bash
$ docker stack ps egpt-cluster
ID                  NAME                       IMAGE               NODE                 DESIRED STATE       CURRENT STATE           ERROR                       PORTS
q0acl1413lin        egpt-cluster_worker1.1     egpt:latest         sdorgan-AERO-15XV8   Running             Running 2 minutes ago                               
teljdg8vw8we        egpt-cluster_worker3.1     egpt:latest         sdorgan-AERO-15XV8   Running             Running 2 minutes ago                               
wtrg97as9zu6        egpt-cluster_scheduler.1   egpt:latest         sdorgan-AERO-15XV8   Running             Running 2 minutes ago                               
8fax95zwl0ih        egpt-cluster_worker2.1     egpt:latest         sdorgan-AERO-15XV8   Running             Running 2 minutes ago                               
```
to check services are up

# Run your first Workflow
First, if you are using docker-compose or swarm, find the scheduler container
```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
c908b8aa262c        egpt:latest         "dask-worker tcp://s…"   3 seconds ago       Up 1 second                             egpt-cluster_worker3.1.jthezuh19wadzf06bp5b33ox1
bb25410bfc3d        egpt:latest         "dask-worker tcp://s…"   7 seconds ago       Up 5 seconds                            egpt-cluster_worker2.1.63ooe478a114ep3hv99usw4an
c49e5350c144        egpt:latest         "dask-worker tcp://s…"   9 seconds ago       Up 8 seconds                            egpt-cluster_worker1.1.z9q1yyeek7yw63v5gw1cuhza8
03b5d083e751        egpt:latest         "dask-scheduler"         11 seconds ago      Up 9 seconds                            egpt-cluster_scheduler.1.jxw8e3kpi7s45v8j5buo6n8s1
```
enter in the container
```bash
docker exec -ti egpt-cluster_scheduler.1.jxw8e3kpi7s45v8j5buo6n8s1 bash
root@dask-scheduler:/egpt#
```
run the 'Hello world' workflow (the scheduler options is used to pass the ip address or the name of the host where the scheduler is used)
```bash
root@dask-scheduler:/egpt$ python egpt.py job run orders/test.45.xml --scheduler scheduler:8786
egpt.processing.Result(exit_status='OK', outputs=['/tmp/tmpkwuyl8mo'])
```
This workflow is very simple but illustrates the mechanisms of this prototype
```python
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
```
The workflow starts by running _say-1_, _say-2_ and _say-3_ activities in parallel. These activities run a task plugin,_test-task_ version _1.0_. The returned values of  _say-1_, _say-2_ and _say-3_ are collected by the _collect_ activity to be writen in a temporary file. If everithing is Ok the content of this file should be like this:
```bash
root@dask-scheduler:/egpt$ cat /tmp/tmpkwuyl8mo
I am worker tcp://10.0.10.13:38183, Hello 1 2019-02-24 15:04:56.199849
I am worker tcp://10.0.10.14:44115, Hello 2 2019-02-24 15:04:56.199859
I am worker tcp://10.0.10.9:37639, Hello 3 2019-02-24 15:04:56.199861
```
We can see that the 3 tasks have been run in the same time on 3 differents workers
