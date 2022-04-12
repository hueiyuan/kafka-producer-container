FROM python:3.9-slim

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ADD requirements.txt /project/

RUN mkdir -p /project/.aws/
RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
        build-essential \
        python3-distutils \
        python3-pip \
    && pip3 install --no-cache-dir -r /project/requirements.txt \
    && apt-get remove --auto-remove --purge --yes \
        build-essential \
    && true \
    && apt-get clean --yes \
    && rm -rf \
        /tmp/* \
        /var/log/apt* \
        /var/log/dpkg* \
        /var/lib/apt/lists/* \
        /var/tmp/*

ADD entry.sh /project/
COPY worker/ /project/worker/
WORKDIR /project
ENTRYPOINT ["/project/entry.sh"]
