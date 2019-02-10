from setuptools import setup
import egpt

setup(name=egpt.__name__,
      version=egpt.__version__,
      description='EGPT Pototype',
      url='http://somewhere',
      author='CS SI',
      author_email='sebastien.dorgan@c-s.fr',
      license='MIT',
      packages=['egpt'],
      zip_safe=False,
      python_requires='>=3.7',
      install_requires=[
          "xarray>=0.11.0",
          "dask>=1.0",
          "distributed>=1.25.1",
          "bottle>=0.12.16",
          "ifaddr>=0.1.6"
      ]) 
