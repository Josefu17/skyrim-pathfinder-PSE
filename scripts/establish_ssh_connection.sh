#!/bin/bash

# Exit the script if any command fails
set -e
set -x

# Docker login
echo "Logging into Docker registry..."
docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"

# Build and Push Docker images
echo "Building and pushing Docker images..."
make build-ci
make push

# Prepare SSH directory
echo "Preparing SSH directory..."
mkdir -p ~/.ssh

# Add private key from GitLab secure variables
echo "Adding private key..."
mv "$SECURE_FILES_PATH/ci_ssh" ~/.ssh/
chmod 600 ~/.ssh/ci_ssh

# Add remote host to known_hosts
echo "Adding remote host to known_hosts..."
ssh-keyscan -4 -H group2.osnet.h-da.cloud >> ~/.ssh/known_hosts

# Remove key duplicates
echo "Removing duplicate keys in known_hosts..."
sort -u ~/.ssh/known_hosts -o ~/.ssh/known_hosts
