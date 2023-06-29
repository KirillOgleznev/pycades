from setuptools import setup
from pathlib import Path


setup(
    name='pycades',
    version='1.1.2',
    author="Kirill",
    author_email="kirill24680@gmail.com",
    description="""Расширение Pycades предоставляет программный интерфейс, аналогичный КриптоПро""",
    packages=['pycades'],
    package_data={
        'pycades': ['pycades.so'],
    },
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
)
