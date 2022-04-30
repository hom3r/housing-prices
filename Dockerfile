FROM python:3.9.12-slim

WORKDIR /app

# install dependencies for nginx
RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential \
    && apt-get -y install libpcre3 libpcre3-dev

# install python packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy files into the container
COPY . .

# copy Docker specific files
COPY .docker/start.sh .
COPY .docker/uwsgi.ini .
COPY .docker/wsgi.py .
COPY .docker/nginx.conf /etc/nginx

# install the local modules
RUN pip install -e .

# unpack the prediction model
RUN tar -zxvf data/model.tgz --directory data

# set start script to be executable
RUN chmod +x ./start.sh

CMD ["./start.sh"]
