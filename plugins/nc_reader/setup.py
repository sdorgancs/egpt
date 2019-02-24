from setuptools import setup
import nc_reader
import json
from pathlib import Path

import os
import egpt.readers as readers



setup(name=nc_reader.__name__,
      version=nc_reader.__version__,
      description=f'EGPT READER: NetCDF 4 reader version {nc_reader.__version__}',
      url='http://somewhere',
      author='CS SI',
      author_email='sebastien.dorgan@c-s.fr',
      license='MIT',
      packages=['nc_reader.v1_0', "nc_reader"],
      classifiers=[
          "Type :: EGPT-READER",
          "Formats :: NetCDF4, HDF5",
          "Extensions :: nc, cdf, hdf, h5, hdf5, he5"
          ],
      zip_safe=False)
