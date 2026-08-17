# Hello World Docker Project

This is a simple Flask application deployed using Docker.

## Project Overview

This project demonstrates how to create a Dockerized Flask application that responds with "Hello, World!" when accessed via a web browser. The application is packaged as a Docker image for easy deployment and distribution.

## Prerequisites

- Docker: Make sure you have Docker installed on your system.

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/YourUsername/My-Portfolio.git
   cd My-Portfolio/hello-world-docker
   ```

2. **Build the Docker Image:**

Build the Docker image using the provided Dockerfile.

```bash
docker build -t hello-world-docker .
```

3. **Run the Docker Container:**

Run the Docker container from the built image.

```bash 
docker run -p 8080:8080 hello-world-docker
```

4. **Access the Application:**

Open your web browser and navigate to http://localhost:8080 to see the "Hello, World!" response from the Flask application.

## Directory Structure

* **'app.py'**: The Flask application code.
* **'requirements.txt'**: List of Python packages required for the application.
* **'Dockerfile'**: Instructions to build the Docker image.
* **'README.md'**: Project documentation.