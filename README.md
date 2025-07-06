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

## Configuración de la base de datos con Docker

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
2) Crear una nueva conexión MySQL
3) Configurar:
    - Host: localhost
    - Puerto: 3307
    - Usuario: root
    - Contraseña: rootpassword
> [!WARNING]
> Atencion: No seleccionar nada en el campo "Base de Datos", esta se creará después.

4️⃣ Crear base de datos y tablas en la nueva conexión:

En el directorio