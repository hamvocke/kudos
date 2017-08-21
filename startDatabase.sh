#! /bin/bash
docker stop kudos-postgres
docker rm kudos-postgres
docker run --name kudos-postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=kudos -d postgres
