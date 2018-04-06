DROP SCHEMA IF EXISTS omnidb CASCADE;
CREATE SCHEMA omnidb;

CREATE FUNCTION omnidb.omnidb_enable_debugger(character varying)
RETURNS void AS '$libdir/omnidb_plugin'
LANGUAGE C IMMUTABLE STRICT;

CREATE TABLE omnidb.contexts
(
  pid           INTEGER NOT NULL PRIMARY KEY,
  function      TEXT,
  hook          TEXT,
  lineno        INTEGER,
  stmttype      TEXT,
  breakpoint    INTEGER NOT NULL,
  finished      BOOLEAN,
  username      TEXT DEFAULT current_user
);

CREATE TABLE omnidb.variables
(
  pid           INTEGER NOT NULL,
  name          TEXT,
  attribute     TEXT,
  vartype       TEXT,
  value         TEXT,
  username      TEXT DEFAULT current_user
);

ALTER TABLE omnidb.variables
ADD CONSTRAINT omnidb_variables_contexts_fk
FOREIGN KEY (pid)
REFERENCES omnidb.contexts (pid)
ON DELETE CASCADE;

CREATE TABLE omnidb.statistics
(
  pid           INTEGER NOT NULL,
  lineno        INTEGER,
  step          INTEGER,
  tstart        TIMESTAMP WITHOUT TIME ZONE,
  tend          TIMESTAMP WITHOUT TIME ZONE,
  username      TEXT DEFAULT current_user
);

ALTER TABLE omnidb.statistics
ADD CONSTRAINT omnidb_statistics_contexts_fk
FOREIGN KEY (pid)
REFERENCES omnidb.contexts (pid)
ON DELETE CASCADE;
