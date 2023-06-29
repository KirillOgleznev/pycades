FROM python:3.11

COPY ./test_requirements.txt /server/test_requirements.txt
RUN pip install -r /server/test_requirements.txt

COPY ./setup.py /server/setup.py
COPY ./pycades /server/pycades
COPY ./README.md /server/README.md

COPY ./libs /tmp
RUN cd tmp/ && linux-amd64_deb/install.sh
RUN cd tmp/ && apt install ./lsb-cprocsp-devel_5.0.12500-6_all.deb
RUN cd tmp/ && apt install ./cprocsp-pki-cades-64_2.0.14589-1_amd64.deb

WORKDIR /server

RUN python ./setup.py bdist_wheel
RUN auditwheel repair dist/*.whl --plat linux_x86_64
RUN pip install wheelhouse/*.whl

COPY ./docker/entrypoint.sh /server/entrypoint.sh
COPY ./tests /server/tests

RUN ["chmod", "+x", "/server/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
