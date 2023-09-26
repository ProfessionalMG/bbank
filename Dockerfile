# Dockerfile.eslint

# Use an official Node.js runtime as the parent image
FROM node:16

# Set working directory in Docker container
WORKDIR /app

# Copy package.json and package-lock.json for npm install
COPY package*.json ./

# Install ESLint and any other necessary packages
RUN npm install eslint

# Copy the entire project into the container
COPY bbank
