UPDATE db_type
SET dbt_in_enabled = 1
WHERE dbt_st_name IN ('mysql', 'mariadb');--omnidb--

UPDATE version SET ver_id = '2.7.0';--omnidb--
