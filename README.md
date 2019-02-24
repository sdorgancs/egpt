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
$ mkdir -p ~/.egpt/plugins
$ # Update your user profile to persit this change
$ export PYTHONPATH=$PYTHONPATH:~/.egpt/plugins
$ # Install egpt core modules
$ pip install egpt/

# (Optionnal) Install egpt test plugins
$ cd egpt/plugins
$ pip install plugins/nc_reader/ --target=$HOME/.egpt/plugins
$ pip install plugins/test_task/ --target=$HOME/.egpt/plugins
$ pip install plugins/test_wf/ --target=$HOME/.egpt/plugins

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