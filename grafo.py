from variable import Variable
from funcion import Funcion


class Grafo:

    def __init__(self):
        self.funciones = {}
        self.variables = {}

    def __str__(self):
        cadena = 'Contenido del Grafo de Variables\n'
        cadena += '\n'.join(str(variable) for variable in self.variables.values())
        return cadena

    def consultar_variables(self, diccionario=False):
        lista_conocido = []
        lista_desconocido = []
        for nombre_variable, variable_actual in self.variables.items():
            if type(variable_actual) is Variable:
                if variable_actual.tenemos_datos():
                    lista_conocido.append(nombre_variable)
                else:
                    lista_desconocido.append(nombre_variable)
        if diccionario:
            return {'conocidas': lista_conocido, 'desconocidas': lista_desconocido}
        else:
            return []+lista_conocido+lista_desconocido

    def get_variable(self, nombre_variable):
        if nombre_variable in list(self.variables.keys()):
            return True, self.variables.get(nombre_variable)
        return False, None
    
    def marcar_como_variable_con_valor(self, variable_conocida):
        variable_valida, objeto_variable = self.get_variable(variable_conocida)
        if variable_valida and type(objeto_variable) is Variable:
            objeto_variable.asignar_valor()
            return True
        else:
            return False  # la variable no existe

    def resetear_variables(self):
        for variable_actual in self.variables.values():
            if type(variable_actual) == Variable:
                variable_actual.resetear_valor()

    def _comprobar_validez_de_parametros_de_funcion(self, n, vi, vo):
        if(type(n) == str and type(vi) == list and type(vo) == list and len(vi) > 0 and len(vo) > 0):
            contenido_str = True
            for elemento in vi:
                if type(elemento) != str:
                    contenido_str = False
            for elemento in vo:
                if type(elemento) != str:
                    contenido_str = False
            return contenido_str
        else:
            return False

    def agregar_variables(self, funcion: Funcion):
        # primero averiguamos cuales son las variables que ya conocemos
        variables_de_grafo = self.consultar_variables()

        # ahora miramos las variables de entrada de la funcion
        for var_fun_in in funcion.variables_in:
            if var_fun_in not in variables_de_grafo:  # si no existe la variable en el grafo la creamos
                self.variables[var_fun_in] = Variable(var_fun_in)
                variables_de_grafo.append(var_fun_in)
            variable_receptora_de_funcion = self.variables.get(var_fun_in)  # apuntando a NODO variable
            if type(variable_receptora_de_funcion) is Variable:
                if funcion.nombre not in variable_receptora_de_funcion.consultar_funciones_in():
                    variable_receptora_de_funcion.funciones_in.append(funcion)

        # ahora miramos las variables de salida de la funcion
        for var_fun_out in funcion.variables_out:
            if var_fun_out not in variables_de_grafo:  # si no existe la variable en el grafo la creamos
                self.variables[var_fun_out] = Variable(var_fun_out)
                variables_de_grafo.append(var_fun_out)
            variable_receptora_de_funcion = self.variables.get(var_fun_out)  # apuntando a NODO variable
            if type(variable_receptora_de_funcion) is Variable:
                if funcion.nombre not in variable_receptora_de_funcion.consultar_funciones_out():
                    variable_receptora_de_funcion.funciones_out.append(funcion)

    def agregar_funcion(self, nombre_funcion: str, variables_entrantes: list, variables_salientes: list):
        if(self._comprobar_validez_de_parametros_de_funcion(nombre_funcion, variables_entrantes, variables_salientes)):
            # creamos objeto de clase FUNCION con los datos disponibles...
            funcion = Funcion(nombre_funcion, variables_entrantes, variables_salientes)
            # incorporamos el objeto a nuestra lista de FUNCIONes
            self.funciones[funcion.nombre] = funcion
            # agregamos las variables a nuestro grafo
            self.agregar_variables(funcion)
        else:
            print(f'\n...ERROR... Se ha tratado de introducir una función incorrecta: {str(nombre_funcion)}')
            exit(0)

    def consultar_variables_con_valor_conocido(self):
        conocidos = []
        for nombre_variable, variable_actual in self.variables.items():
            if type(variable_actual) is Variable:
                if variable_actual.tenemos_datos():
                    conocidos.append(nombre_variable)
        return conocidos

    def consultar_funciones_ejecutables(self):
        variables_conocidas = self.consultar_variables_con_valor_conocido()
        funciones_ejecutables = []
        for nombre_funcion, funcion_actual in self.funciones.items():
            if type(funcion_actual) is Funcion:
                se_puede_ejecutar, lista_variables_que_faltan = funcion_actual.es_ejecutable(variables_conocidas)
                if se_puede_ejecutar:
                    # tenemos una funcion que puede ejecutarse porque tenemos datos de entrada disponibles
                    aporta_datos_nuevos = False
                    for variable_salida_funcion in funcion_actual.variables_out:
                        if variable_salida_funcion not in variables_conocidas:
                            # esta funcion es ejecutable y nos aporta informacion nueva
                            aporta_datos_nuevos = True
                    if aporta_datos_nuevos:
                        funciones_ejecutables.append(nombre_funcion)  # la funcion es ejecutable
                else:
                    pass  # la funcion no es ejecutable porque le faltan las variables de entrada LISTA
        return funciones_ejecutables
