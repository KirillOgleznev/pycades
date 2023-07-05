FROM python:3.11

COPY ./requirements.txt /server/requirements.txt
RUN pip install -r /server/requirements.txt

COPY ./setup.py /server/setup.py
COPY ./pycades /server/pycades
COPY ./README.md /server/README.md

COPY ./libs /tmp
RUN cd tmp/ && linux-amd64_deb/install.sh
RUN cd tmp/ && apt install ./lsb-cprocsp-devel_5.0.12500-6_all.deb
RUN cd tmp/ && apt install ./cprocsp-pki-cades-64_2.0.14589-1_amd64.deb

COPY ./docker/entrypoint.sh /server/entrypoint.sh
COPY ./tests /server/tests

WORKDIR /server

RUN ["chmod", "+x", "/server/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]

