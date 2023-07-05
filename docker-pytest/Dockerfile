FROM python:3.11

ADD ./requirements.txt /opt
RUN pip install -r /opt/requirements.txt

#COPY wheelhouse /opt/wheelhouse
#RUN cd opt && pip install wheelhouse/pycades-1.1.0-py3-none-manylinux_2_24_x86_64.whl

#COPY ./libs /tmp
#RUN tmp/linux-amd64_deb/install.sh
#RUN pip install pycades

COPY tests /opt/tests
COPY ./docker-pytest/entrypoint.sh /opt/entrypoint.sh

WORKDIR /opt
RUN ["chmod", "+x", "/opt/entrypoint.sh"]
#ENTRYPOINT ["./entrypoint.sh"]
ENTRYPOINT ["sleep", "infinity"]