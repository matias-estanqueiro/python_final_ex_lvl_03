# pylint: disable=line-too-long

"""Modulos a utilizar"""
from tkinter.messagebox import showerror, showinfo
import re
from peewee import SqliteDatabase, Model, TextField, IntegrityError
from decorator import registro_log
from observer import Sujeto

db = SqliteDatabase("personal_v3.db")


class BaseModel(Model):
    """Base de datos a utilizar"""

    class Meta:
        """Se define el modelo de base de datos a utilizar para toda la app"""

        database = db


class Personal(BaseModel):
    """Tabla de base de datos y definicion de los tipos de field. Se utiliza el formato TextField ya que no se requiere la información numerica para realizar operaciones"""

    documento = TextField(primary_key=True)
    nombre = TextField()
    apellido = TextField()
    empresa = TextField()
    telefono = TextField()
    email = TextField()
    direccion = TextField()
    nacimiento = TextField()


# Conexion con la base de datos. La conexion permanecera abierta en todo momento #
db.connect()
# Se crea la tabla a partir de la clase definida #
db.create_tables([Personal])


class MostrarAlertas:
    """Clase para mostrar los errores o la informacion al usuario mediante cuadros de dialogo durante la ejecucion de la aplicacion"""

    def mensaje_error(self, desc_error):
        """Muestra mensaje de error"""
        showerror("Error", desc_error)

    def mensaje_ok(self, desc_mensaje):
        """Muestra mensaje de informacion"""
        showinfo("Mensaje", desc_mensaje)


class ValidarDatos:
    """Metodos para realizar la validacion de los datos, en caso de que alguno no cumpla con el formato especificado, no se realizara la consulta. Las validaciones al ya estar determinadas a traves de expresiones regulares de la versión anterior, se sigue con este patron"""

    def __init__(self):
        """Instancia la clase MostrarAlertas, la cual utiliza para enviar al usuario mensajes mediante cuadros de dialogo"""
        self.alertas = MostrarAlertas()

    def validar_dni(self, dni):
        """Validacion mediante expresiones regulares del campo DNI"""
        patron_dni = "^[0-9]{7,8}$"
        if not re.match(patron_dni, dni):
            self.alertas.mensaje_error("Por favor introduzca un formato de DNI valido")
            return False

    def validar_telefono(self, telefono):
        """Validacion mediante expresiones regulares del campo telefono"""
        patron_telefono = "^[0-9]{10,20}$"
        if not re.match(patron_telefono, telefono):
            self.alertas.mensaje_error(
                "Por favor introduzca un formato de telefono valido"
            )
            return False

    def validar_email(self, email):
        """Validacion mediante expresiones regulares del campo email"""
        patron_mail = "^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
        if not re.match(patron_mail, email):
            self.alertas.mensaje_error(
                "Por favor introduzca un formato de email valido"
            )
            return False

    def validar_nacimiento(self, nacimiento):
        """Validacion mediante expresiones regulares del campo nacimiento (fecha)"""
        patron_nacimiento = "^^(((0[1-9]|[12][0-9]|30)[-/]?(0[13-9]|1[012])|31[-/]?(0[13578]|1[02])|(0[1-9]|1[0-9]|2[0-8])[-/]?02)[-/]?[0-9]{4}|29[-/]?02[-/]?([0-9]{2}(([2468][048]|[02468][48])|[13579][26])|([13579][26]|[02468][048]|0[0-9]|1[0-6])00))$"
        if not re.match(patron_nacimiento, nacimiento):
            self.alertas.mensaje_error(
                "Por favor introduzca un formato de fecha valido"
            )
            return False


class BaseDeDatos(Sujeto):
    """Operaciones de CRUD para el manejo de la base de datos SQLite3 a traves de ORM peewee"""

    def __init__(self):
        """Constructor de la clase"""
        # Instancias de las clases creadas #
        self.alertas = MostrarAlertas()
        self.validar = ValidarDatos()
        # Pylint recomienda definir las variables en el constructor antes de utilizarlas #
        self.resultado_consulta = None
        self.con = None
        self.instruccion = None
        self.sql = None
        self.datos = None
        self.comprueba_dni = None
        self.comprueba_telefono = None
        self.comprueba_email = None
        self.comprueba_nacimiento = None
        self.empleado = None

    @registro_log
    def insertar_registro(self, dni, nom, ape, emp, tel, mail, dire, nac):
        """Inserta nuevos registros en la tabla personal en la base de datos personal_v3. Para que se puedan realizar el alta de datos, todos los campos deben estar completos (se realiza esta validacion) y correctos (se valida mediante regex)"""
        if (
            dni == ""
            or nom == ""
            or ape == ""
            or emp == ""
            or tel == ""
            or mail == ""
            or dire == ""
            or nac == ""
        ):
            self.alertas.mensaje_ok(
                "Para poder ingresar la información en la base de datos, todos los campos deben estar completos"
            )
        else:
            self.comprueba_dni = self.validar.validar_dni(dni)
            self.comprueba_telefono = self.validar.validar_telefono(tel)
            self.comprueba_email = self.validar.validar_email(mail)
            self.comprueba_nacimiento = self.validar.validar_nacimiento(nac)
            if (
                self.comprueba_dni is not False
                and self.comprueba_telefono is not False
                and self.comprueba_email is not False
                and self.comprueba_nacimiento is not False
            ):
                try:
                    self.empleado = Personal(
                        documento=dni,
                        nombre=nom,
                        apellido=ape,
                        empresa=emp,
                        telefono=tel,
                        email=mail,
                        direccion=dire,
                        nacimiento=nac,
                    )
                    # force_insert debido a que no se utiliza una key del tipo número / autoincremental en peewee #
                    self.empleado.save(force_insert=True)
                    self.alertas.mensaje_ok("La información fue agregada con exito")
                    self.notificar(dni, nom, ape, emp, tel, mail, dire, nac, "ALTA")
                except IntegrityError:
                    self.alertas.mensaje_error(
                        "ERROR: La operacion no pudo realizarse correctamente. POSIBLE MOTIVO: El dni ingresado ya se encuentra registrado"
                    )

    @registro_log
    def borrar_registro(self, dni, nom, ape, emp, tel, mail, dire, nac):
        """Elimina registros de la tabla 'personal' en la base de datos 'personal_v3'. Previamente realiza una validacion para comprobar que el DNI ingresado se encuentre en la base de datos"""
        # Se pasan los argumentos nom, ape, emp, tel, mail, dire y nac para poder registrar el log #
        try:
            borrar_empleado = Personal.get(Personal.documento == dni)
            borrar_empleado.delete_instance()
            self.notificar(dni, nom, ape, emp, tel, mail, dire, nac, "BORRAR")
        except:
            self.alertas.mensaje_error(
                "Error: La operacion no pudo realizarse correctamente"
            )

    @registro_log
    def actualizar_registro(self, dni, nom, ape, emp, tel, mail, dire, nac):
        """Actualiza registros de la tabla 'personal' en la base de datos 'personal_v3'. Previamente valida que el campo DNI realmente se encuentre almacenado en la base de datos (en caso de no encontrarlo avisa al usuario mediante ua alerta)"""
        try:
            query = Personal.update(
                nombre=nom,
                apellido=ape,
                empresa=emp,
                telefono=tel,
                email=mail,
                direccion=dire,
                nacimiento=nac,
            ).where(Personal.documento == dni)
            query.execute()
            self.alertas.mensaje_ok("Los datos se actualizaron correctamente")
            self.notificar(dni, nom, ape, emp, tel, mail, dire, nac, "MODIFICACION")
        except:
            self.alertas.mensaje_error(
                "Error: La operacion no pudo realizarse correctamente. POSIBLE MOTIVO: El DNI no se encuentra en la base de datos"
            )

    def buscar_registro(self, dni):
        """Busca registros de la tabla 'personal' de la base de datos 'personal_v3'. Este metodo tambien es utilizado en las operaciones de borrar y actualizar para traer los datos de la base de datos a la aplicacion"""
        try:
            query = Personal.get(Personal.documento == dni)
            resultado_busqueda = (
                query.documento,
                query.nombre,
                query.apellido,
                query.empresa,
                query.telefono,
                query.email,
                query.direccion,
                query.nacimiento,
            )
            return resultado_busqueda
        except:
            self.alertas.mensaje_error(
                "Error: La operacion no pudo realizarse correctamente. POSIBLE MOTIVO: El DNI no se encuentra en la base de datos"
            )
