# frontend/Dockerfile

# Use Node 14
FROM node:14

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json /app/

# Install dependencies
RUN npm install

# Copy project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app
CMD ["npm", "run", "serve"]
