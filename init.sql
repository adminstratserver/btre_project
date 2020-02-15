CREATE DATABASE btre_prod;
CREATE USER dbadmin WITH PASSWORD 'Romans12:1';
ALTER ROLE dbadmin SET client_encoding TO 'utf8';
ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbadmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE btre_prod TO dbadmin;

