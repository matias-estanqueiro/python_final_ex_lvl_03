# pylint: disable=line-too-long

"""Modulos a utilizar"""
from tkinter import Tk
import view
import observer


class Aplicacion:
    """Controlador de la aplicacion, trabaja sobre la interfaz de la misma"""

    def __init__(self, root):
        """Constructor de la clase. Definiciones para utilizar la vista de la aplicacion (view.py)"""
        self.root_controler = root
        self.obj_vista = view.VentanaAplicacion(self.root_controler)
        # Instancia de ABMC desde el controlador
        self.mi_observador = observer.Observador(self.obj_vista.base_datos)


if __name__ == "__main__":
    root_tk = Tk()
    app = Aplicacion(root_tk)
    root_tk.mainloop()
