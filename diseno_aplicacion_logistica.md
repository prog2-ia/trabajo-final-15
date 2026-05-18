# 🚚 Diseño General de la Aplicación de Gestión Logística

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

Generar automáticamente información para testing sin necesidad de introducirla manualmente.

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

- Central
- Base
- Despacho

### 👤 Clientes

- Datos personales
- Dirección
- Provincia
- Población
- Coordenadas
- Delegación cercana
- Pedidos asociados

### 🚚 Vehículos

- Camión
- Furgoneta
- Motocicleta
- Mochila

### 📦 Pedidos

- Cliente origen
- Cliente destino
- Peso
- Volumen
- Estado
- Ruta asignada

### 🛣️ Rutas

- Ruta de recogida
- Ruta de entrega
- Ruta de transporte

---

# 3️⃣ Gestión de rutas

## 🎯 Objetivo

Automatizar el flujo logístico de los pedidos.

---

# 🔄 Flujo logístico completo

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

---

# 🏢 Jerarquía de delegaciones

```text
CENTRAL (Nacional)
│
├── BASE Alicante
│      ├── DESPACHO Elche
│      ├── DESPACHO Alicante
│      └── DESPACHO Benidorm
│
├── BASE Valencia
│      ├── DESPACHO Gandía
│      ├── DESPACHO Torrent
│      └── DESPACHO Valencia
│
└── BASE Madrid
       ├── DESPACHO Getafe
       ├── DESPACHO Alcalá
       └── DESPACHO Móstoles
```

---

# 🚚 Funciones logísticas por tipo de delegación

## 🏠 Delegaciones tipo Despacho

### Funciones

- Recoger pedidos de clientes
- Entregar pedidos locales
- Gestionar rutas urbanas

### Vehículos permitidos

- Furgonetas. 
- Motocicletas. 
- Mochilas. 

---

## 🏭 Delegaciones tipo Base

### Funciones

- Recibir pedidos desde despachos
- Enviar pedidos a despachos
- Agrupar mercancía
- Des-agrupar mercancía
- Conectar provincias

### Vehículos permitidos

- Furgonetas grandes
- Camiones ligeros

---

## 🏢 Delegación Central

### Ubicación

Madrid

### Funciones

- Recibir mercancía de bases
- Clasificación nacional
- Redistribución nacional
- Coordinación interprovincial

### Vehículos permitidos

- Camiones de gran capacidad

---

# 📦 Flujo de estados de un pedido

```text
generado
    │
    ▼
en_recogida
    │
    ▼
en_despacho_(origen)
    │
    ▼
en_base_(origen)    
    │
    ▼
en_central
    │
    ▼
en_base(destino)
    │
    ▼
en_despacho(destino)
    │
    ▼
en_reparto
    │
    ▼
entregado
```

---

# 🚛 Relación entre delegaciones y vehículos

| Delegación | Vehículos permitidos |
|---|---|
| Central | Camiones |
| Base | Furgonetas grandes |
| Despacho | Furgonetas, motos, mochilas |

---

# 🗂️ Persistencia de datos

```text
datos/
│
├── delegaciones.json
├── clientes.json
├── pedidos.json
├── rutas.json
├── cache_direcciones.json
└── vehiculos.txt
```

---

# 🧠 Optimización de rutas

- Nearest Neighbor
- Distancia geográfica
- NetworkX
- TSP (Traveling Salesman Problem)

---

# 🌍 Geolocalización

## Funcionalidades

- Geocodificación de direcciones
- Reverse geocoding
- Obtención automática de:
  - Provincia
  - Población
  - Coordenadas GPS

## Librerías

- geopy
- Nominatim
- folium

---

# 🗺️ Visualización gráfica

## Mapas interactivos

- Delegaciones
- Clientes
- Pedidos
- Rutas optimizadas

## Tecnología

- Folium + OpenStreetMap

---

# 📚 Diseño orientado a objetos

```text
Delegacion
├── DelegacionCentral
├── DelegacionBase
└── DelegacionDespacho

Vehiculo
├── VehiculoCamion
├── VehiculoFurgoneta
├── VehiculoMotocicleta
└── VehiculoMochila

Cliente
Pedido
Ruta
```

---

# 🔧 Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lógica principal |
| JSON/TXT | Persistencia |
| NetworkX | Optimización |
| Folium | Mapas |
| Geopy | Geolocalización |
| NumPy | Cálculos |
| JupyterLab | Testing y análisis |

---

# 📈 Flujo completo resumido

```text
1. Generar datos de prueba
2. Crear clientes
3. Geolocalizar direcciones
4. Asignar delegaciones
5. Crear pedidos
6. Generar rutas
7. Asignar vehículos
8. Optimizar recorrido
9. Persistir información
10. Visualizar mapas y rutas
```
