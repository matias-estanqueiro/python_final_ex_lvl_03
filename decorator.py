# pylint: disable=line-too-long

"""Importacion de modulos"""
from datetime import datetime


def registro_log(function):
    """Generacion de log en archivo txt de las operaciones CRUD realizadas. Almacena fecha y hora + CRUD + datos utilizados"""

    def wrap(*args):
        log = open("log_crud_decorator.txt", "a", encoding="utf-8")
        log.write(
            f"{datetime.today().strftime('%Y-%m-%d %H:%M')} -- {function.__name__} -- {args}\n"
        )
        log.close()
        return function(*args)

    return wrap
