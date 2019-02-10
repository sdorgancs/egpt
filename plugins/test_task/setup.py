from setuptools import setup
import test_task

setup(name=test_task.__name__,
      version=test_task.__version__,
      description='EGPT TASK: A test task',
      url='http://somewhere',
      author='CS SI',
      author_email='sebastien.dorgan@c-s.fr',
      license='MIT',
      packages=[ 'test_task.v1_0', 'test_task'],
      classifiers=[
          "Type :: EGPT-TASK"
          ],
      zip_safe=False)