# Dockerfile

# pull the official docker image
FROM python:3.11.1-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV DIM_DATA_END_DATE=31/12/2030
ENV DIM_DATA_START_DATE=01/01/2010
ENV FILES_PATH=./cdr-files/



# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .