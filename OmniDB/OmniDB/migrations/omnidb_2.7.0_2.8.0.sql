ALTER TABLE connections ADD COLUMN ssh_server varchar(500);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_port varchar(20);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_user varchar(100);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_password varchar(100);--omnidb--
ALTER TABLE connections ADD COLUMN ssh_key text;--omnidb--
ALTER TABLE connections ADD COLUMN use_tunnel integer;--omnidb--

UPDATE connections
SET ssh_server = '',
    ssh_port = '22',
    ssh_user = '',
    ssh_password = '',
    ssh_key = '',
    use_tunnel = ''--omnidb--

UPDATE version SET ver_id = '2.8.0';--omnidb--
