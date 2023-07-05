import importlib.util
import os

# Сохранение текущей рабочей директории
current_directory = os.getcwd()

# Директория, содержащая библиотеку pycades.so
pycades_directory = os.path.dirname(os.path.abspath(__file__))


def load_library():
    """
    Загружает библиотеку _pycades.so из директории pycades_directory.

    Returns:
        Загруженный модуль _pycades.
    Raises:
        ImportError: Если файл _pycades.so не найден.
    """
    # Получение абсолютного пути к файлу .so
    so_file_path = os.path.join(pycades_directory, "_pycades.so")

    # Проверка существования файла .so
    if not os.path.exists(so_file_path):
        raise ImportError("Библиотека _pycades.so не найдена")

    # Загрузка .so файла
    try:
        spec = importlib.util.spec_from_file_location(__name__, so_file_path)
        pycades_lib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pycades_lib)
    except Exception as e:
        raise ImportError(f"Ошибка загрузки библиотеки _pycades.so: {e}")

    # Возвращение загруженной библиотеки
    return pycades_lib


load_library()
