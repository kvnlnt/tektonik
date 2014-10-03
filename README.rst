========
TEKTONIK
========

1. Architecture
===============

1.1 Properties
--------------

Endpoints
~~~~~~~~~
/properties     GET     (read)
/property       POST    (create)
/property/:id   GET     (read)
/property/:id   PUT     (update)
/property/:id   DELETE  (delete)

Database
~~~~~~~~
properties      id, property


1.2 Paths
---------

Endpoints
~~~~~~~~~
/paths          GET     (read)
/path           POST    (create)
/path/:id       GET     (read)
/path/:id       PUT     (update)
/path/:id       DELETE  (delete)

Database
~~~~~~~~
paths           id, path, property_id

1.3 Path Pages
--------------

Endpoints
~~~~~~~~~
/path_pages     GET     (read)
/path_page      POST    (create)
/path_page/:id  GET     (read)
/path_page/:id  PUT     (update)
/path_page/:id  DELETE  (delete)

Database
~~~~~~~~
path_pages      id, path_id, page_id, isStatic, eff_date, exp_date


1.4 Pages
---------

Endpoints
~~~~~~~~~
/pages          GET     (read)
/page           POST    (create)
/page/:id       GET     (read)
/page/:id       PUT     (update)
/page/:id       DELETE  (delete)

Database
~~~~~~~~
pages           id, page


1.5 Page Parts
--------------

Endpoints
~~~~~~~~~
/page_parts      GET     (read)
/page_part       POST    (create)
/page_part/:id   GET     (read)
/page_part/:id   PUT     (update)
/page_part/:id   DELETE  (delete)

Database
~~~~~~~~
page_parts      id, page_id, part_id, order


1.6 Parts
---------

Endpoints
~~~~~~~~~
/parts          GET     (read)
/part           POST    (create)
/part/:id       GET     (read)
/part/:id       PUT     (update)
/part/:id       DELETE  (delete)

Database
~~~~~~~~
parts           id, part


