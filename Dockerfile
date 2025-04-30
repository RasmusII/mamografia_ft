FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /opt/

# Instalar dependencias del sistema necesarias para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requerimientos_django.pip ./

RUN pip install --upgrade pip

RUN pip install -r requerimientos_django.pip

COPY . .

EXPOSE 8000 8003

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]