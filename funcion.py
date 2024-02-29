class Funcion:

    def __init__(self, nombre_de_funcion: str, variables_de_entrada: list, variables_de_salida: list):
        self.nombre = str(nombre_de_funcion)
        self.variables_in = [] + variables_de_entrada
        self.variables_out = [] + variables_de_salida

    def es_ejecutable(self, lista_variables_disponibles: list):
        if len(lista_variables_disponibles) > 0:
            variables_que_faltan = []
            for variable_in in self.variables_in:
                if variable_in not in lista_variables_disponibles:
                    variables_que_faltan.append(variable_in)
            if len(variables_que_faltan) > 0:
                return False, variables_que_faltan
            else:
                return True, []
        return False, [] + self.variables_in

    def __str__(self):
        return f'{self.nombre} ({", ".join(self.variables_in)}) = {", ".join(self.variables_out)}'
