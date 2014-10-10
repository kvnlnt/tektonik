==================================================================
ark.tektonik
==================================================================

ark.tektonik or just "tektonik" is the rest api for the project `ARK <http://code.kevinlint.com>`_. It's resources can be best understood by reviewing the ARK project's documentation.

.. _TOP:
.. contents:: Table of Contents
   :depth: 2

Properties
-----------
Properties are domain names.

.. list-table:: MODEL
   :header-rows: 1

   * - Column
     - Type
   * - id
     - primary key
   * - property
     - string

/properties
***********

.. contents:: 
   :local: 

POST
^^^^

Example::

   curl -i -H "Content-Type: application/json" -X POST -d '{"property":"website.com"}' http://127.0.0.1:5000/properties

Headers:

- Content-Type: application/json

Request:

.. code-block:: javascript

    {
      "property": "my.website.com"
    }

Response:

.. code-block:: javascript

    {
      "id":1,
      "property": "my.website.com"
    }

Returns:

- 201
- 400


GET
^^^^

Example::

   curl -i -H http://127.0.0.1:5000/properties

Response:

.. code-block:: javascript

    {
      "id":1,
      "property": "my.website.com"
    },
    {
      "id":2,
      "property": "other.website.com"
    }

Returns:

- 200
- 404

----

TOP_

