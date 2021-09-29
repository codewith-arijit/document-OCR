# pull the official base image
FROM ubuntu:latest
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
# install dependencies
RUN apt-get update && apt-get install -y tesseract-ocr build-essential libpoppler-cpp-dev pkg-config python-dev mupdf default-jre default-jdk python3-pip  && rm -rf /var/lib/apt/lists/*
#RUN pip3 install virtualenv
#RUN python3 -m virtualenv env
#RUN source env/bin/activate
COPY ./requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt && apt autoremove

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# 
# Command line to activate docker
# docker build --tag django_demo:latest .
# docker run --name django_demo -d -p 8000:8000 django_demo:latest
# ffmpeg libsm6 libxext6  >> Add these in case build or anything else fails