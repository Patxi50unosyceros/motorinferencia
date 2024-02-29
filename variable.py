from enum import Enum
from funcion import Funcion

class Variable:

    class EstadoVariable(Enum):
        CON_DATOS = 1
        SIN_DATOS = 2
        INDEFINIDO = 3

    def __init__(self, nombre_de_variable: str):
        self.nombre = str(nombre_de_variable)
        self.funciones_out = []  # funciones en cuya salida aparece esta variable
        self.funciones_in = []  # funciones en cuya entrada aparece esta variable
        self.valor = self.EstadoVariable.INDEFINIDO

    def consultar_funciones_in(self):
        salida = []
        for funcion in self.funciones_in:
            if type(funcion) is Funcion:
                salida.append(funcion.nombre)
        return salida

    def consultar_funciones_out(self):
        salida = []
        for funcion in self.funciones_out:
            if type(funcion) is Funcion:
                salida.append(funcion.nombre)
        return salida

    def asignar_valor(self):
        self.valor = self.EstadoVariable.CON_DATOS

    def resetear_valor(self):
        self.valor = self.EstadoVariable.SIN_DATOS

    def tenemos_datos(self):
        if self.valor == self.EstadoVariable.CON_DATOS:
            return True
        return False
    
    def __str__(self):
        salida = f'  Variable <{self.nombre}> '
        for funcion in self.funciones_out:
            salida += '\n    F '
            salida += str(funcion)  # informa funcion saliente
        for funcion in self.funciones_in:
            salida += '\n    f '
            salida += str(funcion)  # informa funcion entrante
        return salida
