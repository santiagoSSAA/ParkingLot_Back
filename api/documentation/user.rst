====================
 Recurso de Usuario
====================

Recurso POST
------------
.. http:post:: /api/v1/user

Crea un usuario en la plataforma.

**Campos obligatorios**

:birthday: **(date)** Fecha de nacimiento.
:document: **(string)** Número de documento.
:name: **(string)** Nombres con apellidos.
:email: **(string)** Correo electrónico.
:password: **(string)** Contraseña.
:cellphone: **(string)** Número celular.
:gender: **(string)** Género ( M , F , U ).

*Campos opcionales*

:number_plate: **(string)** Número de placa.
:vehicle_type:: **(string)** Tipo de vehículo ( auto, moto ).

**Ejemplo de petición**

.. sourcecode:: http

    POST /api/v1/user HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer asiherlksdnfsuhse...

    {
        "birthdate": "2021-05-03T12:00:12.783015",
        "document": "1008293849",
        "name": "Cesar Alejandro Comino Hernandez",
        "email": "cesarElCrack@yopmail.com",
        "password": "5InchesInYourMom",
        "cellphone": "31829382938",
        "gender": "M",
        "number_plate": "PFG-053",
        "vehicle_type": "auto"
    }

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "inserted": 2
    }

.. sourcecode:: http

    HTTP/1.1 400 BAD_REQUEST
    Content-Type: application/json

    {
        "code": "invalid_body",
        "detail": "Cuerpo con estructura inválida",
        "data": {
            "names": [
                "Este campo es requerido."
             ]
        }
    }

.. sourcecode:: http

    HTTP/1.1 409 CONFLICT
    Content-Type: application/json

    {
        "code": "user_already_exist",
        "detailed": "El usuario ya existe en la base de datos"
    }

:status 201: Usuario creado
:status 400: Cuerpo con estructura inválida
:status 409: El usuario ya existe

Recurso GET
-----------
.. http:get:: /api/v1/user

Devuelve la información de usuarios de la plataforma.

**Campos opcionales**

:profile: **(string)** Perfil de usuario (**user**, **admin**)
:document: **(string)** Número de documento
:email: **(string)** Email del usuario

**Ejemplos de petición**

.. sourcecode:: http

    GET /api/v1/user?email=mail@mail.com HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...
    Range: 0-9

**Ejemplos de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "count": 1,
        "data": [
            {
                "birthdate": "2021-05-03T12:00:12.783015",
                "document": "1008293849",
                "name": "Cesar Alejandro Comino Hernandez",
                "email": "cesarElCrack@yopmail.com",
                "password": "5InchesInYourMom",
                "cellphone": "31829382938",
                "gender": "M",
                "number_plate": "PFG-053",
                "vehicle_type": "auto"
            }
        ]
    }

.. sourcecode:: http

    HTTP/1.1 401 UNAUTHORIZED

.. sourcecode:: http

    HTTP/1.1 403 FORBIDDEN

    {
        "code": "do_not_have_permission",
        "detailed": "No tienes permiso para ejecutar esta acción."
    }

:status 200: Usuarios retornados
:status 401: Token no enviado o inválido
:status 403: Acceso denegado al recurso

Recurso PATCH
-------------
.. http:patch:: /api/v1/user/<user_email>

Modifica la información de un usuario en la plataforma.

**Nota:** Se debe enviar como mínimo un dato. Todos los campos son opcionales.

:birthday: **(date)** Fecha de nacimiento.
:document: **(string)** Número de documento.
:name: **(string)** Nombres con apellidos.
:email: **(string)** Correo electrónico.
:password: **(string)** Contraseña.
:cellphone: **(string)** Número celular.
:gender: **(string)** Género ( M , F , U ).
:number_plate: **(string)** Número de placa.
:vehicle_type:: **(string)** Tipo de vehículo ( auto, moto ).
:is_active:: **(Boolean)** Es usuario activo.

**Ejemplo de petición**

.. sourcecode:: http

    PATCH /api/v1/user/micorreo@correo.com HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer eyaslm234jkh6ñl34k2354jkh...

    {
        "birthdate": "2021-05-03T12:00:12.783015",
        "document": "1008293849",
        "name": "Cesar Alejandro Comino Hernandez",
        "email": "cesarElCrack@yopmail.com",
        "password": "5InchesInYourMom",
        "cellphone": "31829382938",
        "gender": "M",
        "number_plate": "PFG-053",
        "vehicle_type": "auto",
        "is_active": true
    }

**Ejemplos de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK

.. sourcecode:: http

    HTTP/1.1 400 BAD_REQUEST
    Content-Type: application/json

    {
        "code": "invalid_body",
        "detail": "Cuerpo con estructura inválida",
        "data": {
            "email": [
                "No cumple con la expresión regular requerida."
                ]
        }
    }

.. sourcecode:: http

    HTTP/1.1 401 UNAUTHORIZED

.. sourcecode:: http

    HTTP/1.1 403 FORBIDDEN

    {
        "code": "do_not_have_permission",
        "detailed": "No tienes permiso para ejecutar esta acción."
    }
    
    :status 200: Usuario modificado
    :status 400: Cuerpo con estructura inválida
    :status 401: Token no enviado o inválido
    :status 403: Acceso restringido al recurso