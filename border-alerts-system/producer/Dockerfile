FROM python:3.10-slim

WORKDIR /producer

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
