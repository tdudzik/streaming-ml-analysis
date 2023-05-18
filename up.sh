#!/bin/sh
docker-compose down && docker-compose up -d --force-recreate --build && docker-compose logs -f

