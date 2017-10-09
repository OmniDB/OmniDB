#!/bin/bash

psql -h localhost -p 5405 -d omnidb_tests -U postgres -f ../../../database/dellstore2-normal-1.0.sql

