#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE wonderfuldb;
	CREATE DATABASE sarchiapone;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "wonderfuldb" <<-EOSQL
	CREATE TABLE test_table_1 (varie VARCHAR (10));
	INSERT INTO test_table_1 VALUES ( 'aaaa' );
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "sarchiapone" <<-EOSQL
	CREATE TABLE tabellina (varie VARCHAR (10));
	INSERT INTO tabellina VALUES ( 'bbbb' );
EOSQL