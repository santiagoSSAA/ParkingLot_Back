========================
 Recurso de Reservación
========================

Recurso POST
-------------
.. http:get:: /api/v1/reservation

Crea una reservación

**Campos opcionales**

:initial_hour: **(datetime)** Hora de inicio (yyyy-mm-dd HH:MM)

:document: **(string)** Documento (en caso de ser reserva sin usuario)

:email: **(string)** Email 

:slot: **(integer)** id del slot

:final_hour: **(datetime)** Hora de finalización (mismo formato que arriba)

:vehicle_type: **(string)** auto o moto

:vehicle_plate: **(string)** placa de vehiculo


**Ejemplo de petición**

.. sourcecode:: http

    POST /api/v1/reservation HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer asiherlksdnfsuhse...
    {
        "document": "1002938192",
        "email": "pepe@email.com",
        "initial_hour": "2021-05-21 12:45",
        "slot": 1,
        "number_plate": "pfg098",
        "vehicle_type": "auto"
    }

    {
        "initial_hour": "2021-05-21 12:45",
        "final_hour": "2021-05-21 18:45",
        "user": 3
    }

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 201 CREATED
    Content-Type: application/json
    {
        "created": 3
    }

Recurso GET
------------
.. http:get:: /api/v1/reservation

Devuelve una lista de reservaciones

**Ejemplo de petición**

.. sourcecode:: http

    GET /api/v1/reservation HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    **SI ES ADMIN**

    {
        "count": 1,
        "data": [{
            "user" : {
                "id": 1,
                "email": "pepe@email.com",
                "name": "pepe garcia",
                "cellphone": "31928309189",
                "creation_date": "20201-02-12T01239123.12312",
                "birthdate": "20201-02-12T01239123.12312",
                "gender": "M",
                "profile": "user",
                "number_plate": "pfg098"
            },
            "initial_hour": "20201-02-12T01239123.12312",
            "final_hour": "20201-02-12T01239123.14576",
            "number_plate": null,
            "vehicle_type": null,
            "slot": {
                "id": 12,
                "place_code": "A123"
            },
            "document_number": "1002938292",
            "email": null,
            "is_cancelled": false
        }]        
    }

    **SI NO ES ADMIN**

    {
        "code": 1,
        "data": [
            {
                "id": 3,
                "initial_hour": "2021-06-01T16:45:00-05:00",
                "final_hour": "2021-06-21T17:55:00-05:00",
                "number_plate": "",
                "vehicle_type": "auto",
                "slot": "FPG0981",
                "status": "Vigente" (o Finalizado o Próximo)
            }
        ]
    }

Recurso GET
------------
.. http:get:: /api/v1/reservation/price/{id:int}

Devuelve el precio de una reservación

**Ejemplo de petición**

.. sourcecode:: http

    GET /api/v1/reservation/price/1 HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "price": 8000.0,
        "hours": 1
    }


Recurso PATCH
--------------
.. http:get:: /api/v1/reservation/{id:int}

Actualiza los datos de una reservacion

**Campos opcionales**
:document: **(string)**
:email: **(string)**
:initial_hour: **(string)**
:final_hour: **(string)**
:vehicle_plate: **(string)**
:vehicle_type: **(string)**

**Ejemplo de petición**

.. sourcecode:: http

    PATCH /api/v1/reservation HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer asiherlksdnfsuhse...

    {
        "document": "1002938192",
        "email": "pepe@email.com",
        "initial_hour": "2021-05-21 12:45",
        "slot": 12,
        "number_plate": "pfg098",
        "vehicle_type": "auto"
    }

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK

Recurso DELETE
---------------
.. http:get:: /api/v1/reservation/{id:int}

Cancela una reservación

**Ejemplo de petición**

.. sourcecode:: http

    DELETE /api/v1/reservation HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK