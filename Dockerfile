FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/

COPY requerimientos_django.pip ./

RUN pip install --upgrade pip

RUN pip install -r requerimientos_django.pip

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]