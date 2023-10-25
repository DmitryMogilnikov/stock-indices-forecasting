FROM python:3.10-slim
WORKDIR backend

COPY requirements/requirements.txt /backend
RUN pip install -r requirements.txt
COPY src /backend
COPY environments /backend/environments