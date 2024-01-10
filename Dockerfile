FROM python:3.12-alpine3.18
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY src/ /code/

WORKDIR /code/src
CMD uvicorn app:app --reload --host 0.0.0.0 --port 8000 --proxy-headers