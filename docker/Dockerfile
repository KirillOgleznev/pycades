FROM python:3.10
#FROM ubuntu:22.04
ADD ./test_requirements.txt /opt
RUN pip install -r /opt/test_requirements.txt

COPY ./ /tmp/

RUN apt-get update
RUN apt-get install build-essential libboost-all-dev -y
RUN cd tmp/ && linux-amd64_deb/install.sh
RUN cd tmp/ && apt-get install ./lsb-cprocsp-devel_5.0.12500-6_all.deb
RUN cd tmp/ && apt-get install ./cprocsp-pki-cades-64_2.0.14589-1_amd64.deb
RUN apt-get clean

COPY ./docker/entrypoint.sh /opt
COPY tests /opt/tests
RUN cd tmp && python setup.py install

WORKDIR /opt
RUN ["chmod", "+x", "/opt/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
