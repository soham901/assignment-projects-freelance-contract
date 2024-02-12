FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


CMD "prefect server start && python3 main.py"

EXPOSE 4200
