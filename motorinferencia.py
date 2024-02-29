from enum import Enum
from investigador import Investigador
from recursos import *


class MotorInferencia:

    class EstadoMotorInferencia(Enum):
        SIN_DEFINIR = 0
        APRENDIZAJE_HECHO = 1
        PROBLEMA_APRENDIENDO = 2

    def __init__(self, keyword='Recursos_'):
        self.clave_clase = keyword
        self.investigador = Investigador()
        self.estado = self.EstadoMotorInferencia.SIN_DEFINIR

    def resetear(self):
        self.investigador.resetear()
        self.estado = self.EstadoMotorInferencia.SIN_DEFINIR

    def absorver_conocimiento_disponible(self, reseteando=True, mostrar=True):
        if reseteando:
            self.resetear()
        mapa_de_recursos = self._mapear_recursos(self.clave_clase)
        if mapa_de_recursos is None:
            self.estado = self.EstadoMotorInferencia.PROBLEMA_APRENDIENDO
            if mostrar:
                print('\n- - -  WARNING: conocimiento incoherente\n')
        else:
            self.estado = self.EstadoMotorInferencia.APRENDIZAJE_HECHO
            self._agregar_mapa_a_investigador(mapa_de_recursos)
            if mostrar:
                print('\n+ + +  conocimiento absorvido\n')

    @staticmethod
    def _mapear_recursos(keyword):
        """
        lee las clases llamadas "KEYWORD"+"ALGO" y de la información recogida crea
        un diccionario tal que:
        {   'KEYWORDalgo":  {   'constante1': valor
                                'posibilidades': {  'funcion1': [['var_in'],['var_out']] } } }
        """
        elsuperdict = {}
        for nombre, valor in globals().items():
            if isinstance(valor, type) and nombre.startswith(keyword):
                atributos_info = {}
                for atr in dir(valor):
                    if not str(atr).startswith('__'): # 
                        if callable(getattr(valor, atr)):
                            pass  # funcion nombre ATR=atr con contenido VALOR=getattr(valor, atr)
                        elif isinstance(getattr(valor, atr), list):
                            atributos_info[atr] = getattr(valor, atr)
                        elif isinstance(getattr(valor, atr), dict):
                            atributos_info[atr] = getattr(valor, atr)
                        else:
                            atributos_info[atr] = getattr(valor, atr)
                elsuperdict[nombre] = atributos_info  # almacenado TEMA/RECURSO
        error = False
        for nombre_tema, recursos_tema in elsuperdict.items():
            lista_recursos = list(recursos_tema.keys())
            if 'posibilidades' in lista_recursos:
                contenido_de_posibilidades = recursos_tema.get('posibilidades')
                for nombre_fun, listas_variables in contenido_de_posibilidades.items():
                    if type(nombre_fun) is str and type(listas_variables) is list:
                        pass  # de momento estamos ante {'tema': {'posibilidades': {'funcion': [lista_cosas]}}}
                    else:
                        error = True
            else:
                error = True
        if error:
            print(f'Se ha dado un ERROR asimilando recurso {nombre_tema}')
            return None
        else:
            return elsuperdict

    def mostrar_recursos(self):
        print('- Mostrando el Mapa de Recursos')
        print(self.investigador.conocimiento)

    def _agregar_mapa_a_investigador(self, mapa_de_recursos: dict):
        """
        lee un diccionario tal que:
        un diccionario tal que:
        {   'KEYWORDalgo":  {   'constante1': valor
                                'posibilidades': {  'funcion1': [['var_in'],['var_out']] } } }
        """
        for nombre_recurso, dic_recurso in mapa_de_recursos.items():
            for constante in list(dic_recurso.keys()):
                if constante == 'posibilidades':  # ignora los valores de constantes
                    dic_funciones = dic_recurso.get(constante)
                    for nombre_funcion in list(dic_funciones.keys()):
                        # nombre_funcion = valores_in, valores_out
                        variables = dic_funciones.get(nombre_funcion)
                        self.investigador.agregar_funcion(f'{nombre_recurso}.{nombre_funcion}',
                                                          variables[0],
                                                          variables[1])
    
    def explotar(self, lista_de_variables_conocidas: dict, mostrar=True):
        return self.investigador.explotar(lista_de_variables_conocidas, mostrar)  # planificamos los pasos a calcular

    def averiguar(self, lista_de_variables_conocidas: dict, lista_variables_deseadas: list, mostrar=True):
        return self.investigador.averiguar(lista_de_variables_conocidas, lista_variables_deseadas, mostrar)

    def ejecutar_los_pasos(self, pasos_planificados: list, diccionario_de_variables_conocidas: dict, mostrar=True):
        diccionario_de_variables_completado = {}
        diccionario_de_variables_completado.update(diccionario_de_variables_conocidas)  # pendiente de mejorar para que funcione con deepcopy
        cantidad_pasos_planificados = len(pasos_planificados)
        if cantidad_pasos_planificados > 0:
            if mostrar:
                print(f'\nVamos a dar {cantidad_pasos_planificados} pasos')
            for paso, orden in zip(pasos_planificados, list(range(cantidad_pasos_planificados))):  # recorremos los pasos planificados
                nombre_de_funcion = list(paso.keys())[0]  # extraemos el nombre de la funcion
                variables_conocidas = [x for x in list(diccionario_de_variables_completado.keys())]
                datos_funcion = paso.get(nombre_de_funcion)
                var_in = datos_funcion.get('v_entrada')
                var_out = datos_funcion.get('v_salida')
                var_new = datos_funcion.get('v_aportadas')

                if mostrar:
                    print(f'\nPaso {orden+1}: en este momento conocemos:')
                    for variable_conocida in variables_conocidas:
                        print(f'    {variable_conocida} = {diccionario_de_variables_completado.get(variable_conocida)}')
                    print(f'        con la funcion <{nombre_de_funcion}>({", ".join(var_in)})')

                partes = str(nombre_de_funcion).split('.')
                clase_que_contiene_la_funcion = globals()[partes[0]]
                funcion = getattr(clase_que_contiene_la_funcion, partes[1])
                for variable_salida in var_out:
                    if variable_salida not in list(diccionario_de_variables_completado.keys()):
                        diccionario_de_variables_completado[variable_salida] = 'prometida'
                # pendiente aqui hacer dos filtros:
                # - uno: para q solo llegue accesible a la funcion exclusivamente las variables que le tocan
                funcion(diccionario_de_variables_completado)
                # - dos: para que se recoja lo recibido; y la funcion no pueda escribir variables que no debiese

                if mostrar:
                    for variable_aportada in var_new:
                        print(f'            -> {variable_aportada} = {diccionario_de_variables_completado.get(variable_aportada)}')
        else:
            if mostrar:
                print(f'\nCon el conocimiento actual no podemos esclarecer nada...')


if __name__ == '__main__':
    import os
    os.system("cls")

    motor = MotorInferencia()  # creamos el objeto principal, el cerebro vacío
    motor.absorver_conocimiento_disponible(mostrar=True)  # enriquecemos el cerebro
    motor.mostrar_recursos()  # pedimos al cerebro que muestre lo aprendido

    diccionario_de_variables_conocidas = {"altura": 3, "volumen": 150, "diametro": 3}
    lista_variables_conocidas = list(diccionario_de_variables_conocidas.keys())

    # proponemos un problema real: tenemos variables conocidas y que mine datos
    pasos = motor.explotar(lista_variables_conocidas, mostrar=True)
    motor.ejecutar_los_pasos(pasos, diccionario_de_variables_conocidas)

    # proponemos un problema real: tenemos variables conocidas y
    # haga lo minimo posible para llegar a las variables deseadas
    lista_variables_deseadas = ['area']
    pasos = motor.averiguar(lista_variables_conocidas, lista_variables_deseadas, mostrar=True)
    motor.ejecutar_los_pasos(pasos, diccionario_de_variables_conocidas)

    print("")
