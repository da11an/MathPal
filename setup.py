import os
from setuptools import setup, find_packages
from pathlib import Path

requirements = []

__version__ = "0.0.0"


setup(
    name="MathPal",
    version=__version__,
    packages=find_packages(),
    license="GNU GPL 3.0",
    author="Dallan Prince",
    author_email="dallan.prince@gmail.com",
    url="https://github.com/da11an/MathPal",
    install_requires=requirements,
    python_requires=">=3.6, <4",
    description="Learn Math Facts Games",
    include_package_data=True,
    entry_points={
        "console_scripts": ["MathPal=MathPal:main"]
    },
)