#!/bin/bash

# docker exec -it postgres_database psql -U evidence -d postgres -c "DROP DATABASE evidence;"

docker exec -it postgres_database psql -U evidence -d evidence -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
