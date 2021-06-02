========================
 Recurso de Parqueadero
========================

Recurso POST
-------------
.. http:post:: /api/v1/parking_slot

Crea un slot de parqueadero.

**Campos obligatorios**

:place_code: **(string)** código de slot.

**Ejemplo de petición**

.. sourcecode:: http

    POST /api/v1/parking_slot HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer asiherlksdnfsuhse...

    {
        "place_code": "A123"
    }

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json

    {
        "created": 8
    }


Recurso GET
------------
.. http:get:: /api/v1/parking_slot

Devuelve una lista de slots.

**Atributos opcionales**

:place_code: **(string)** Código de slot.
:status: **(string)** Estado de slots.

**Ejemplo de petición**

.. sourcecode:: http

    GET /api/v1/parking_slot HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    **SI ES ADMIN**

    {
        "count": 1,
        "data": [
            {
                "id": 1,
                "place_code": "FPG098",
                "reservation": {
                    "id": 2,
                    "user": {
                        "id": 5,
                        "email": "ejemplo2@yopmail.com",
                        "name": "Pepe García",
                        "cellphone": "3182938192",
                        "document": "1002931293",
                        "creation_date": "2021-05-13T14:30:04.893672-05:00",
                        "birthdate": "2000-04-06",
                        "gender": "M",
                        "profile": "user",
                        "number_plate": "PFG068",
                        "vehicle_type": "auto"
                    },
                    "initial_hour": "2021-05-24T16:45:00-05:00",
                    "final_hour": "2021-05-24T17:55:00-05:00",
                    "number_plate": "",
                    "vehicle_type": "auto",
                    "slot": 1,
                    "document_number": null,
                    "email": null,
                    "status": "Vigente",
                    "is_cancelled": false
                },
                "status": "Ocupado"
            }
        ]
    }

    **SI NO ES ADMIN**

    {
        "count": 1,
        "data": [
            {
                "id": 1,
                "place_code": "FPG099"
            }
        ]
    }

Recurso GET específico
-----------------------
.. http:get:: /api/v1/parking_slot/{id:int}

Devuelve la info de un slot específico.


**Ejemplo de petición**

.. sourcecode:: http

    GET /api/v1/parking_slot/1 HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "data": {
            "id": 1,
            "place_code": "FPG098",
            "reservation": {
                "id": 2,
                "user": {
                    "id": 5,
                    "email": "ejemplo2@yopmail.com",
                    "name": "Pepe García",
                    "cellphone": "3182938192",
                    "document": "1002931293",
                    "creation_date": "2021-05-13T14:30:04.893672-05:00",
                    "birthdate": "2000-04-06",
                    "gender": "M",
                    "profile": "user",
                    "number_plate": "PFG068",
                    "vehicle_type": "auto"
                },
                "initial_hour": "2021-05-24T16:45:00-05:00",
                "final_hour": "2021-05-24T17:55:00-05:00",
                "number_plate": "",
                "vehicle_type": "auto",
                "slot": 1,
                "document_number": null,
                "email": null,
                "status": "Vigente",
                "is_cancelled": false
            },
            "status": "Ocupado"
        }
    }

Recurso PATCH
--------------
.. http:patch:: /api/v1/parking_slot/{id:int}

Modifica la info de un slot.

**Campos opcionales**

:place_code: **(string)** código de slot.

**Ejemplo de petición**

.. sourcecode:: http

    PATCH /api/v1/parking_slot HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer asiherlksdnfsuhse...

    {
        "place_code": "A123"
    }

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

Recurso DELETE
---------------
.. http:delete:: /api/v1/parking_slot/{id:int}

Elimina un slot.


**Ejemplo de petición**

.. sourcecode:: http

    DELETE /api/v1/parking_slot/1 HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json