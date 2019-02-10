from setuptools import setup
import test_wf

setup(name=test_wf.__name__,
      version=test_wf.__version__,
      description='EGPT WORFLOW: Test workflow',
      url='http://somewhere',
      author='CS SI',
      author_email='sebastien.dorgan@c-s.fr',
      license='MIT',
      packages = ['test_wf', 'test_wf.v1_0'],
      classifiers = [
            "Type :: EGPT-WORKFLOW",
      ],
      zip_safe=False)