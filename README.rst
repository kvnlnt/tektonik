==================================================================
ark.tektonik
==================================================================

ark.tektonik or just "tektonik" is the rest api for the project `ARK <http://code.kevinlint.com>`_. It's resources can be best understood by reviewing the ARK project's documentation.

.. contents:: Table of Contents

Properties
-----------
Properties are domain names. That's it.

/properties
***********

    .. list-table:: MODEL
       :header-rows: 1

       * - Column
         - Type
       * - id
         - integer
       * - property
         - string

    GET::

        curl http://127.0.0.1:5000/properties

    POST::

       curl -i -H "Content-Type: application/json" -X POST -d '{"property":"website.com"}' http://127.0.0.1:5000/properties


/properties/:id
***************
- GET
- PUT
- DELETE
