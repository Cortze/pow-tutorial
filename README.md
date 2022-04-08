# Ejemplo de Proof of Work

## Introducción
En este tutorial, intentaremos simular de una manera muy sencilla el concepto de Proof of Work que se utiliza en la red de Bitcoin para generar consenso sobre cuál es el nuevo bloque que va a ser añadido a la cadena. 

Conoceremos los conceptos básicos de las funciones Hash, base fundamental para mantener los datos guardados en los bloques inmutables. 
Tambien analizaremos el algoritmno que se usa para ver cuando un bloque está listo para ser añadido a la cadena o para validar que el que el bloque que se quiere añadir cumple todos los requisitos.

Para ello, proponemos una pequeña demo en la que los estudiantes tendrán que completar las partes de código que faltan para completar el algoritmo de Proof of Work propuesto.

## Ejercicios propuestos 1 ( obligatorios )

Los estudiantes tendrán que rellenar los componentes que faltan del fichero `minero.py` para generar el algoritmo de proof of work sobre un bloque dado. 

Este algoritmo deberá comprobar que la versión serializada del bloque (`block.get_json()`) tenga un resultado de la función hash `sha256()` con la misma cantidad de ceros por la izquierda que la definida en la dificultad del problema. Para ello, el estudiante deberá incrementar el campo `nonce` del objeto `Block` hasta que se cumpla esa condición.

La manera de ejecutar el fichero `minero.py` es la siguiente:
1. En la terminal, dentro de la carpeta que contiene el fichero, se ha de ejecutar el siguiente comando:
`python3 hasher.py --input=YYYYYY.json --dificulty=X`
Donde `YYYYY.json`define el fichero bloque que se quiere minar. (La estructura base del bloque se proporciona en el fichero `bloque_base.json`) 
Y donde `X` es la dificultad que le queremos dar al algoritmo de minado. (Numero entero entre 1 y 10)


#### Lista de funciones a completar

1. calculate_valid_block()
2. increase_nonce()
3. get_hash()

## Ejercicios propuestos 2 ( opcionales )