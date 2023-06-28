from setuptools import setup

setup(
    name='pycades',
    version='28.06.2023',
    author="Kirill",
    author_email="kirill24680@gmail.com",
    description="""Расширение Pycades предоставляет программный интерфейс, аналогичный КриптоПро""",
    py_modules=["pycades"],
    packages=['pycades'],
    package_data={
        'pycades': ['pycades.so', '/opt/cprocsp/lib/amd64/libcppcades.so.2'],
    },
)
