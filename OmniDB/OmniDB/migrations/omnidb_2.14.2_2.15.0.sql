INSERT INTO db_type VALUES('terminal',1);--omnidb--

UPDATE mon_units SET is_default = 1 WHERE unit_id IN (1, 2, 6, 8, 10);--omnidb--

UPDATE version SET ver_id = '2.15.0';--omnidb--
