from . import pycades
import os

# Сохранение текущей рабочей директории
current_directory = os.getcwd()

# Директория, содержащая библиотеку pycades.so
pycades_directory = os.path.dirname(os.path.abspath(__file__))


class PycadesModuleWrapper:
    """
    Класс-обертка для модуля _pycades.

    Args:
        original_instance: Оригинальный объект модуля _pycades.
    """

    def __init__(self, original_instance):
        self._original_instance = original_instance

    @staticmethod
    def is_python_type(value):
        return isinstance(value, (int, float, str, list, tuple, dict, set, bool, bytes, bytearray, complex))

    def __call__(self, *args, **kwargs):
        """
        Обертка для вызова функций модуля _pycades, в директории пакета

        Returns:
            Результат вызова функции модуля _pycades.
        """
        os.chdir(pycades_directory)
        args = [
            arg if not isinstance(arg, PycadesModuleWrapper) else arg._original_instance
            for arg in args
        ]
        # Проверка, являются ли значения **kwargs экземплярами PycadesModuleWrapper
        kwargs = {
            key: value if not isinstance(value, PycadesModuleWrapper) else value._original_instance
            for key, value in kwargs.items()
        }

        value = self._original_instance(*args, **kwargs)
        value = value if self.is_python_type(value) else PycadesModuleWrapper(value)
        # Восстановление предыдущей директории
        os.chdir(current_directory)
        return value

    def __getattr__(self, name):
        """
        Обертка для доступа к атрибутам модуля _pycades, в директории пакета

        Returns:
            Значение атрибута модуля _pycades.
        """
        if name == '_original_instance':
            return super().__getattribute__(name)
        os.chdir(pycades_directory)
        value = getattr(self._original_instance, name)
        value = value if self.is_python_type(value) else PycadesModuleWrapper(value)
        # Восстановление предыдущей директории
        os.chdir(current_directory)
        return value

    def __setattr__(self, name, value):
        if name == '_original_instance':
            super().__setattr__(name, value)
        else:
            setattr(self._original_instance, name, value)

    def __delattr__(self, name):
        delattr(self._original_instance, name)

    def __repr__(self):
        return self._original_instance.__repr__()

    def __class__(self):
        return type(self._original_instance)

    def __instancecheck__(self, instance):
        return isinstance(instance, type(self._original_instance))

    def __subclasscheck__(self, subclass):
        return issubclass(subclass, type(self._original_instance))

    def __class_getitem__(self, item):
        return type(self._original_instance)[item]

    def __getitem__(self, item):
        return self._original_instance[item]

    def __bool__(self):
        return bool(self._original_instance)

    def __len__(self):
        return len(self._original_instance)

    def __iter__(self):
        return iter(self._original_instance)

    def __next__(self):
        return next(self._original_instance)

    def __contains__(self, item):
        return item in self._original_instance

    def __eq__(self, other):
        # if isinstance(other, PycadesModuleWrapper):
        #     return self._original_instance is other._original_instance
        return self._original_instance == other

    def __ne__(self, other):
        return self._original_instance != other

    def __lt__(self, other):
        return self._original_instance < other

    def __le__(self, other):
        return self._original_instance <= other

    def __gt__(self, other):
        return self._original_instance > other

    def __ge__(self, other):
        return self._original_instance >= other

    def __hash__(self):
        return hash(self._original_instance)

    def __add__(self, other):
        return self._original_instance + other

    def __sub__(self, other):
        return self._original_instance - other

    def __mul__(self, other):
        return self._original_instance * other

    def __truediv__(self, other):
        return self._original_instance / other

    def __floordiv__(self, other):
        return self._original_instance // other

    def __mod__(self, other):
        return self._original_instance % other

    def __pow__(self, other):
        return self._original_instance ** other

    def __reversed__(self):
        return reversed(self._original_instance)

    def __missing__(self, key):
        return self._original_instance.__missing__(key)

    def __enter__(self):
        return self._original_instance.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._original_instance.__exit__(exc_type, exc_val, exc_tb)

    def __bytes__(self):
        return bytes(self._original_instance)

    def __format__(self, format_spec):
        return self._original_instance.__format__(format_spec)

    def __get__(self, instance, owner):
        return self._original_instance.__get__(instance, owner)

    def __set__(self, instance, value):
        self._original_instance.__set__(instance, value)

    def __delete__(self, instance):
        self._original_instance.__delete__(instance)

    def __dir__(self):
        self._original_instance.__dir__()


# Создание экземпляра класса-обертки для модуля _pycades
pycades = PycadesModuleWrapper(pycades)
