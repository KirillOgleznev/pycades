import os
from os import listdir

# Получение списка файлов в директории 'pycades/cprocsp/lib/amd64'
file_list = [f for f in listdir('pycades/cprocsp/lib/amd64')]

# Проход по каждому файлу в списке и применение команды 'patchelf' для каждого файла
for file in file_list:
    cmd = 'patchelf --force-rpath --set-rpath $ORIGIN pycades/cprocsp/lib/amd64/{file}'
    print(file)
    os.system(cmd.format(file=file))

# Проход по каждому файлу в обновленном списке и выполнение команды 'strings' с использованием 'grep'
for file in file_list:
    print('--', file)
    # cmd = 'objdump -s pycades/cprocsp/lib/amd64/{file} | grep /etc/opt'
    cmd = 'strings pycades/cprocsp/lib/amd64/{file} | grep libcpui.so.4'
    # cmd = 'xxd -p pycades/cprocsp/lib/amd64/{file} | grep 2f657463'
    os.system(cmd.format(file=file))
