#!/bin/bash

# Update system
apt update && apt upgrade -y

# Install common tools
apt install -y curl git nginx docker.io ,docker.dev , docker.vm
# Start services
systemctl enable nginx
systemctl start nginx

systemctl enable docker
systemctl start docker

echo "Server setup complete"
