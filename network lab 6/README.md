# Lab 6 — Resilient WAN & Secure Microservice Exposure

**Course:** CP352005 Computer Networks  
**Institution:** Khon Kaen University  

---

## 📖 Overview

This lab extends the SME network architecture built in previous labs by introducing:

*   **WAN Connectivity**
*   **Internet NAT** (Network Address Translation)
*   **Firewall Rules**
*   **Selective Microservice Exposure**
*   **WAN Monitoring**

The environment is simulated using **Docker containers** to represent routers, servers, and clients. The primary goal is to simulate a **secure enterprise network edge** where internal services remain protected while only approved services are exposed to the Internet.

---

## 🏗️ Network Architecture

```text
       [ Internet (10.255.0.0/24) ]
                    |
             [ InternetTester ]
                    |
      [ R1 (Edge Router + NAT + FW) ]
                    |
       [ ISP Network (100.10.10.0/29) ]
                    |
          [ R2 (Internal Router) ]
           /                 \
    [ LAN A ]             [ LAN B ]
 (192.168.10.0/24)     (192.168.20.0/24)
       |                     |
  [ ServerA ]           [ ServerB ]
                             |
                        [ ClientA ]
```

---

## 📦 Infrastructure Components

| Container | Role |
| :--- | :--- |
| **R1** | Edge router with NAT & firewall |
| **R2** | Internal router |
| **ServerA** | Public microservice host |
| **ServerB** | Internal microservice host |
| **ClientA** | Internal client |
| **InternetTester** | Simulated Internet user |

---

## 🚀 Implementation Steps

### 1. Start the Infrastructure
Stop any previous environment and start the new containers.

```bash
# Stop previous environment
docker compose down -v

# Build and start all containers
docker compose up --build -d

# Verify running containers
docker ps
```
**Expected Containers:** `R1`, `R2`, `ServerA`, `ServerB`, `ClientA`, `InternetTester`.

### 2. Start Microservices
Start the Python microservices on both servers in the background.

```bash
docker exec -d ServerA sh -c "python /automation/start_services.py"
docker exec -d ServerB sh -c "python /automation/start_services.py"

# Verify processes
docker exec ServerA ps
docker exec ServerB ps
```

### 3. Verify Service Ports
Ensure that services are listening on the correct ports.

```bash
docker exec ServerA ss -tuln
docker exec ServerB ss -tuln
```
**Expected Ports:**
*   `8000`: Upload Service
*   `8001`: Processing Service
*   `8002`: AI Service
*   `9000`: Gateway Service

### 4. Test Internal Network Connectivity
Verify that LAN A can reach LAN B.

```bash
docker exec -it ClientA ping -c 3 192.168.20.10
```
**Expected Result:** `0% packet loss`.

### 5. Test Internal Service Access
ClientA accesses services on ServerB.

```bash
# Health check
docker exec -it ClientA sh -c "curl -v http://192.168.20.10:8000/health; echo"

# Workflow service
docker exec -it ClientA sh -c "curl -v -X POST http://192.168.20.10:9000/process-file; echo"
```
**Expected Result:** `HTTP/1.0 200 OK`.

### 6. Test Internet Connectivity
Test outbound Internet connectivity from ServerA through NAT.

```bash
docker exec -it ServerA ping -c 3 8.8.8.8
```
**Expected Result:** `0% packet loss`.

### 7. Verify Router Routing Tables
Check routing configurations on both routers.

```bash
# Check R1 routing
docker exec R1 ip route
# Expected: default via 10.255.0.1, 192.168.20.0/24 via 100.10.10.2

# Check R2 routing
docker exec R2 ip route
# Expected: default via 100.10.10.1, 192.168.10.0/24 via 100.10.10.1
```

### 8. Verify NAT Configuration
Inspect NAT rules on R1.

```bash
docker exec R1 iptables -t nat -L -n -v
```
**Expected Rule:** `DNAT` for port 8000 and `MASQUERADE` for outbound traffic.

### 9. Verify Firewall Rules
Inspect the forwarding rules on the edge router.

```bash
docker exec R1 iptables -L FORWARD -n -v
```
**Security Policy Overview:**
*   Allow established connections (return traffic).
*   Allow Internet → ServerA:8000 (public service).
*   Allow LAN outbound traffic.
*   Drop other inbound connections.

### 10. Test Public Service Exposure
Simulate an external user (InternetTester) accessing the services.

```bash
# Allowed service (Should succeed)
docker exec -it InternetTester sh -c "curl -v http://10.255.0.2:8000/health; echo"

# Blocked backend service (Should fail)
docker exec -it InternetTester sh -c "curl -v http://10.255.0.2:9000/process-file; echo"
```
**Expected:** `HTTP/1.0 200 OK` for port 8000; `Connection refused` or timeout for port 9000.

### 11. Verify Connection Tracking
Check NAT connection tracking on R1.

```bash
docker exec R1 cat /proc/net/nf_conntrack | grep 8000
```
**Expected Entry:** Shows source (InternetTester) mapping to destination (ServerA).

### 12. WAN Monitoring
Check the specific route used for WAN monitoring.

```bash
docker exec R1 ip route | grep 8.8.8.8
```
**Expected Result:** `8.8.8.8 via 10.255.0.1`.

---

## 🏁 Final Results

The network successfully demonstrates:
1.  **Internet NAT Connectivity:** Internal hosts can reach the Internet.
2.  **Secure Microservice Exposure:** Only port 8000 is reachable from the outside.
3.  **Firewall Traffic Control:** Traffic is filtered based on security policies.
4.  **Network Segmentation:** LAN A and LAN B are correctly routed.
5.  **WAN Monitoring Capability:** Router can track Internet reachability.

---

## ✍️ Author

* 673380416-3 นายพัทธดนย์ คำนัน โบร์ท 
* 673380428-6 นายสิทธิโชค มุขนาค บูบู้ 
* 673380583-4 นายณัฐภัทร ฉ่ำตะคุ อ้น 
* 673380606-8 นายสรวิศ สุคงเจริญ โอ่ง 
* 673380608-4 นางสาวอมลวรรณ พิมพิชัย เนย
  
**Date:** [03/12/2026]  
**Course:** CP352005 Computer Networks, Khon Kaen University
