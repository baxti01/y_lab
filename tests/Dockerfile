FROM python:3.10-slim

COPY ./tests tests/

#COPY requirements.txt /tests
COPY ./.env /tests

WORKDIR /tests

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD pytest
