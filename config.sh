#!/bin/bash
sed -i -e "s/microservice/$1/g" serverless.yml package.json docker-compose.yml
rm serverless.yml-e package.json-e docker-compose.yml-e
