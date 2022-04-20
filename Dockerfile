FROM python:3.10-alpine

ENV DATABASE_URL ""
ENV RUN_ENV PRODUCTION

WORKDIR /src

# Required for alpine image
RUN apk update \
    && apk add --virtual build-essential gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY . /src

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]