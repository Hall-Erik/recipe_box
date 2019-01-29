#Grab the python alpine image
FROM ubuntu:18.10

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip gunicorn locales
RUN pip3 install uwsgi
RUN pip3 install --upgrade pip

# Set locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Add our code
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Expose is NOT supported by Heroku
# EXPOSE 5000 		

# Run the image as a non-root user
RUN useradd -m myuser
USER myuser

ENV FLASK_APP run.py

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD flask db upgrade && gunicorn --bind 0.0.0.0:$PORT run:app