from grafo import Grafo
from funcion import Funcion
import gc


class Investigador:

    def __init__(self):
        self.conocimiento = Grafo()
    
    def resetear(self):
        self.conocimiento = None  # elimina la referencia
        gc.collect()  # recolecta la basura para eliminar la memoria ram
        self.conocimiento = Grafo()  # crea un nuevo objeto limpio

    def agregar_funcion(self, nombre, lista_variables_entrada, lista_variables_salida):
        self.conocimiento.agregar_funcion(nombre, lista_variables_entrada, lista_variables_salida)
        # aumenta conocimiento (variables y funciones)
    
    def __str__(self):
        return str(self.conocimiento)

    def averiguar(self, lista_variables_conocidas: list, lista_variables_deseadas: list, mostrar=False):
        """
            = Pendiente de Hacer / ToDo =
            =============================
            Dado un conocimiento, y tiempo limitado,
            buscar caminos dirigidos a lo deseado
            ignorando resto que nos son irrelevantes;
            esta parte del programa va a ser todo un
            dolor, pero la verdadera magia...
        """
        recorridos = []
        if mostrar:
            print('\n' + f'Averiguando: [{", ".join(lista_variables_deseadas)}]')
            print(f'Partiendo desde: [{", ".join(lista_variables_conocidas)}]')
            print('\t++++ PROXIMAMENTE (pendiente de implementar, ya tengo ideas) ++++')
        return recorridos

    def explotar(self, lista_variables_conocidas: list, mostrar=False):
        self.conocimiento.resetear_variables()  # ponemos los valores de variables = EstadoVariable.SIN_DATOS
        for variable_conocida in lista_variables_conocidas:
            fue_bien = self.conocimiento.marcar_como_variable_con_valor(variable_conocida)  # estos valores serán = EstadoVariable.CON_DATOS
            if not fue_bien:
                print('\n' + f'--- Ha fallado el programa al intentar marcar una variable que no existe: {variable_conocida}')
                exit(0)
        coleccion_de_pasos = []  # aqui listaremos los diccionarios {'Funcion': 'ejecutada', 'Encontrados': [listavaloresnuevosencontrados]}
        variables_actualmente_conocidas = self.conocimiento.consultar_variables_con_valor_conocido()
        while True:
            lista_funciones_ejecutables_actualmente = self.conocimiento.consultar_funciones_ejecutables() 
            # lista de funciones disponibles que revelan datos encontrables aun ocultos
            if len(lista_funciones_ejecutables_actualmente) == 0:
                # ya no podemos sacar nada más
                break
            else:
                self._aplicar_funciones(coleccion_de_pasos, variables_actualmente_conocidas, lista_funciones_ejecutables_actualmente)
        if mostrar:
            print('\n' + f'Explotando conocimiento disponible desde: [{", ".join(lista_variables_conocidas)}]')
            mis_pasos = len(coleccion_de_pasos)
            for paso, orden in zip(coleccion_de_pasos, list(range(mis_pasos))):
                funcion = list(paso.keys())[0]
                info_de_funcion = paso.get(funcion)
                # {'v_entrada': funcion_actual.variables_in, 'v_salida': funcion_actual.variables_out, 'v_aportadas': variables_aportadas}
                variables_esclarecidas = info_de_funcion.get('v_aportadas')
                print(f'  Paso {orden+1}: <{funcion}> esclarecemos: [{", ".join(variables_esclarecidas)}]')
            if mis_pasos == 0:
                print('  <> ... con mi conocimiento actual no puedo hacer nada ... <>')
        return coleccion_de_pasos

    def _aplicar_funciones(self, coleccion_de_pasos: list, variables_actualmente_conocidas: list, lista_funciones_ejecutables_actualmente: list):
        for funcion in lista_funciones_ejecutables_actualmente:
            funcion_actual = self.conocimiento.funciones.get(funcion)
            variables_aportadas = []
            if type(funcion_actual) is Funcion:
                variables_salida = funcion_actual.variables_out
                for variable in variables_salida:
                    if variable not in variables_actualmente_conocidas:
                        variables_aportadas.append(variable)
                        self.conocimiento.marcar_como_variable_con_valor(variable)  # activamos los valores que vamos encontrando
                coleccion_de_pasos.append({funcion: {'v_entrada': funcion_actual.variables_in,
                                                     'v_salida': funcion_actual.variables_out,
                                                     'v_aportadas': variables_aportadas}})
                variables_actualmente_conocidas += variables_aportadas


if __name__ == '__main__':

    import os
    os.system("cls")
    patxi = Investigador()

    # alimentando funciones conocidas que relacionan variables...
    patxi.agregar_funcion('calcCircunf_Diametro', ['diametro'], ['circunferencia'])
    patxi.agregar_funcion('calcRadio_Diametro', ['diametro'], ['radio'])
    patxi.agregar_funcion('calcDiametro_Radio', ['radio'], ['diametro'])
    patxi.agregar_funcion('calcArea_Radio', ['radio'], ['area'])

    print(patxi)  # muestra el contenido del grafo

    print('')
    patxi.explotar(['radio'], mostrar=True)
    # comprueba todo lo conseguible con las funciones conocidas
    # la funcion EXPLOTAR devuelve una lista de pasos tal que:
    # [{'Funcion': 'ejecutada', 'Encontrados': [listavaloresnuevosencontrados]},...
    # ..., {'Funcion': 'ejecutada', 'Encontrados': [listavaloresnuevosencontrados]}]

    print('')
    patxi.averiguar(['radio'], ['circunferencia'], mostrar=True)
    # comprueba con las funciones conocidas, cómo llegar de variables desconocidas a deseadas
    # con el menor número de pasos posible...
    # [{'Funcion': 'ejecutada', 'Encontrados': [listavaloresnuevosencontrados]},...
    # ..., {'Funcion': 'ejecutada', 'Encontrados': [listavaloresnuevosencontrados]}]
    print('')
