# Network Lab 5: Internet Edge + ISP WAN + Distributed Microservices

## 📝 Overview
This lab simulates a complex **enterprise network architecture** using Docker containers to emulate network devices and servers. The topology extends Lab 4 by introducing an Internet Edge architecture, ISP WAN simulation, and distributed microservices.

The goal is to demonstrate how **distributed microservices communicate across WAN networks** while managing routing, NAT, and network segmentation similar to real-world enterprise environments.

---

## 🎯 Lab Objectives
* Simulate **Internet Edge Architecture**.
* Implement **ISP WAN connectivity**.
* Deploy and orchestrate **distributed microservices**.
* Test **cross-site service communication** (LAN-to-LAN via WAN).
* Verify **NAT (Network Address Translation)** and routing behavior.
* Demonstrate **enterprise network segmentation**.

---

## 🌐 Network Topology

```text
       [ Internet ]
            |
         (DHCP)
            |
    [ R1 (Edge Router) ] --- (10.255.0.2)
            |
      [ ISP WAN Link ]  --- (100.10.10.0/29)
            |
    [ R2 (Branch Router) ]
            |
    ---------------------------------
    |                               |
 [ LAN A ]                      [ LAN B ]
(192.168.10.0/24)              (192.168.20.0/24)
    |                               |
 [ ServerA ]                    [ ServerB ]
 [ ClientA ]                    [ ClientB ]
```

---

## 🛠 Device & Addressing Scheme

### Network Devices Role
| Device | Role |
| :--- | :--- |
| **R1** | Internet Edge Router + NAT Gateway |
| **R2** | Branch Router |
| **ServerA** | Microservices Stack A |
| **ServerB** | Microservices Stack B |
| **ClientA** | Testing Client |

### Address Table
| Device | Interface | IP Address | Role |
| :--- | :--- | :--- | :--- |
| **R1** | eth0 | `10.255.0.2` | Internet (External) |
| **R1** | eth1 | `100.10.10.1` | ISP WAN |
| **R1** | eth2 | `192.168.10.1` | LAN A Gateway |
| **R2** | eth0 | `100.10.10.2` | WAN |
| **R2** | eth1 | `192.168.20.1` | LAN B Gateway |
| **ServerA** | eth0 | `192.168.10.10` | Microservices Stack |
| **ServerB** | eth0 | `192.168.20.10` | Microservices Stack |
| **ClientA** | eth0 | `192.168.10.50` | Client |

---

## 🚀 Infrastructure Deployment

### 1. Start the Containers
```bash
docker compose down -v
docker compose up -d
```

### 2. Verify Container Status
```bash
docker ps
```
*Expected: R1, R2, ServerA, ServerB, ClientA, ClientB should all be "Up".*

---

## 📦 Microservices Deployment

### 1. Start Microservices on Servers
```bash
docker exec -d ServerA sh -c "python /automation/start_services.py"
docker exec -d ServerB sh -c "python /automation/start_services.py"
```

### 2. Verify Microservice Ports
```bash
docker exec ServerA ss -tuln
```
**Service Mapping:**
| Port | Service | Description |
| :--- | :--- | :--- |
| **8000** | Upload Service | Handles file uploads |
| **8001** | Processing Service | Data processing logic |
| **8002** | AI Service | AI/Inference tasks |
| **9000** | Gateway Service | API Gateway & Orchestrator |

---

## 🧪 Testing & Verification

### 1. Inter-LAN Connectivity
Verify if ClientA (LAN A) can reach ServerB (LAN B) via the WAN:
```bash
docker exec -it ClientA ping -c 3 192.168.20.10
```
*Path: ClientA → R1 → ISP WAN → R2 → ServerB*

### 2. Cross-Site Microservice Health Check
Test access to a service on a different site:
```bash
docker exec -it ClientA curl http://192.168.20.10:8000/health
```

### 3. API Gateway Workflow Test
Test the full orchestration via the Gateway:
```bash
curl -X POST http://192.168.20.10:9000/process-file
```

### 4. Internet & NAT Verification
Verify that internal servers can reach the internet:
```bash
docker exec -it ServerA ping -c 3 8.8.8.8
```

**Check NAT rules on R1:**
```bash
docker exec R1 iptables -t nat -L -n
```

**Check active NAT translations:**
```bash
docker exec R1 cat /proc/net/nf_conntrack | grep 8.8.8.8
```

---

## 🛣 Routing Table Verification

### Router R1 (Edge)
* **Default Route:** `0.0.0.0/0 via 10.255.0.1` (Internet)
* **Static Route:** `192.168.20.0/24 via 100.10.10.2` (To Branch)

### Router R2 (Branch)
* **Default Route:** `0.0.0.0/0 via 100.10.10.1` (To Edge)
* **Static Route:** `192.168.10.0/24 via 100.10.10.1` (To HQ/LAN A)

---

## 📊 Architecture Significance

| Concept | Implementation in Lab |
| :--- | :--- |
| **Enterprise Edge** | R1 acts as the security and routing boundary. |
| **WAN Connectivity** | Simulation of 100.10.10.0/29 as a leased line/ISP link. |
| **Distributed Services** | Services are spread across different geographical/logical sites. |
| **NAT Overload** | R1 hides internal IPs (192.168.x.x) from the Internet. |
| **Orchestration** | Gateway API (Port 9000) manages service-to-service calls. |

---

## 🏁 Conclusion
This lab successfully demonstrates a **modern distributed architecture**. Key takeaways include the implementation of a functional ISP WAN link, the use of an Internet Edge router for NAT, and the ability for microservices to maintain connectivity and functionality across a segmented enterprise network.

---
**Author:** CP532005 Computer Networks Laboratory
*Lab 5 – Internet Edge + Distributed Microservices*

673380416-3 นายพัทธดนย์ คำนัน โบร์ท 

673380428-6 นายสิทธิโชค มุขนาค บูบู้ 

673380583-4 นายณัฐภัทร ฉ่ำตะคุ อ้น 

673380606-8 นายสรวิศ สุคงเจริญ โอ่ง 

673380608-4 นางสาวอมลวรรณ พิมพิชัย เนย

---