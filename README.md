# egpt

This project is developped in Python 3.7.1 and it is only a demonstration project to evaluate the use of dask to create a distributed prototyping environment to help EUMETSAT developpers and scientists to create applications that use satellite instrument data.

# Main dependencies
## dask>=1.0 and distributed>=1.25.1
dask.distributed is the central component of this projetc, it is used to distribute the computing load over a cluster of machine
## xarray>=0.11.0
xarray dataframe are used read, distribute and manipulate satellites instrument data over the dask.distributed cluster
## bottle>=0.12.16
bottle is used to implemented the debugging server

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
Go back to the master machine and create a swarm network:
```bash
docker network create -d overlay cluster-net
```

### Build egpt docker image
On each machine participating to the cluster:

```bash
$ git clone https://github.com/sdorgancs/egpt.git
$ cd egpt && docker build -t egpt
```