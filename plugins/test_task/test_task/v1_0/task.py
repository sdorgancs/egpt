from prettyprinter import cpprint
from distributed import get_worker
import math

def reflectance(radiance: float, solar_flux: float, sza: float) -> float:
    if math.isnan(radiance) or math.isnan(solar_flux) or math.isnan(sza):
        return math.nan
    return max(0, min(1., math.pi * (radiance / solar_flux) / math.cos(math.radians(sza))))

def band_index(name: str) -> int:
    return int(name[2:4]) - 1 

def solar_flux(ds, band_name, x, y):
    didx = ds["detector_index"].values[x, y]
    if math.isnan(didx):
        return math.nan
    return ds["solar_flux"].values(band_index(band_name), int(didx))

def sza(ds, x):
    return ds["SZA"].values(x, 0)

def execute(data):
   pass