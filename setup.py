import os
from pathlib import Path

from setuptools import setup
from wheel.bdist_wheel import bdist_wheel


# Восстановление исправленного пакета
# (не актуальна тк пакеты были восстановлены вручную)
class RepairBdistWheel(bdist_wheel):
    def run(self):
        bdist_wheel.run(self)
        # Функция для восстановления исправленного пакета
        self.repair_wheel()

    def repair_wheel(self):
        # Восстановление пакетов для разных платформ
        platforms = ['manylinux_2_35_x86_64', 'manylinux_2_34_x86_64', 'manylinux_2_31_x86_64',
                     'manylinux_2_28_x86_64', 'manylinux_2_27_x86_64', 'manylinux_2_24_x86_64']
        for platform in platforms:
            self.execute_auditwheel(platform)

    def execute_auditwheel(self, platform):
        auditwheel_cmd = f'auditwheel repair --plat {platform} {self.dist_dir}/*.whl'
        self.spawn(auditwheel_cmd)


setup(
    name='pycades',
    version='1.1.5',
    author="Kirill Ogleznev",
    author_email="kirill24680@gmail.com",
    description="""Расширение Pycades предоставляет программный интерфейс, аналогичный КриптоПро""",
    packages=[
        'pycades',
        'pycades.config64.cprocsp',
        'pycades.config-123456.cprocsp',
        'pycades.cprocsp.lib.amd64',
        'pycades.vr.opt.cprocsp.dsrf.db1',
        'pycades.vr.opt.cprocsp.dsrf.db2',
        'pycades.vr.opt.cprocsp.keys.root.hsm_keys',
        'pycades.vr.opt.cprocsp.tmp',
        'pycades.vr.opt.cprocsp.tmpcerts.ca',
        'pycades.vr.opt.cprocsp.tmpcerts.root',
        'pycades.vr.opt.cprocsp.users',
        'pycades.vr.opt.cprocsp.users.root.stores',
        'pycades.vr.opt.cprocsp.users.stores',
    ],
    package_data={
        'pycades': [
            '_pycades.so',
            'config64/cprocsp/config64.ini',
            'config64/cprocsp/license.ini',
            'config-123456/cprocsp/config64.ini',
            'config-123456/cprocsp/license.ini',
            *[os.path.join(dp[8:], f) for dp, _, filenames in os.walk('pycades/vr') for f in filenames],
            *[os.path.join(dp[8:], f) for dp, _, filenames in os.walk('pycades/cprocsp') for f in filenames],
        ],
    },
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    # cmdclass={
    #     'bdist_wheel': RepairBdistWheel,
    # },
)
