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
RUN apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]