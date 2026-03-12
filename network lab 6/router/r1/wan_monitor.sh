#!/bin/sh

while true; do
  if ping -c 1 -W 1 8.8.8.8 >/dev/null 2>&1; then
    ip route replace default via 10.255.0.1
  else
    ip route del default >/dev/null 2>&1 || true
  fi
  sleep 5
done