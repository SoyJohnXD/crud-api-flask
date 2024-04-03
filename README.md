# Proyecto de Aprendizaje de Flask CRUD

Este proyecto es una aplicación simple de Flask que implementa operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para gestionar roles en una base de datos MySQL. Utiliza Flask para crear una API RESTful que permite a los usuarios realizar las siguientes acciones:

- Obtener una lista de todos los roles.
- Obtener un rol específico por su ID.
- Crear un nuevo rol.
- Actualizar un rol existente.
- Eliminar un rol.

## Requisitos

- Docker
- Docker Compose

## Instalación y Uso con Docker Compose

1. Clona este repositorio en tu máquina local utilizando el siguiente comando:

    ```
    git clone https://github.com/tu_usuario/flask-crud.git
    ```

2. Navega al directorio del proyecto:

    ```
    cd flask-crud
    ```

3. Ejecuta el siguiente comando para construir y levantar los contenedores Docker:

    ```
    docker-compose up -d --build
    ```

4. Accede a la documentación de la API en tu navegador visitando la URL [http://localhost:4000/docs](http://localhost:4000/docs).

5. Utiliza las rutas de la API para realizar operaciones CRUD en los roles de la base de datos.


