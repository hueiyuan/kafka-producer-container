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
COPY example_producer/ /project/example_producer/
COPY project_configs/ /project/example_producer/project_configs/
COPY project_libs/ /project/example_producer/project_libs/
COPY helpers/ /project/example_producer/helpers/
WORKDIR /project
ENTRYPOINT ["/project/entry.sh"]
