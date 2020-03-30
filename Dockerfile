FROM ubuntu:18.04

WORKDIR /home

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . ./

ENTRYPOINT [ "python3" ]

CMD [ "index.py" ]