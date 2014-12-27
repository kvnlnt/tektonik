--insert into path_pages (path_id, page_id) values (2,3)

--DELETE FROM path_pages where 1=1

SELECT 
        page.id,
        page.page,
FROM
        path_pages as path_page,
        pages as page
WHERE
        path_page.path_id = 1 AND
        path_page.page_id = page.id

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
   