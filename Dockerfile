FROM python:3.10-slim

COPY ./src /st/src/
COPY reqs.txt /st

RUN pip3 install -r /st/reqs.txt

WORKDIR /st/src/

CMD [ "python3", "app/main.py" ]