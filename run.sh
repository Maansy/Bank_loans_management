#!/bin/bash

# Start containers
docker-compose up -d

echo "Application is running. Backend: http://localhost:8000, Frontend: http://localhost:8080"
