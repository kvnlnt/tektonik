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

.. list-table:: POST
   :header-rows: 1

   * - Content-Type
     - Requires
     - Returns
     - Payload
   * - application/json
     - property
     - 201 or 400
     - JSON

Example::

   curl -i -H "Content-Type: application/json" -X POST -d '{"property":"website.com"}' http://127.0.0.1:5000/properties


.. list-table:: GET
   :header-rows: 1

   * - Content-Type
     - Requires
     - Returns
     - Payload
   * - n/a
     - n/a
     - 200 or 404
     - JSON

Example::

   curl http://127.0.0.1:5000/properties


/properties/:id
***************

.. list-table:: GET
   :header-rows: 1

   * - Content-Type
     - Requires
     - Returns
     - Payload
   * - id
     - n/a
     - 200 or 404
     - JSON

Example::
    
    curl http://127.0.0.1:5000/properties/1

.. list-table:: PUT
   :header-rows: 1

   * - Content-Type
     - Requires
     - Returns
     - Payload
   * - application/json
     - property
     - 200 or 400
     - JSON

Example::

   curl -i -H "Content-Type: application/json" -X POST -d '{"property":"website.com"}' http://127.0.0.1:5000/properties/1


.. list-table:: DELETE
   :header-rows: 1

   * - Content-Type
     - Requires
     - Returns
     - Payload
   * - n/a
     - n/a
     - 204 or 400
     - n/a

Example::

   curl -i -H DELETE http://127.0.0.1:5000/properties/1
