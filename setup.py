from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="RaspiMonitor",
    version="1.0.0",
    author="Jyrki Karjalainen",
    description="School project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/0x4aK/laiteohjelmointi",

    python_requires='>=3.6',
    install_requires=['CherryPy', 'schedule', 'sense-hat'],

    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['raspimonitor.service' ,'public/*', 'public/js/*', 'public/css/*']},

    entry_points={
        'console_scripts': ['raspimonitor=raspimonitor.main:main'],
    },
)
