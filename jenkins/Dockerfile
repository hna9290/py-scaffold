FROM python:3.8-slim
ENV DOCKERVERSION=19.03.8
ENV TERRAFORMVERSION=0.12.29
RUN apt-get update && apt-get install -y curl build-essential wget unzip git
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORMVERSION}/terraform_${TERRAFORMVERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORMVERSION}_linux_amd64.zip \
    && mv terraform /usr/bin \
    && rm terraform_${TERRAFORMVERSION}_linux_amd64.zip
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz\
    && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 -C /usr/local/bin docker/docker \
    && rm docker-${DOCKERVERSION}.tgz
COPY jenkins/requirements.txt /
RUN pip3 install --no-cache-dir -r requirements.txt
