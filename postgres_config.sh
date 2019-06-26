#!/bin/bash

#set up Postgres tables and config files for intel-data-mgmt-for-rt-Models
#do this if you haven't set up a postgres table yet, otherwise ignore this section
echo "CREATE USER <user> PASSWORD '<db_pwd>'; CREATE DATABASE <db name>; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <user>;" | sudo -u postgres psql
sudo -u postgres sed -i "s|#listen_addresses = 'localhost'|listen_addresses = '*'|" /etc/postgresql/10/main/postgresql.conf
sudo -u postgres sed -i "s|127.0.0.1/32|0.0.0.0/0|" /etc/postgresql/10/main/pg_hba.conf
sudo -u postgres sed -i "s|::1/128|::/0|" /etc/postgresql/10/main/pg_hba.conf
service postgresql restart
