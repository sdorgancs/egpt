import xarray as xr
from os import path
import numpy as np
from distributed import Client, wait
import math


def reflectance(radiance: float,   solar_flux: float, angle: float) -> float:
    if math.isnan(radiance) or math.isnan(solar_flux) or math.isnan(angle):
        return math.nan
    return max(0, min(1., math.pi * (radiance / solar_flux) / math.cos(math.radians(angle))))

def band_index(name):
    return int(name[2:4]) - 1 

def solar_flux(ds, band_name, x, y):
    didx = ds["detector_index"].values[x, y]
    if math.isnan(didx):
        return math.nan
    return ds["solar_flux"].values(band_index(band_name), int(didx))

def sza(ds, x):
    return ds["SZA"].values(x, 0)

def func(da):
    array = xr.zeros_like(da)
    print(da)

def get_dataset():
    product = "/home/sdorgan/Desktop/Shared/Projets/EGPT/Data/S3A_OL_1_EFR____20190207T101301_20190207T101601_20190207T120253_0180_041_122_2160_LN1_O_NR_002.SEN3/"

    files = [
        path.join(product, "Oa10_radiance.nc"),#Red
        path.join(product, "Oa05_radiance.nc"),#Green
        path.join(product, "Oa03_radiance.nc"),#Blue
        path.join(product, "instrument_data.nc"),
        path.join(product, "tie_geometries.nc"),
    ]
    
    return xr.open_mfdataset(files)


if __name__ == "__main__":
    client = Client()

    ds = get_dataset()
    print(ds)
    ds.attrs["title"] = "Composite"

    #print(ds)
    print(ds["detector_index"].sizes["columns"])
    print(ds["detector_index"].sizes["rows"])
    idx = ds["detector_index"].values.copy()
    idx[np.isnan(idx)] = 0
    print(idx.max())

    print(band_index("Oa10_radiance"))
    client.close()
    # red = ds["Oa10_radiance"]
    # red = red.chunk((1, red.shape[1]))
    # print(red)

    # res = client.map(func,red)
    # wait(res)

    # angles = ds["SZA"]
