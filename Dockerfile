FROM python:3.10.12-slim

# this is like doing cd app
# any subsequent commands like COPY, CMD, etc will be in /app
WORKDIR /app

# copy requirements.txt into /app (workdir)
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy all files inside app onto current workdir in container
COPY app/ .

CMD ["python3", "-u", "courses.py"]
