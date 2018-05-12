ALTER TABLE connections ADD COLUMN ssh_server varchar(500);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_port varchar(20);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_user varchar(100);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_password varchar(100);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_key text;--omnidb--
ALTER TABLE connections ADD COLUMN use_tunnel integer;--omnidb--

UPDATE version SET ver_id = '2.8.0';--omnidb--
