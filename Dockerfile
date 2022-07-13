FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN mkdir -p /usr/src/morr

WORKDIR /usr/src/morr

COPY requirements.txt /usr/src/morr/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./conf/uwsgi.ini /etc/uwsgi/uwsgi.ini

COPY ./app /usr/src/morr/app

ENV STATIC_PATH /usr/src/morr/app/static
