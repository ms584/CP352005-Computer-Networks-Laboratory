#!/bin/sh
set -e

sysctl -w net.ipv4.ip_forward=1

IF_INET=$(ip -o -4 addr | awk '/10\.255\.0\.2\/24/ {print $2}')
IF_ISP=$(ip -o -4 addr | awk '/100\.10\.10\.1\/29/ {print $2}')
IF_LAN=$(ip -o -4 addr | awk '/192\.168\.10\.1\/24/ {print $2}')

sleep 2

# Default route to Internet
ip route replace default via 10.255.0.1 dev "$IF_INET"

# Keep host route for monitor
ip route replace 8.8.8.8 via 10.255.0.1 dev "$IF_INET"

# Clean old rules
iptables -F
iptables -t nat -F

# Policies
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

# NAT overload for outbound Internet access
iptables -t nat -A POSTROUTING -o "$IF_INET" -j MASQUERADE

# Expose only ServerA:8000 to Internet
iptables -t nat -A PREROUTING -i "$IF_INET" -p tcp --dport 8000 \
  -j DNAT --to-destination 192.168.10.10:8000

# Critical: SNAT the inbound-DNAT flow toward ServerA
iptables -t nat -A POSTROUTING -o "$IF_LAN" -p tcp -d 192.168.10.10 --dport 8000 \
  -j MASQUERADE

# Allow established traffic first
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Internet -> ServerA:8000 allowed
iptables -A FORWARD -i "$IF_INET" -o "$IF_LAN" -p tcp -d 192.168.10.10 --dport 8000 -j ACCEPT

# LAN A -> Internet allowed
iptables -A FORWARD -i "$IF_LAN" -o "$IF_INET" -s 192.168.10.0/24 -j ACCEPT

# LAN A -> WAN -> LAN B allowed
iptables -A FORWARD -i "$IF_LAN" -o "$IF_ISP" -s 192.168.10.0/24 -d 192.168.20.0/24 -j ACCEPT

# WAN -> LAN A only from LAN B allowed
iptables -A FORWARD -i "$IF_ISP" -o "$IF_LAN" -s 192.168.20.0/24 -d 192.168.10.0/24 -j ACCEPT

# Block any other Internet inbound to LAN A
iptables -A FORWARD -i "$IF_INET" -o "$IF_LAN" -j DROP

# Block any other WAN inbound to LAN A
iptables -A FORWARD -i "$IF_ISP" -o "$IF_LAN" -j DROP

# Start FRR
mkdir -p /run/frr /var/log/frr
chown -R frr:frr /run/frr /var/log/frr /etc/frr
/usr/lib/frr/frrinit.sh start

# Start WAN monitor
/bin/sh /wan_monitor.sh &

tail -f /dev/null