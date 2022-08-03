from setuptools import setup, find_packages

setup(
    name='timer',
    version='0.0.1',
    description='A simple timer for profiling python code',
    author='Cameron Allen',
    author_email=('csal@brown.edu'),
    packages=find_packages(include=['timer', 'timer.*']),
    url='https://github.com/camall3n/timer/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
