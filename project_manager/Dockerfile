FROM python:3.10.8

WORKDIR /project_manager

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .