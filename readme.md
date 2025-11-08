# MavPulse Backend

## How to run 

### Creates docker image
`docker build -t backend .`

### Run the container
`docker run --rm backend`

### Different way to run container (No need to build image)
`docker-compose run --rm backend .`

## Debugging
you can also use venv environment

### 1. Create virtual environment:
`python3 -m venv venv`

### 2. Activate virtual environment:
`source venv/bin/activate`

### Linux
Some Python packages (like `psycopg2-binary`) require system dependencies on Linux.: `sudo apt install libpq-dev python3-dev build-essential`

### 3. Install project dependencies:
`pip install -r requirements.txt`

### 4. To stop virtual environment:
`deactivate`

