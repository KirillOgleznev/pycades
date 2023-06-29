from setuptools import setup


setup(
    name='pycades',
    version='1.1.0',
    author="Kirill",
    author_email="kirill24680@gmail.com",
    description="""Расширение Pycades предоставляет программный интерфейс, аналогичный КриптоПро""",
    packages=['pycades'],
    package_data={
        'pycades': ['pycades.so'],
    },
)
