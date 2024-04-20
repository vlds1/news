FROM python:3.10-slim as back

ENV PYTHONPATH=/st/src

COPY ./src /st/src/
COPY reqs.txt /st

RUN pip3 install -r /st/reqs.txt

WORKDIR /st/src/
