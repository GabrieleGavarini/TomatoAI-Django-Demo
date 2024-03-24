FROM python:3.12

WORKDIR /app

RUN pip install django==5.0.3 \
                djangorestframework==3.15.0