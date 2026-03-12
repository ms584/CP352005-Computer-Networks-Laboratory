FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    frr \
    iproute2 \
    iptables \
    iputils-ping \
    procps \
    curl \
    tcpdump \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/zebra=no/zebra=yes/' /etc/frr/daemons && \
    sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

CMD ["bash"]