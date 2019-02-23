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
First install Python 3.7.1 or better and clone this repository.

```bash
mkdir -p ~/.egpt/plugins
# Update your .profile to persit this change
export PYTHONPATH=$PYTHONPATH:~/.egpt/plugins
# Install egpt core modules
pip install egpt/

# (Optionnal) Install egpt test plugins
cd egpt/plugins
pip install nc_reader/ --target=$HOME/.egpt/plugins
pip install test_task/ --target=$HOME/.egpt/plugins
pip install test_wf/ --target=$HOME/.egpt/plugins

# (Optionnal) Test plugins installation
python egpt/egpt/modules.py
```