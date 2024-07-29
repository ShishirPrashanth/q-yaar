# q-yaar
Get out to play.

## ***Project Specs***
* Python - 3.11.9
* Django - 5.0.7
* Postgres - 16.3

## ***Setup on Local***

### Setup Postgres
```bash
$ sudo su - postgres 
$ psql -p 5434 # (Or whichever port runs your postgres 16.3) This will open psql shell, follow these commands

CREATE DATABASE q_yaar_db;
CREATE USER q_yaar_user WITH PASSWORD 'q_yaar_password';
ALTER ROLE q_yaar_user SET client_encoding TO 'utf8';
ALTER ROLE q_yaar_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE q_yaar_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE q_yaar_db TO q_yaar_user;
ALTER ROLE q_yaar_user SUPERUSER;
ALTER ROLE q_yaar_user CREATEDB;
```
Connect to DB from command line using psql
```bash
psql -d postgres://q_yaar_user:q_yaar_password@localhost:5434/q_yaar_db # Use the applicable port number
```