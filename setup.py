from setuptools import setup
from wheel.bdist_wheel import bdist_wheel
from pathlib import Path
import os


class BdistWheelCommand(bdist_wheel):
    def run(self):
        """Run command."""
        bdist_wheel.run(self)
        auditwheel_cmd = 'auditwheel repair --plat {plat} dist/*.whl'
        mv_cmd = 'mv ./wheelhouse/*.whl ./dist'
        os.system(auditwheel_cmd.format(plat='manylinux_2_35_x86_64'))
        os.system(auditwheel_cmd.format(plat='mv_cmd'))


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
    cmdclass={
        'bdist_wheel': BdistWheelCommand,
    },
)
