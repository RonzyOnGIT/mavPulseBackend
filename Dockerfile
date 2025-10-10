FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

CMD ["python3", "-u", "courses.py"]
