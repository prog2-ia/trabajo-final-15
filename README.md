[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/09uckVan)
# Sistema de Gestión Logística

## Instalación


git clone <repo>
cd trabajo-final-15

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

## Prueba y ejecución
En la actualidad estamos generando programas de prueba antes de generar el menu de ejecución principal
Se pueden ejecutar desde la carpeta **test** los programas utilizados para probar el funcionamento de funciones y clases.


## Descripción

Este proyecto implementa un sistema de gestión logística desarrollado en **Python** utilizando **Programación Orientada a Objetos (POO)**.  
El sistema permite modelar un entorno logístico en el que se gestionan pedidos, rutas y flotas de vehículos que transportan mercancías entre diferentes ciudades.

La aplicación permite:

- gestionar pedidos con restricciones
- agrupar pedidos en rutas
- calcular distancias entre ciudades
- estimar costes logísticos
- generar albaranes de transporte
- simular el funcionamiento de una flota de transporte

El proyecto está diseñado de forma modular para facilitar su ampliación futura.

---

# Arquitectura del proyecto

El proyecto se organiza en diferentes módulos: 
```text
├──logistica/  
│    ├── clases/  
│    │     ├──── pedido.py  
│    │     ├──── ruta.py 
│    │     ├──── clientes.py
│    │     ├──── vehiculo.py  
│    │     ├──── flota.py  
│    │     ├──── camion.py  # Clase derivada de vehiculo
│    │     ├──── furgoneta.py  # Clase derivada de vehiculo
│    │     └──── moto.py  # Clase derivada de vehiculo
│    │
│    ├── datos/
│    │     ├── ruta.html
│    │     └── ciudades_alicante.py   # Diccionario de ciudades y coordenadas
│    │  
│    ├── exceptions/  
│    │     └── errores.py  
│    │  
│    ├── tests/  
│    │     ├── test_01_crear_pedido.py
│    │     ├── test_09_calcular_km_rutas.py
│    │     └── ...            # Otros tests
│    │    
│    ├── utiles/  
│    │    └── util.py 
│    │ 
│    ├── Diagrama UML
│    ├── diagrama uml.png
│    ├── Estructura
│    ├── Proyecto ejemplo
│    └── requirements.txt
├── .gitignore
└── README.md 

 
```
---

# Modelo del sistema

El sistema se basa en las siguientes entidades principales:

- **Pedido**
- **Ruta**
- **Vehículo**
- **Flota**

---

# Clase Pedido

La clase `Pedido` representa un envío logístico entre dos ciudades.

## Atributos  
Cada pedido contiene información sobre:

- identificador
- origen
- destino
- peso
- volumen
- fecha de entrega
- nivel de servicio
- validacion
- coordenadas x e y para visualizacion de ruta
- coordenadas de latitud y longitud de origen
- coordenadas de latitud y longutud de destino
- km entre origen y destino


## Funcionalidades

- Validación de datos
- obtencion de coordenadas geograficas de origen y destino
- calculo de distancia entre origen y destino
- Agrupación de pedidos mediante sobrecarga del operador `+`
- Representación en texto

Ejemplo de salida:

**Pedido:P0 Alicante → Torrevieja 44.5 km Peso:42.28 kg Vol:0.14 l. Entrega:2026-03-25 Hora:23:06 Servicio:urgente**


---
# Clase Ruta

La clase `Ruta` contiene una lista de pedidos y representa un recorrido de un vehiculo distribuyendo pedidos  

Cada ruta contiene información de :
- Identificador de la ruta 
- Distancia total estimada de la ruta
- Lista de pedidos

## Funcionalidades
- Añadir pedido a ruta 
- Eliminar pedido de ruta
- calcular nº de pedidos de ruta
- Calcular el peso de todos los pedidos
- Calcular el volumen de todos los pedidos
- Calcular el recorrido total de toda la ruta
- Calcular el coste de la ruta
- Devuelve la lista de pedidos de la ruta
- Devuelve un albaran de la ruta
- Devuelve una cadena con el recorrido de la ruta
- Compara el coste de dos rutas diferentes mediante el oparador de sobrecarga __lt__
- Calcula el numero de pedidos de la ruta mediante el operado de sobrecarga __len__
- Imprime la informacion de la ruta mediante la sobrecarga __str__
    

# Clase Vehiculo (planificada)

La clase `Vehiculo` representará un vehículo de transporte dentro de la flota.

Esta clase actuará como **clase base** para distintos tipos de vehículos.

## Atributos previstos

- matrícula
- capacidad de peso
- capacidad de volumen
- lista de pedidos asignados
- ruta asignada

## Funcionalidades previstas

- comprobar si puede transportar un pedido
- cargar pedidos
- calcular ocupación del vehículo
- asignar rutas

---

# Subclases de Vehiculo

El sistema incluirá diferentes tipos de vehículos especializados.

## Camion

Vehículo de gran capacidad utilizado para transporte interurbano.

Capacidad aproximada:

- peso máximo elevado
- gran volumen de carga

Uso principal:

- rutas largas
- transporte de grandes pedidos

---

## Furgoneta

Vehículo de capacidad media utilizado para reparto regional.

Capacidad aproximada:

- peso medio
- volumen medio

Uso principal:

- rutas de reparto urbano o regional

---

## Moto

Vehículo ligero para transporte rápido.

Capacidad aproximada:

- peso bajo
- volumen reducido

Uso principal:

- entregas urgentes
- reparto en ciudad

---

# Clase Flota

La clase `Flota` representa el conjunto de vehículos disponibles.

Esta clase permitirá gestionar los recursos logísticos del sistema.

## Funcionalidades previstas

- añadir vehículos
- eliminar vehículos
- asignar rutas a vehículos
- calcular ocupación de la flota
- balancear carga entre vehículos

---

# Relaciones entre clases

El sistema presenta las siguientes relaciones:

Flota  
│  
├── Vehiculo  
│ ├── Camion  
│ ├── Furgoneta  
│ └── Moto  
│  
Ruta  
│  Pedido  


## Relaciones principales

- **Una ruta contiene múltiples pedidos**
- **Un vehículo transporta una ruta**
- **Una flota contiene múltiples vehículos**

---

# Diagrama UML conceptual
            Flota
              │
              │ contiene
              │
           Vehiculo
           /  |   \
          /   |    \
     Camion Furgoneta Moto
           |
           | transporta
           |
           Ruta
           |
           | agrupa
           |
          Pedido


---

# Cálculo de distancias

El sistema calcula la distancia entre ciudades utilizando la librería: geophy



Esto permite obtener distancias geográficas reales entre las ciudades de origen y destino.

Las ciudades incluidas actualmente son:

- Alicante
- Valencia
- Madrid
- Barcelona
- Murcia
- Sevilla
- Bilbao
- Zaragoza

La distancia de la ruta se calcula sumando las distancias entre los destinos de los pedidos.

---

# Generación de albaranes

Cada ruta puede generar un albarán logístico con la siguiente información:

- pedidos incluidos
- peso total transportado
- volumen total
- distancia total
- coste estimado

Ejemplo de albarán:  

ALBARÁN RUTA R1  
Pedido:P1 Alicante → Valencia Peso:5 kg   
Pedido:P2 Valencia → Madrid Peso:8 kg  

Total pedidos: 2  
Peso total: 13 kg  
Volumen total: 3  
Distancia: 420 km  
Coste estimado: 630 €  


---

# Instalación

Instalar dependencias. Desde terminal: **pip install geopy**


---

# Ejecutar pruebas
python tests/test_pedido_ruta.py


---

# Tecnologías

- Python 3
- Programación Orientada a Objetos
- geopy
- Git

---

# Posibles mejoras

- optimización automática de rutas
- asignación automática de vehículos
- visualización de rutas en mapas
- simulación de flotas
- interfaz gráfica

---

# Autores

Manuel Quiles Gómez  
Anton Koniaev


