#!/bin/bash
set -e



create_db() {
    database=$1
    connstr=""
    # Se a variavel $PGPASSWORD nao estiver definida (tamanho zero) o script
    # foi executado externamente (não durante a configuração inicial do banco),
    # entao e necessario determinar a string de conexao com usuario
    if [ -z "$PGPASSWORD" ]; then
        connstr="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/"
    fi
    psql "$connstr" <<-EOSQL
        CREATE ROLE "$database" ENCRYPTED PASSWORD '$POSTGRES_PASSWORD' LOGIN NOCREATEROLE CREATEDB NOSUPERUSER CONNECTION LIMIT -1;
        CREATE DATABASE "$database" WITH TEMPLATE = "template0" ENCODING = 'UTF-8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';
        GRANT ALL ON DATABASE "$database" TO "$database";
EOSQL
}

if [ -n "$POSTGRES_DATABASES" ]; then
	for db in $(echo "$POSTGRES_DATABASES" | tr ',' ' '); do
		create_db "$db"
	done
fi
# psql -U postgres
# CREATE USER postgres WITH ENCRYPTED PASSWORD 'postgres';
# CREATE DATABASE db_bora_la;
# GRANT ALL PRIVILEGES ON DATABASE db_bora_la TO postgres;
# \l