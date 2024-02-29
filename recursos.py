class Recursos_Circulos:

    # relaciones entrada->salida con las funciones que llamarian para resolver
    posibilidades = {
                        'calcCircunf_Diametro': [['diametro'], ['circunferencia']],
                        'calcRadio_Diametro': [['diametro'], ['radio']],
                        'calcDiametro_Radio': [['radio'], ['diametro']],
                        'calcArea_Radio': [['radio'], ['area']]
                    }

    # variables constantes comunes dentro de la ejecucion
    pi = 3.1415926588

    @classmethod
    def calcCircunf_Diametro(cls, parametros: dict):
        valor_diametro = parametros.get('diametro')
        parametros['circunferencia'] = valor_diametro*cls.pi
    
    @staticmethod
    def calcRadio_Diametro(parametros: dict):
        valor_diametro = parametros.get('diametro')
        parametros['radio'] = valor_diametro/2.0

    @staticmethod
    def calcDiametro_Radio(parametros: dict):
        valor_radio = parametros.get('radio')
        parametros['diametro'] = valor_radio*2.0
    
    @classmethod
    def calcArea_Radio(cls, parametros: dict):
        valor_radio = parametros.get('radio')
        parametros['area'] = cls.pi*valor_radio*valor_radio

class Recursos_Cilindros:

    # relaciones entrada->salida con las funciones que llamarian para resolver
    posibilidades = {
                        'calcVolumen_AreaAlt': [['area', 'altura'], ['volumen']],
                        'calcAltura_AreaVolumen': [['area', 'volumen'], ['altura']],
                        'calcArea_AlturaVolumen': [['altura', 'volumen'], ['area']]
                    }

    @staticmethod
    def calcVolumen_AreaAlt(parametros: dict):
        area = parametros.get('area')
        altura = parametros.get('altura')
        parametros['volumen'] = area*altura

    @staticmethod
    def calcAltura_AreaVolumen(parametros: dict):
        area = parametros.get('area')
        volumen = parametros.get('volumen')
        parametros['altura'] = volumen/area

    @staticmethod
    def calcArea_AlturaVolumen(parametros: dict):
        altura = parametros.get('altura')
        volumen = parametros.get('volumen')
        parametros['area'] = volumen/altura
