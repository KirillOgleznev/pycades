FROM quay.io/pypa/manylinux2014_x86_64

RUN /opt/python/cp37-cp37m/bin/pip install --upgrade twine pip
COPY ./requirements.txt /server/requirements.txt
RUN /opt/python/cp37-cp37m/bin/pip install -r /server/requirements.txt

COPY ./README.md /server/README.md
COPY ./setup.py /server/setup.py
COPY ./pycades /server/pycades

COPY ./libs /tmp
RUN cd tmp/ && linux-amd64_deb/install.sh
RUN cd tmp/ && apt install ./lsb-cprocsp-devel_5.0.12500-6_all.deb
RUN cd tmp/ && apt install ./cprocsp-pki-cades-64_2.0.14589-1_amd64.deb

WORKDIR /server

RUN /opt/python/cp37-cp37m/bin/python ./setup.py bdist_wheel
RUN auditwheel repair dist/*.whl --plat linux_x86_64
RUN /opt/python/cp37-cp37m/bin/pip install wheelhouse/*.whl

COPY ./docker-manylinux/entrypoint.sh /server/entrypoint.sh
COPY ./tests /server/tests

RUN ["chmod", "+x", "/server/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
