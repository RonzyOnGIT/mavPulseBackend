# MavPulse Backend

## How to run 

### Creates docker image
`docker build -t backend .`

### Run the container
`docker run --rm backend`

### Different way to run container (No need to build image)
`docker-compose run --rm backend .`

## Debugging
For quick startups for debugging, you can use venv environment for faster debugging

To run venv environment: `source venv/bin/activate`

To stop running: `deactivate`

If you encounter issues with being unable to start up venv environment, is most likely due to
the line ending differences in Windows and Linux

