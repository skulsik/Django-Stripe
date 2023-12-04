FROM python:3

WORKDIR /project

COPY ./requirements.txt /project/

RUN pip install -r requirements.txt

COPY . .