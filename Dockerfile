FROM ubuntu:18.04
COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# Dev
RUN curl -k -o kubectl "https://amazon-eks.s3.us-west-2.amazonaws.com/1.21.2/2021-07-05/bin/linux/amd64/kubectl"

RUN apt-get install -y software-properties-common ; add-apt-repository -y ppa:deadsnakes/ppa ; apt-get update ; apt-get install -y python3.8 python3.8-distutils

RUN curl -k "https://bootstrap.pypa.io/get-pip.py" -o get-pip.py
RUN python3.8 get-pip.py
RUN python3.8 -m pip install pip --upgrade
RUN python3.8 -m pip install pipenv

WORKDIR /app
RUN pipenv install

# RUN python3.8 -m pip install pipenv
#ENTRYPOINT /app/entrypoint.sh


#docker build -t eddenburrow/apidemo:latest -f Dockerfile .

# eksctl delete cluster --name=my-cluster


# eksctl create cluster --fargate --name my-gate