--insert into path_pages (path_id, page_id) values (2,3)

--DELETE FROM path_pages where 1=1


--SELECT
--    property.id,
--    property.property
--FROM
--    properties as property
--WHERE
--    property.id = 1

SELECT
        path_page.id as path_page_id,
        page.id,
        page.page
FROM
        path_pages as path_page,
        pages as page
WHERE
        path_page.path_id = 1 AND
        path_page.page_id = page.id


--SELECT 
--        path.id,
--        path.path
--FROM
--        path_pages as path_page,
--        paths as path
--WHERE
--        path_page.page_id = 2 AND
--        path_page.path_id = path.id

--SELECT 
--        count(distinct page.id) as total_pages,
--        count(distinct path.id) as total_paths
--FROM
--        properties as property,
--        paths as path,
--        path_pages as path_page,
--        pages as page
-- WHERE
--        property.id = 1 AND
--        path.property_id = property.id AND
--        path_page.path_id = path.id AND
--        path_page.page_id = page.id
   