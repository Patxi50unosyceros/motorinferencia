# Motor de Inferencia

### _Enfoque_

Este proyecto trata de facilitar la tarea de resolver *problemas complejos* entendiendo el conocimiento dispuesto en **RECURSOS** como la comprensión de un mapa de **variables** las cuales se conectan entre sí a través de **funciones**. En un futuro se podrán crear incluso análisis... pero de momento, se busca resolver tareas partiendo de unas *variables iniciales* y desde ahí llegar a conocer el valor de *variables objetivo*.

### _Uso_

Los objetos disponibles de clase **MOTORINFERENCIA** disponen de los siguientes métodos:

- .absorver_conocimiento_disponible: construye el grafo a partir de las clases contenidas en RECURSOS
- .mostrar_recursos: muestra el contenido del grafo (la colección de variables, y tras cada variable: las funciones en cuya salida está esta variable, y después, las funciones en las que esta variable es parte de la entrada)
- .explotar: calcula la lista de pasos posibles para averiguar el valor de todas variables desconocidas posibles usando las funciones disponibles y las variables que se conocen inicialmente.
- averiguar: [pendiente de implementar] calcula la lista de pasos posibles para averiguar el valor de un conjunto de variables desconocidas (no todas las posibles) usando las funciones disponibles y las variables que se conocen inicialmente.
- ejecutar_los_pasos: aplica una lista de pasos sobre un conjunto de variables.

> Se pueden ver demostracicones/ejemplos en el codigo de *INVESTIGADOR* y en *MOTORINFERENCIA*

### _Futuras Funcinalidades_
--> Para poder gestionar conocimiento complejo con miles de funciones y variables se buscará optimizar el código para:

- no dar pasos innecesarios/ineficientes
- en caso de encontrar un bloqueo por fallo de una función, ser capaz de buscar un camino alternativo para sortear el obstáculo
- en caso de que se interrumpa la ejecución, poder reanuadarla
- construir una caché que permita agilizar el uso del grafo
- poder hacer análisis inductivos y deductivos
- en base a experiencia y posibles mejoras, poder elegir si hacer el camino con menos tiempo, o con menos pasos
- que el sistema sea capaz de aprender por experiencia qué caminos suelen ser más largos o más cortos
- ... estoy abierto a sugerencias ...


## Ejemplo de lo que muestra actualmente INVESTIGADOR:

``` python
Contenido del Grafo de Variables
  Variable <diametro>
    F calcDiametro_Radio (radio) = diametro
    f calcCircunf_Diametro (diametro) = circunferencia
    f calcRadio_Diametro (diametro) = radio
  Variable <circunferencia>
    F calcCircunf_Diametro (diametro) = circunferencia
  Variable <radio>
    F calcRadio_Diametro (diametro) = radio
    f calcDiametro_Radio (radio) = diametro
    f calcArea_Radio (radio) = area
  Variable <area>
    F calcArea_Radio (radio) = area

Explotando conocimiento disponible desde: [radio]
  Paso 1: <calcDiametro_Radio> esclarecemos: [diametro]
  Paso 2: <calcArea_Radio> esclarecemos: [area]
  Paso 3: <calcCircunf_Diametro> esclarecemos: [circunferencia]

Averiguando: [circunferencia]
Partiendo desde: [radio]
        ++++ PROXIMAMENTE (pendiente de implementar, ya tengo ideas) ++++
```


## Ejemplo de lo que muestra actualmente MOTORINFERENCIA:

``` python
+ + +  conocimiento absorvido

- Mostrando el Mapa de Recursos
Contenido del Grafo de Variables
  Variable <diametro>
    F Recursos_Circulos.calcDiametro_Radio (radio) = diametro
    f Recursos_Circulos.calcCircunf_Diametro (diametro) = circunferencia
    f Recursos_Circulos.calcRadio_Diametro (diametro) = radio
  Variable <circunferencia>
    F Recursos_Circulos.calcCircunf_Diametro (diametro) = circunferencia
  Variable <radio>
    F Recursos_Circulos.calcRadio_Diametro (diametro) = radio
    f Recursos_Circulos.calcDiametro_Radio (radio) = diametro
    f Recursos_Circulos.calcArea_Radio (radio) = area
  Variable <area>
    F Recursos_Circulos.calcArea_Radio (radio) = area
    F Recursos_Cilindros.calcArea_AlturaVolumen (altura, volumen) = area
    f Recursos_Cilindros.calcVolumen_AreaAlt (area, altura) = volumen
    f Recursos_Cilindros.calcAltura_AreaVolumen (area, volumen) = altura
  Variable <altura>
    F Recursos_Cilindros.calcAltura_AreaVolumen (area, volumen) = altura
    f Recursos_Cilindros.calcVolumen_AreaAlt (area, altura) = volumen
    f Recursos_Cilindros.calcArea_AlturaVolumen (altura, volumen) = area
  Variable <volumen>
    F Recursos_Cilindros.calcVolumen_AreaAlt (area, altura) = volumen
    f Recursos_Cilindros.calcAltura_AreaVolumen (area, volumen) = altura
    f Recursos_Cilindros.calcArea_AlturaVolumen (altura, volumen) = area

Explotando conocimiento disponible desde: [altura, volumen, diametro]
  Paso 1: <Recursos_Circulos.calcCircunf_Diametro> esclarecemos: [circunferencia]
  Paso 2: <Recursos_Circulos.calcRadio_Diametro> esclarecemos: [radio]
  Paso 3: <Recursos_Cilindros.calcArea_AlturaVolumen> esclarecemos: [area]

Vamos a dar 3 pasos

Paso 1: en este momento conocemos:
    altura = 3
    volumen = 150
    diametro = 3
        con la funcion <Recursos_Circulos.calcCircunf_Diametro>(diametro)
            -> circunferencia = 9.4247779764

Paso 2: en este momento conocemos:
    altura = 3
    volumen = 150
    diametro = 3
    circunferencia = 9.4247779764
        con la funcion <Recursos_Circulos.calcRadio_Diametro>(diametro)
            -> radio = 1.5

Paso 3: en este momento conocemos:
    altura = 3
    volumen = 150
    diametro = 3
    circunferencia = 9.4247779764
    radio = 1.5
        con la funcion <Recursos_Cilindros.calcArea_AlturaVolumen>(altura, volumen)
            -> area = 50.0

Averiguando: [area]
Partiendo desde: [altura, volumen, diametro]
        ++++ PROXIMAMENTE (pendiente de implementar, ya tengo ideas) ++++

Con el conocimiento actual no podemos esclarecer nada...
```

## _Mis Reflexiones_

> Este proyecto fue producto del intento de ayudar a un amigo que quiere construir un gran proyecto que pueda automatizar una colección de tareas muy complejas con cientos de funcionalidades interdependientes, donde todo se resuelve en base a reglas y experiencia. ¿Dónde llegaremos?
