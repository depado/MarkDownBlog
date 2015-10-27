FROM alpine

RUN apk add --update python3 python3-dev
RUN apk add gcc libc-dev

ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
RUN apk del gcc libc-dev python3-dev
RUN rm -rf /var/cache/apk/*

ADD . /app
WORKDIR /app

RUN mkdir /var/log/gunicorn/

EXPOSE 80
ENTRYPOINT ["gunicorn", "app:app", "-c", "/app/gunicorn.py"]
