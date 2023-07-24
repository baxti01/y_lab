FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . app/

WORKDIR app/

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD alembic upgrade head && python3 main.py