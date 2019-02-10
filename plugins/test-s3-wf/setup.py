from setuptools import setup
import test_s3_wf

setup(name=test_s3_wf.__name__,
      version=test_s3_wf.__version__,
      description='A test workflow',
      url='http://somewhere',
      author='CS SI',
      author_email='sebastien.dorgan@c-s.fr',
      license='MIT',
      packages=['test-s3-_wf'],
      zip_safe=False)