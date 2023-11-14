#!/bin/bash

# Install Docker (Ubuntu/Debian example, adjust for other OS)
sudo apt-get update
sudo apt-get install -y docker.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Build and start containers
docker-compose up -d --build

# Wait for the database to be ready (adjust the duration as needed)
echo "Waiting for DB to be ready..."
sleep 10
# Run Django makemigrations
docker-compose exec backend python manage.py makemigrations
# Run Django migrations
docker-compose exec backend python manage.py migrate

# Create Django superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('mansy', 'mansy@example.com', 'mansy')" | docker-compose exec -T backend python manage.py shell

echo "Setup complete. Use './run.sh' to start the application."
