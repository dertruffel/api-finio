FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN apt-get update

RUN apt-get install  \
    ca-certificates gcc g++ libpq-dev musl-dev \
    libffi-dev curl cargo git -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD . /code/

CMD gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --log-file - --bind 0.0.0.0:8070 --chdir src