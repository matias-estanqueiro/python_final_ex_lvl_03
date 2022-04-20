"""Modulo con el patron observador, el cual realizará un registro por consola del CRUD. El modulo se reutilizo del ejercicio de la unidad_6, y se lo aplico a la app"""
from datetime import datetime


class Sujeto:
    """Mantiene una lista de sus dependientes, llamados observadores, y les notifica
    automáticamente cualquier cambio de estado, generalmente llamando a uno de sus métodos"""

    observadores = []

    def agregar(self, obj):
        """Agrega"""
        self.observadores.append(obj)

    def notificar(self, *args):
        """Actualiza"""
        for observador in self.observadores:
            observador.update(*args)


class ObservadorNoDefinido:
    """Excepcion en caso de que el observador no tenga un metodo update definido"""

    def update(self):
        """Levanta la excepcion"""
        raise NotImplementedError("Delegación de actualización")


class Observador(ObservadorNoDefinido):
    """Clase que define la logica del observador"""

    def __init__(self, obj):
        self.obser = obj
        self.obser.agregar(self)

    def update(self, *args):
        log = open("log_crud_observer.txt", "a", encoding="utf-8")
        log.write(f"{datetime.today().strftime('%Y-%m-%d %H:%M')} -- {args}\n")
        log.close()
