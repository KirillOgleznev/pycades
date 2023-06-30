from setuptools import setup
from pathlib import Path

from wheel.bdist_wheel import bdist_wheel


def repair_wheel(dist_dir='dist'):
    import os

    auditwheel_cmd = 'auditwheel repair --plat {plat} ' + dist_dir + '/*.whl'

    os.system(auditwheel_cmd.format(plat='manylinux_2_35_x86_64'))
    os.system(auditwheel_cmd.format(plat='manylinux_2_34_x86_64'))
    os.system(auditwheel_cmd.format(plat='manylinux_2_31_x86_64'))
    os.system(auditwheel_cmd.format(plat='manylinux_2_28_x86_64'))
    os.system(auditwheel_cmd.format(plat='manylinux_2_27_x86_64'))
    os.system(auditwheel_cmd.format(plat='manylinux_2_24_x86_64'))

    os.system('mv ./wheelhouse/*.whl /server/dist')


class BdistWheel(bdist_wheel):
    def run(self):
        bdist_wheel.run(self)
        self.execute(repair_wheel, (self.dist_dir,), msg="repair wheel")


setup(
    name='pycades',
    version='1.1.3',
    author="Kirill Ogleznev",
    author_email="kirill24680@gmail.com",
    description="""Расширение Pycades предоставляет программный интерфейс, аналогичный КриптоПро""",
    packages=['pycades'],
    package_data={
        'pycades': ['pycades.so'],
    },
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    cmdclass={
        'bdist_wheel': BdistWheel,
    },
)
