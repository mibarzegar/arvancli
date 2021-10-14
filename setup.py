from setuptools import setup, find_packages

setup(name='arvancli', version='0.1', packages=find_packages(), entry_points={'console_scripts': ['arvancli = arvancli.main:main',],})
