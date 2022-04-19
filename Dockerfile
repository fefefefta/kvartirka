FROM python:3.8.10-alpine
WORKDIR /usr/src/app
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh .
COPY . /usr/src
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
