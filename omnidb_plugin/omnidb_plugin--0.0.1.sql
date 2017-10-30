\echo Use "CREATE EXTENSION omnidb_plugin" to load this file. \quit

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
  finished      BOOLEAN
);

CREATE TABLE omnidb.variables
(
  pid           INTEGER NOT NULL,
  name          TEXT,
  attribute     TEXT,
  vartype       TEXT,
  value         TEXT
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
  tend          TIMESTAMP WITHOUT TIME ZONE
);

ALTER TABLE omnidb.statistics
ADD CONSTRAINT omnidb_statistics_contexts_fk
FOREIGN KEY (pid)
REFERENCES omnidb.contexts (pid)
ON DELETE CASCADE;
