==========================
 Recurso de Autenticación
==========================

Recurso POST
------------
.. http:post:: /api/v1/auth

Crea un token de Acceso

**Campos obligatorios**

:user: **(string)** Correo electrónico.
:password: **(string)** Contraseña.
:keep_logged_in: **(boolean)** token duradero (si o no). 
:type: **(string)** user o admin, dependiendo del tipo de usuario.

**Ejemplo de petición**

.. sourcecode:: http

    POST /api/v1/auth HTTP/1.1
    Content-Type: application/json

    {
        "user": "pepe@email.com",
        "password": "@sda2(*&8",
        "keep_logged_in": false,
        "type": "user"
    }

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "id": 1,
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHBpcmF0aW9uX2RawdGUiOiIyMDIxLTA1LTE0IDAyOjM1OjA1LjQ5OTYzOSIsImVtYWlsIjoiYWRtaW5AeW9wbWFpbC5jb20iLCJ0eXBlIjoiYWRtaW4iLCJyZWZyZXNoIjoiOXBubWUwSFdzMDY0cldLRDZ6R0llb2dYcmlCUGhOIn0.s9v3D4JV2QHGnJJ35E72przDZBILSl4s7S3BmOhAvZ4",
        "refresh": "9pnme0HWs064rWKD6zGIeogXriBPhN",
        "profile": "user"
    }

:status 201: Token creado
:status 400: Cuerpo con estructura inválida
:status 401: No autorizado
:status 404: Usuario no encontrado

Recurso PATCH
------------
.. http:patch:: /api/v1/auth

Inhabilita el token de un usuario.

**Ejemplo de petición**

.. sourcecode:: http

    PATCH /api/v1/auth HTTP/1.1
    Authorization: Bearer eyMask8sdfjsñlkdfmglkj5...

**Ejemplos de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK

.. sourcecode:: http

    HTTP/1.1 400 BAD_REQUEST

.. sourcecode:: http

    HTTP/1.1 404 NOT FOUND

:status 200: Token inhabilitado
:status 400: Cabecera inválida
:status 404: Token no encontrado