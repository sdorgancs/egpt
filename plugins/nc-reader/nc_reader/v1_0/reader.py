from egpt.order import JobOrder
from time import sleep
import xarray as xr
from typing import Union, TextIO, BinaryIO
import types
NAME="nc-reader"
VERSION="1.0"
FORMATS=[
    ("nc", "NetCDF4")
]

def read(filename: str) -> xr.Dataset:
    return xr.open_dataset(filename)
