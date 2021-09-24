# pull the official base image
FROM ubuntu:latest
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev mupdf

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y default-jre
RUN apt-get install -y default-jdk


RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
#RUN pip3 install virtualenv
#RUN python3 -m virtualenv env
#RUN source env/bin/activate
COPY ./requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# 
# Command line to activate docker
# docker build --tag django_demo:latest .
# docker run --name django_demo -d -p 8000:8000 django_demo:latest