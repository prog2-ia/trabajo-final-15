# 🚚 Sistema de Gestión Logística en Python

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-green)
![Licencia](https://img.shields.io/badge/Licencia-Uso%20educativo-lightgrey)

---

## 📌 Descripción

Sistema de gestión logística desarrollado en Python que permite:
- Gestión de clientes
- Gestión de delegaciones
- Gestión de vehículos asignados a delegaciones
- Gestión de pedidos de clientes
- Gestión de rutas 

Para el cálculo de las rutas, se utilizán librerias externas para calcular geolocalizaciones exactas y calcular distancias entre origen y destino de pedios. Estas librerías externas permiten:
- Geolocalización de direcciones reales
- Visualización en mapas interactivos

El proyecto está diseñado siguiendo principios de **Programación Orientada a Objetos (POO)**, con persistencia de datos en formatos TXT y JSON. Arquitectura modular desacoplada.

---
# 📌 Objetivo de la aplicación

La aplicación simula la gestión logística completa de una empresa de transportes encargada de:

- Recoger mercancías desde clientes origen.
- Transportarlas entre distintas delegaciones.
- Entregarlas a clientes destino.
- Optimizar rutas y recursos logísticos.

Toda la operativa se basa en direcciones geolocalizadas automáticamente mediante coordenadas GPS.

---

# 🧩 Arquitectura General

```text
┌──────────────────────────────────────────────────────────────┐
│                   APLICACIÓN LOGÍSTICA                       │
└──────────────────────────────────────────────────────────────┘
                │
                ├── Generación de datos de prueba
                │
                ├── Mantenimiento de ficheros
                │
                └── Gestión de rutas
```

---

# 📦 Módulos principales

# 1️⃣ Generación de datos de prueba

## 🎯 Objetivo

Dada la gran cantidad de datos necesarios para manejar la aplicación y realizar un testing fiable, se incluyen programas que generán de forma aleatorio los datos de los archivos maestros. 
## 📂 Datos generados

- Delegaciones. 
- Clientes
- Vehículos
- Pedidos

## ⚙️ Funcionalidades

- Generación aleatoria de clientes.
- Creación de delegaciones jerárquicas.
- Generación automática de pedidos.
- Generación de vehículos compatibles.
- Asignación geográfica automática.
- Persistencia en ficheros JSON/TXT.

---

# 2️⃣ Mantenimiento de ficheros

## 🎯 Objetivo

Gestionar manualmente toda la información del sistema.

## 📁 Entidades gestionadas

### 🏢 Delegaciones
- Nombre de la delegación
- Dirección
- Población
- Tipo de delegación (Despacho, Base o Central)
- Delegación superior de la que depende
- Coordenadas geográficas (Latitud, Longitud)


### 👤 Clientes

- DNI
- Nombre
- Apellidos
- Dirección
- Coordenadas geográficas
- Despacho mas cercano
- Distancia hasta el despacho
- Provincia
- Población
- Pedidos en curso
- Pedidos terminados
- Importe facturado
- Coordenadas


### 🚚 Vehículos

- Tipo de vehículo (Camión, Furgoneta, Motocicleta, Mochila)
- Matrícula
- Disponibilidad
- Delegación asignada
- Peso máximo(kg)
- Volumen máximo(litros)

### 📦 Pedidos

- Nº de pedido
- Cliente origen
- Cliente destino
- Distancia en km.
- Estado (Ubicación del pedido)
- Fecha de generación del pedido
- Fecha de entrega del pedido


---

# 3️⃣ Gestión de rutas

## 🎯 Objetivo

Automatizar el flujo logístico de los pedidos. A partir de unos pedidos generados, se confeccionan las rutas. Existen las siguientes variantes de rutas:

### 📦 Rutas

- Nº de pedido
- Cliente origen
- Cliente destino
- Distancia en km.
- Estado (Ubicación del pedido
- Fecha de generación del pedido
- Fecha de entrega del pedido
- Finalizada (no quedan pedios por recoger o repartir)
- Lista de pedidos asignados, pendientes de recoger o repartir
---


# 🔄 Flujo logístico entre localidades. 
## Cuando el origen y el destino están en la misma localidad.

```text
CLIENTE ORIGEN
      │
      ▼
DESPACHO
      │
      ▼
CLIENTE DESTINO
```

# 🔄 Flujo logístico entre provincias. 
## Cuando el origen y el destino están en la misma provincia

```text
CLIENTE ORIGEN
      │
      ▼
DESPACHO ORIGEN
      │
      ▼
    BASE
      │
      ▼
DESPACHO DESTINO
      │
      ▼
CLIENTE DESTINO
```
# 🔄 Flujo logístico completo
## Cuando el origen y el destino estan en provincias diferentes

```text
CLIENTE ORIGEN
      │
      ▼
DESPACHO ORIGEN
      │
      ▼
BASE ORIGEN
      │
      ▼
CENTRAL MADRID
      │
      ▼
BASE DESTINO
      │
      ▼
DESPACHO DESTINO
      │
      ▼
CLIENTE DESTINO
```

# 🚛 Tipos de rutas. 
- ## Rutas de transporte de despachos (despacho→clientes→despacho)
  - Tipo **recogida**: recoger pedidos de clientes, utilizando la flota del despacho. 
  - Tipo **entrega**: repartir pedidos a clientes, utilizando la flota del despacho

- ## Rutas de transporte de bases (base→despachos→base)
  - Tipo **transporte_recogida_de_despachos**: recoger pedidos de despachos, utilizando la flota de furgonetas de la base
  - Tipo **transporte_envio_a_despachos**, entregar pedidos a despachos, utilizando la flota de furgonetas de la base. 

- ## Rutas de transporte de central (central→bases→central)
  - Tipo **transporte_recogida_de_bases**: recoger pedidos de bases, utilizando la flota de camiones de la central
  - Tipo **transporte_envio_a_bases**, entregar pedidos a bases, utilizando la flota de camiones de la central. 


En la actualidad solo están implementadas las rutas de tipo recogida, entre despacho y clientes.

En las delegaciones de tipo base, después de recibir o antes de enviar pedidos, hay que agrupar o des-agrupar pedidos asignando un numero de pedido de tipo agrupado.

Para generar las Rutas de tipo transporte_recogida_de_bases, antes de generar la ruta hay que realizar una agrupación de pedidos que tengan una misma base destino, equivalente a agrupar los pedidos en un palet.

Para generar las Rutas de tipo transporte_envio_a_despachos, antes de generar la ruta hay que realizar una des-agrupación de pedidos recibidos en la base para repartirlos por los diferentes despachos, equivalente a clasificar los pedidos recibidos en un palet.


# 🧠 Arquitectura del sistema

El sistema se organiza en capas independientes:

### 🔹 Dominio (`clases/`)
Contiene la lógica del negocio:
- delegacion.py
- cliente.py
- vehiculo.py
- pedido.py
- ruta.py

### 🔹 Persistencia (`persistencia/`)
- Lectura y escritura en JSON para delegaciones, clientes y pedidos
- Lectura y escritura en txt para vehículos
- Normalización de datos
- Compatibilidad de formatos
- Cache de geocodificación para evitar bloqueo en libreria externa de geolocalización geopy

### 🔹 Utilidades (`utiles/`)
- Geolocalización.py (geopy). De uso libre. Con restricciones respecto al número de peticiones en el tiempo
  - Geolocalización directa. A partir de dirección, calcula coordenadas
  - Geolocalización inversa. A partir de coordenadas, genera dirección
- utils.py. Funciones auxiliares
  - (folium). Librería para visualización geoespacial de datos. Se utilziza para ubicar en mapa geolocalizaiones y rutas
    - Generación de mapas
  - Cálculo de distancias. A partir de coordenadas origen y destino
  - validación y generación de dnis
  - generación y validación de matrículas
  - búsqueda de directorios raiz
  - 


### 🔹 Aplicación (`programas/`)
- Generación de datos de prueba
  - Delegaciones
  - Clientes
  - Vehículos
  - Pedidos
- Mantenimiento de ficheros
  - Mantenimiento de delegaciones
  - Mantenimiento_clientes
  - Mantenimiento de vehículos
  - Mantenimiento_pedidos
- Gestión de rutas
  - Rutas de despachos
    - Generar rutas (implementado solo con recogidas)
    - Grabación de recogidas
    - Grabación de entregas (sin implementar)
    - Listado de rutas
  - Rutas de bases (sin implementar)
    - Agrupar pedidos a bases
    - Des-agrupar pedidos de bases
    - Generar rutas
    - Grabación de recogidas
    - Grabación de entregas
  - Rutas de central (sin implementar)
    - Generar rutas
    - Grabación de recogidas
    - Grabación de entregas

### 🔹 Interfaz (`menu/`)
- Navegación por consola

### 🔹 Tests (`tests/`)
- Pruebas funcionales

---

## 🧩 Flujo de ejecución

La aplicación está basada en tres módulos principales, Generación de datos de prueba, Mantenimiento de ficheros y Gestión de rutas.

Debe de resolver la gestión logística de una empresa de transportes, en la cual hay que trasladar mercancía desde un cliente en una ubicación geográfica (Definida mediante su dirección y geolocalizada por el programa), hasta otro cliente ubicado en otra localización en cualquier lugar de España.

Dada la gran cantidad de información necesaria para el manejo de la logística, la aplicación tiene una parte que es la generación de datos de prueba, en la cual se generan aleatoriamente los ficheros necesarios para los testing, para que el usuario no tenga que darlos de alta uno a uno con los programas de mantenimiento. El flujo de ejecución debería ser el siguiente:


## 1️⃣ Generación aleatoria de datos de prueba. 
Actualmente yá estan creados todos los archivos de persistencia que necesita la aplicación, por lo que para realiar el testing se puede saltar este paso. Si se quiere empezar desde cero, habría que ejecutar la secuencia de programas de este menu:

  - Generar delegaciones → Generar vehículos → Generar clientes → Generar pedidos


## 2️⃣ Gestionar los datos mediante los programas de mantenimiento. 

- Mediante la opción de Listado se puede filtrar y mostrar el estado actual de los datos
- Mediante la opción de Modificación se puede alterar el contenido de los registros de datos. La aplicación valida y verifica que se mantenga la coherencia de los datos
- Mediante al opción de Altas se dan de alta registros de nuevos datos
- Mediante la opción de Bajas se pueden anular registros de datos existentes.


## 3️⃣ Generación de rutas de transporte.
Mediante esté menu se gestiona la creación de rutas envio y recepcion de pedidos. Está divido en Gestion de rutas de Despachos, Bases y Central. Dada la complejidad de la aplicación tan solo se ha implementado hasta ahora la gestion de rutas de Despachos. El proceso de creación y gestión de una ruta es el siguiente:
  - 1️⃣ **Generar ruta**. Para ello el programa sigue para las rutas de despachos, la siguente secuencia
    - Pide el número despacho y a continuación visualiza los pedidos con estado 'generado' de ese despacho.
    - Muestra los vehículos disponibles en esa delegación y pide el vehiculo a asignar a la ruta.
    - Pide los pedidos a incluir en la ruta, validando que el peso y volumen total de los pedidos seleccionados no supere el peso o volumen máximo permitido en el vehículo
    - Si los pedidos seleccionados se validan correctamente, se pregunta si se desea confirmar la grabación de la ruta.
      - La ruta se crea incluyendo con número correlativo de ruta, la delegación seleccionada, una lista de los pedidos seleccionados, tipo de ruta 'recogida'
      - los pedidos seleccionados cambian al estado "en_ruta"
      - El vehículo seleccionado pasa al estado disponible=False


  - 2️⃣ **Recepcionar pedidos de ruta**. El programa seguirá la siguiente lógica:
    - Pedir una ruta de recogida y mostrar los pedidos de esa ruta que siguen con estado 'en_ruta'.
    - Pedir la lista de los recibos que se han recepcionado
    - Marcar los pedidos recepcionados con estado 'en_delegacion_xxxxx'
    - Mostrar los pedidos pendientes de recepcionar
    - Preguntar si se marca la ruta como terminada
    - Si se marca como terminada, se marca el vehiculo como disponibles=True. 
    - Los pedidos que no se han recogido, se vuelve al estado como 'generado'


  - 3️⃣ **Visalizar rutas**. Despues de generar ruta o recepcionar pedidos, podemos ver el estado de las rutas activas.




## 🧠 Filosofía de la aplícación
  - Las delegaciónes se encargan de recoger, gestionar, transportar, y entregar los pedidos que generen los clientes. Existen 3 tipos de delegaciones:
    - **Despachos**
    - **Bases**,
    - **Central**.


  - **Despachos** (ámbito local) ➡️ dependen de las **Bases** (ámbito provincial) y estas a su vez ➡️dependen de la **Central** (ámbito nacional)


- **Delegaciones tipo Despacho**. Una por localidad. Su función es:
  - Recoger los pedidos de los clientes de ese despacho desde su domicilio. **Ruta de recogida**
  - Entregar los pedidos con destino a clientes de ese despacho. **Ruta de entrega**
    

- **Delegaciones tipo Base**. Una por provincia. Su función es:
  - Recibir los pedidos con origen en Despachos de esa base. 
    - **Ruta de transporte de recepción desde Despachos**
  - Enviar los pedidos con destino a Despachos de esa base. 
    - **Ruta de transporte de envío hasta Despachos**
  - Agrupar los pedidos procedentes de sus Despachos cuyo destino sean otros Despachos pertenecientes a otras bases(otra provincia)
  - Des-Agrupar los pedidos procedentes de otras bases, cuyo destino seán Despachos de esa base.


- **Delegación central**. Una sola, a nivel nacional, Ubicada en Madrid. Su función es:
  - Recibir los pedidos agrupados provenientes de las bases origen. **Ruta de transporte de recepción de Bases** 
  - Enviar los pedidos agrupados con destino a las bases destino. **Ruta de transporte de envío a bases**

```
main.py
   ↓
menu principal/
   ↓
Generación de datos de prueba /
   ↓
Mantenimiento de maestros/
   ↓
Gestión de rutas/
   ↓
datos/
```

---

# 🧱 Estructura del proyecto

```
logistica/
│
├── clases/
│   ├── delegacion.py
│   ├── cliente.py
│   ├── vehiculo.py
│   ├── pedido.py
│   └── ruta.py
│
├── persistencia/
│   ├── persistencia_delegaciones.py
│   ├── persistencia_clientes.py
│   ├── persistencia_vehiculos.py
│   ├── persistencia_pedidos.py
│   ├── persistencia_rutas.py
│   └── geocoding_cache.py
│
├── utiles/
│   ├── utils.py
│   └── geolocalizacion.py
│
├── datos/
│   ├── delegaciones.json
│   ├── clientes.json
│   ├── vehiculos.txt
│   ├── pedidos.json
│   ├── vehiculos.txt
│   ├── rutas.json
│   ├── cache_direcciones.json
│   ├── geocoding_cache.json
│   ├── ruta.html
│   ├── mapa_clientes.html
│   ├── mapa_delegaciones.html
│   └── mapa_pedidos.html
│
├── programas/
│   ├── generar_delegaciones.py
│   ├── generar_clientes.py
│   ├── generar_vehiculos.py
│   ├── generar_pedidos.py
│   ├── generar_rutas_despachos.py
│   ├── mantenimiento_delegaciones.py
│   ├── mantenimiento_clientes.py
│   ├── mantenimiento_vehiculos.py
│   └── mantenimiento_pedidos.py
│
├── menu/
│   └── menu_principal.py
│
├── tests/
│   ├── test_10_generar_clientes.py
│   ├── test_15_prueba_delegaciones.py
│   └── test_16_generar_pedidos.py
│
└── main.py
```

---

# 🧬 Herencia
 
## 🔹 Delegación (Clase abstracta)
- 🌳Clases derivadas
  - 🛵 Despacho
  - 📦 Base
  - 🏭 Central

  
Los despachos dependen de las bases y estas de la central

Ejemplo:
```
🏭 Central
   └── 📦 Base Alicante
          ├── 🛵 Despacho 12
          ├── 🛵 Despacho 16
          └── 🛵 Despacho 19
          
   
```
## 🔹 Vehiculo (Clase abstracta)
- 🌳Clases derivadas
  - 🎒 Mochila. Utilizadas en despachos
  - 🛵 Motocicleta. Utilizadas en despachos
  - 🚐 Furgoneta. Utilizada en despachos y bases.
  - 🚛 Camion. Utilizada en central

## 🔹 Pedido
- 🌳Clases derivadas
  - 📦📦GrupoPedidos (clase abstracta)
    - GrupoPedidosRecogida
    - GrupoPedidosTransporte
    - GrupoPedidosReparto

---


# ⚙️ Tecnologías

- Python 3.9+
- Folium, para visualización de mapas
- Geopy, para geolocalización
- Networkx, para generación de grafos y cálculo de ruta optima mediante algoritmo del viajante
- JSON (persistencia)
- Programación Orientada a Objetos (POO)
  - Herencia, polimorfismo, encapsulamiento.


---

# ▶️ Ejecución

```bash
python main.py
```



# ⚠️ Consideraciones

- Las APIs de geolocalización tienen límites de uso  
- Las direcciones devueltas por la geolocalización, a partir de unas coordenadas, se normalizan para extraer la población y la provincia
- Algunas direcciones pueden no resolverse, a pesar la normalización, si no se consigue extraer población y provincia, se excluyen
- Se utiliza cache para geolocalizar y evitar que se bloquee por repetición de consultas

---

# 📈 Mejoras futuras

- Implementar la gestion de rutas de bases y central
- Sustituir la generación de rutas basada en geolocalización por rutas reales (Google Maps)
- Mejorar Interfaz gráfica  
- Persistencia en Base de datos real  
- Dashboard  

---

# 👨‍💻 Autores

- Manuel Quiles Gómez  

---

# 📄 Licencia

Uso educativo / académico