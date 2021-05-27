=================
 Recurso de Pago
=================

Recurso POST
------------
.. http:post:: /api/v1/payment

Crea un Pago

**Campos obligatorios**

:reservation: **(integer)** ID de reservación.
:price: **(integer)** Precio de pago.
:concept: **(string)** Concepto de pago.
:status: **(string)** Estado de pago.

**Notas importante**

    * :status: : (approved, rejected, pending, cancelled)

**Ejemplo de petición**

.. sourcecode:: http

    POST /api/v1/payment HTTP/1.1
    Content-Type: application/json
    Authorization: Bearer asiherlksdnfsuhse...

    {
        "reservation": 2,
        "price": 8000,
        "concept": "Pago de reserva",
        "status": "approved"
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
            "reservation": [
                "Este campo es requerido."
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


.. sourcecode:: http

    HTTP/1.1 404 NOT_FOUND
    Content-Type: application/json

    {
        "code": "resrvation_not_found",
        "detail": "Reservación no encontrada"
    }

:status 201: Pago creado
:status 400: Cuerpo inválido
:status 401: No token o token inválido
:status 403: No eres admin bro
:status 404: Reservación't

Recurso GET
------------
.. http:get:: /api/v1/payment

Devuelve una lista de pagos

**Atributos opcionales**

:id: **(integer)** ID del pago.
:reservation: **(integer)** ID de la reservación.
:status: **(string)** Estado de pago

**Ejemplo de petición**

.. sourcecode:: http

    GET /api/v1/payment HTTP/1.1
    Authorization: Bearer asiherlksdnfsuhse...

**Ejemplo de respuesta**

.. sourcecode:: http

    HTTP/1.1 200 OK
    Content-Type: application/json

    {
        "count": 1,
        "data": [
            {
                "reservation": {
                    "id": 1,
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
                    "initial_hour": "2021-05-21T05:25:00-05:00",
                    "final_hour": "2021-05-21T06:25:00-05:00",
                    "vehicle_plate": "",
                    "vehicle_type": "auto",
                    "slot": 1,
                    "document_number": null,
                    "email": null,
                    "status": "Finalizado",
                    "is_cancelled": false
                },
                "price": 12500,
                "concept": "prueba",
                "status": "approved"
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

.. sourcecode:: http

    HTTP/1.1 404 NOT_FOUND
    Content-Type: application/json

    {
        "code": "resrvation_not_found",
        "detail": "Reservación no encontrada"
    }

:status 200: Pagos retornados
:status 400: Cuerpo inválido
:status 401: No token o token inválido
:status 403: No eres admin bro
:status 404: Reservación't