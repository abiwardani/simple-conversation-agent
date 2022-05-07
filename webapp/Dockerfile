# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set env variables
ENV API_PORT=6970
ENV API_KEY=efee65b6-76d4-4f92-914a-58844d089fa8

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --threads 50 -b 0.0.0.0:5000 app:app