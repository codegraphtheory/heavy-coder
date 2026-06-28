# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash ca-certificates git ffmpeg asciinema procps rsync \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pytest pyyaml

RUN pip install --no-cache-dir asciinema-agg 2>/dev/null || true

RUN useradd -m -s /bin/bash -u 10001 graphtheory

COPY . /home/graphtheory/workspace/heavy-coder
COPY demos/docker/opt /opt/demo

RUN pip install --no-cache-dir -e /home/graphtheory/workspace/heavy-coder \
    && chmod +x /opt/demo/*.sh /opt/demo/bin/*.sh \
    && mkdir -p /home/graphtheory/workspace/heavy-coder/demos/docker/out \
    && chown -R graphtheory:graphtheory /home/graphtheory /opt/demo

USER graphtheory
ENV HOME=/home/graphtheory
ENV USER=graphtheory
ENV LOGNAME=graphtheory
ENV TERM=xterm-256color
ENV COLUMNS=120
ENV LINES=36
WORKDIR /home/graphtheory/workspace/heavy-coder

ENTRYPOINT ["/opt/demo/entrypoint.sh"]
CMD ["/opt/demo/record-asciinema.sh"]