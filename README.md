# Escaleras

## Aprendizaje

La idea es que el agente aprenda a llegar al objetivo atravesando distintos obtáculos. Notar que la vista del mundo es de "costado", como si fuera un juego de plataforma.

El aprendizaje está dividido en:

- Aprender a subir una escalera (jump_slab)
- Llegar a un objetivo para el cual hay que dejarse caer (falling)

El código que permite esto se encuentra en el archivo `Learning.py`

## Mapas

Los mapas están guardados en `test_maps` y `learning_maps`, cada carpeta contiene los mapas de test y aprendizaje
necesarios para que el agente aprenda a subir una escalera y a dejarse caer.

El formato de los archivos es:

- **0**: Celda vacía
- **1**: Posición de incio del agente
- **2**: Objetivo del agente
- **3**: Obstáculo

