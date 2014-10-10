==================================================================
ark.tektonik
==================================================================

ark.tektonik or just "tektonik" is the rest api for the project `ARK <http://code.kevinlint.com>`_. It's resources can be best understood by reviewing the ARK project's documentation.

.. contents:: Table of Contents

Properties
-----------
Properties are domain names. That's it.

.. list-table:: MODEL
   :header-rows: 1

   * - Column
     - Type
   * - id
     - integer
   * - property
     - string

/properties
***********
.. list-table:: METHODS
   :header-rows: 1

   * - Method
     - Content-Type
     - Requires
     - Returns
   * - GET
     - n/a
     - n/a
     - 200, JSON list of property objects
   * - POST
     - application/json
     - property
     - 201, property JSON object

EXAMPLES

- GET::
    
    curl http://127.0.0.1:5000/properties

- POST::

   curl -i -H "Content-Type: application/json" -X POST -d '{"property":"website.com"}' http://127.0.0.1:5000/properties


/properties/:id
***************
.. list-table:: METHODS
   :header-rows: 1

   * - Method
     - Content-Type
     - Requires
     - Returns
   * - GET
     - id
     - n/a
     - 200, JSON object of property
   * - PUT
     - application/json
     - property
     - 200, updated property JSON object
   * - DELETE
     - n/a
     - n/a
     - 204

EXAMPLES

- GET::
    
    curl http://127.0.0.1:5000/properties/1

- PUT::

   curl -i -H "Content-Type: application/json" -X POST -d '{"property":"website.com"}' http://127.0.0.1:5000/properties/1

- DELETE::

   curl -i -H DELETE http://127.0.0.1:5000/properties/1