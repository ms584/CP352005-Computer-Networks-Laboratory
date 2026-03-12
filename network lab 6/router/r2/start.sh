#!/bin/sh
set -e

sysctl -w net.ipv4.ip_forward=1

mkdir -p /run/frr /var/log/frr
chown -R frr:frr /run/frr /var/log/frr /etc/frr
/usr/lib/frr/frrinit.sh start

tail -f /dev/null