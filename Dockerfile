# # Set locale
# RUN locale-gen en_US.UTF-8
# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8

# python runtime
FROM python:3.6.8-alpine

RUN apk update && apk add build-base postgresql-dev libffi-dev

# working directory
WORKDIR /app

# copy current directory into the container
COPY . /app

# install requirements
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

ENV FLASK_APP run.py

EXPOSE 5000
# CMD flask db upgrade && gunicorn --bind 0.0.0.0:5000 run:app
CMD flask db upgrade && gunicorn --bind 0.0.0.0:$PORT run:app