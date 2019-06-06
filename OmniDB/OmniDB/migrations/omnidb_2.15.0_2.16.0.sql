ALTER TABLE users ADD COLUMN welcome_closed integer;--omnidb--

UPDATE users
SET welcome_closed = 0--omnidb--

UPDATE version SET ver_id = '2.16.0';--omnidb--
