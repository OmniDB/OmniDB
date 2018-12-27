UPDATE connections SET ssh_server = '' WHERE ssh_server IS NULL;--omnidb--
UPDATE connections SET ssh_port = '22' WHERE ssh_port IS NULL;--omnidb--
UPDATE connections SET ssh_user = '' WHERE ssh_user IS NULL;--omnidb--
UPDATE connections SET ssh_password = '' WHERE ssh_password IS NULL;--omnidb--
UPDATE connections SET ssh_key = '' WHERE ssh_key IS NULL;--omnidb--
UPDATE connections SET use_tunnel = 0 WHERE use_tunnel IS NULL;--omnidb--

UPDATE version SET ver_id = '2.14.0';--omnidb--
