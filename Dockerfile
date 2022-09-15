FROM python:3.6.8-alpine3.8

WORKDIR /2022IThome_env

COPY * .

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--preload"]
