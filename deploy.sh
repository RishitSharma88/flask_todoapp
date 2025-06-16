#!/bin/bash

# Update package info
sudo apt-get update -y

# Install Docker if not installed
if ! command -v docker &> /dev/null
then
    echo "Docker not found, installing..."
    sudo apt-get install -y docker.io
else
    echo "Docker already installed"
fi

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Pull your Docker image (replace with your actual image)
sudo docker pull rishitsharma88/flask-todo-app:latest

# Stop and remove any existing container named 'todo-container'
if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^todo-container$"; then
    sudo docker stop todo-container
    sudo docker rm todo-container
fi

# Run the container
sudo docker run -d --name todo-container -p 5000:5000 your-dockerhub-username/flask-todo-app:latest

echo "App deployed and running on port 5000"
