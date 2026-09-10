FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "migrate", "&&", "python", "manage.py", "collectstatic", "--noinput", "&&", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]