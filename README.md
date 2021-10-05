# README.md 
-----------

![](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen) ![](https://img.shields.io/badge/docker%20build-passing-brightgreen)
### Basic Requirements: {#1}
* Docker version **20.10.8**, build **3967b7d**
* Docker-compose version **1.29.2**
* Git version **2.25.1**

### Installation: {#2}

### Install Using Docker-Compose:


* Clone the latest code from Gitlab Repo: 
> git clone -b main git@gitlab.engro.io:z5x-tech/document-scanner.git
* Change directory:
> cd document-scanner
* Start and Build Docker Container:
> docker-compose -d up --build
* Access the WebApp running at:
    - [localhost:8000/index/](http://127.0.0.1:8000/index/)

### URLRoutes: {#3}

* PanCard Scanning: [localhost:8000/pancard/](http://127.0.0.1:8000/pancard/)

* AdharCard Scanning: [localhost:8000/aadharcard/](http://127.0.0.1:8000/aadhar/)
* VoterID Scanning: [localhost:8000/voterid/](127.0.0.1:8000/voterid)
* Driving License Scanning: [localhost:8000/driver/](127.0.0.1:8000/driver/)
* Bank Statement Analyser: [localhost:8000/bank_id/](http://127.0.0.1:8000/bank_id/)

### API Routes {#4}
* **POST Methods**:
    - **Pancard Api**: 127.0.0.1:8000/api/v1/pancard
    - **AdharCard Api**: 127.0.0.1:8000/api/v1/adhar
    - **VoterID Api**: 127.0.0.1:8000/api/v1/voter
    - **Driving License Api**: 127.0.0.1:8000/api/v1/driver
    - **Bank Api**: 127.0.0.1:8000/api/v1/bank

* **API Documentation and Collection:**
&nbsp;
    &nbsp; &nbsp; &nbsp;[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/5097955-527ef47b-459c-4ac0-a7af-0ada43f956ed?action=collection%2Ffork&collection-url=entityId%3D5097955-527ef47b-459c-4ac0-a7af-0ada43f956ed%26entityType%3Dcollection%26workspaceId%3De200c205-fe52-4da3-8015-3c24fabe9140)

### Installation Without Docker-Compose (Development): {#5}
Steps are for **Ubuntu 20.04 LTS** 
* Clone the latest code from Gitlab Repo: 
> git clone -b main git@gitlab.engro.io:z5x-tech/document-scanner.git
* Change directory:
> cd document-scanner
* Create a Virtual Environment for python **3.8** and install pip3 **v20.0.2**
> python3 -m venv env 
* Activate the environment:
> source env/bin/activate
* Install necessary packages: 
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr libpoppler-cpp-dev mupdf default-jre default-jdk python3-pip build-essential pkg-config python-dev
pip3 install -r requirements.txt
```
* Run the server:
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```



