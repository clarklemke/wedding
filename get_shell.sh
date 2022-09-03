#!/bin/bash
docker exec -t -i `docker ps -aqf "name=wedding-api-1" ` bash
