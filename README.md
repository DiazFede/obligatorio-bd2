# Sistema de Votación Online - Corte Electoral

Este proyecto es un **sistema de votación online** que permite a los ciudadanos **participar en elecciones de forma autónoma y segura**, garantizando **anonimato de voto, control administrativo y generación de estadísticas**.

Incluye:

✅ Backend en **Flask**  
✅ Frontend en **React**  
✅ Base de datos **MySQL vía Docker**  
✅ Estadísticas con **Chart.js**

---

## Requisitos previos

✅ **Docker y Docker Compose instalados**  
✅ **Python 3.10+ instalado**  
✅ **Node.js 18+ instalado**  
✅ **DataGrip para gestionar la base de datos visualmente**

---

## Configuración de la base de datos con Docker y DataGrip

1️⃣ Ubicarse en la carpeta raíz del proyecto donde está el `docker-compose.yml`:
```bash
cd obligatorio-bd2
```

2️⃣ Levantar el contenedor de MySQL:
```bash
docker-compose up -d
```

3️⃣ Crear la conexión a la base de datos en DataGrip:

1) Abrir DataGrip.
2) Crear una nueva conexión MySQL.
3) Configurar:
    - Host: localhost
    - Puerto: 3307
    - Usuario: root
    - Contraseña: rootpassword
> [!WARNING]
> Atencion: No seleccionar nada en el campo "Base de Datos", esta se creará después.

4️⃣ Crear base de datos y tablas en la nueva conexión:

En el directorio:
```bash
/obligatorio-bd2/db/init
```
Podemos encontrar los archivos:
```bash
schema.sql
insert.sql
```
Los cuales contienen las tablas y los datos de prueba (respectivamente). Para terminar la configuración de la base de datos, debemos:
1) Abrir una nueva "query console" en nuestra conexión.
2) Abrir, copiar y pegar el archivo "schema.sql" en la consola y ejecutarlo. Esto nos creará la base de datos y las tablas.
3) Abrir, copiar y pegar el archivo "insert.sql" en la consola y ejecutarlo. Esto nos insertará los datos de prueba en cada tabla.

> [!WARNING]
> Es importante ejecutar los pasos en orden para que DataGrip no de error.

Una vez hecho esto, habremos terminado la configuración de nuestra base de datos.

## Configuración del backend

1️⃣ Ubicarse en la carpeta del backend:
```bash
cd backend
```

2️⃣ Crear un entorno virtual:
```bash
python -m venv venv
```

3️⃣ Activar el entorno virtual:

Si estas usando un sistema operativo Windows, ejecuta:
```bash
venv\Scripts\activate
```

Si estas usando un sistema operativo MacOS o Linux, ejecuta:
```bash
source venv/bin/activate
```

4️⃣ Instalar dependencias:
```bash
pip install -r requirements.txt
```

5️⃣ Levantar el backend:
```bash
python run.py
```
Una vez hecho esto, habremos terminado la configuración de nuestra base de datos.
> [!TIP]
> El backend quedará disponible en http://localhost:5000