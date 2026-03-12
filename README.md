# 🌐 Computer Networks Laboratory

This repository contains laboratory exercises for the **Computer Networks** course. Each lab simulates real-world network infrastructure using **Docker containers** to emulate routers, servers, and clients in a controlled environment.

Google Drive Link: [CP352005 Network Lab](https://drive.google.com/drive/folders/1h4wsl5imC_2uLLio0ZDTWANK40NS1YOD?usp=sharing)

## 🚀 Key Concepts Covered
* **Network Segmentation:** Creating isolated VLANs and subnets.
* **Routing:** Configuring static routes and inter-VLAN communication.
* **NAT (Network Address Translation):** Implementing DNAT, SNAT, and MASQUERADE.
* **Packet Analysis:** Using Wireshark and `tcpdump` to inspect traffic.
* **Microservices:** Understanding communication in distributed systems.
* **WAN Networking:** Simulating ISP links and enterprise edge architectures.

---

## 📂 Repository Structure

```text
.
├── network lab 3/           # Packet Capture & MIME Transfer
│   ├── automation/          # Scripts for file transfer testing
│   ├── captures/            # .pcap files from packet capturing sessions
│   ├── docker-compose.yml   # Network container configurations
│   ├── Dockerfile           # Images for hosts and clients
│   └── README.md            # Lab 3 specific documentation
│
├── network lab 4/           # NAT & Stateless/Stateful APIs
│   ├── automation/          # API Testing scripts
│   ├── docker-compose.yml   # NAT network topology simulation
│   └── README.md            # Lab 4 specific documentation
│
├── network lab 5/           # Enterprise Edge & WAN Microservices (Part 1)
│   ├── automation/
│   │   └── start_services.py # Microservices orchestration
│   ├── docker-compose.yml   # Multi-segment network topology
│   └── README.md            # Lab 5 specific documentation
│
├── network lab 6/           # Resilient WAN & Secure Microservice Exposure
│   ├── automation/
│   │   └── start_services.py # Service deployment scripts
│   ├── router/              # Router configurations (FRRouting)
│   │   ├── Dockerfile       # Image for router containers
│   │   ├── r1/              # Edge Router (NAT, Firewall, WAN Monitor)
│   │   │   ├── frr.conf
│   │   │   ├── start.sh
│   │   │   └── wan_monitor.sh
│   │   └── r2/              # Internal Router (Inter-VLAN Routing)
│   │       ├── frr.conf
│   │       └── start.sh
│   ├── docker-compose.yml   # Full-scale edge architecture setup
│   └── README.md            # Lab 6 specific documentation
│
└── README.md                # Main Documentation
```

---

## 🧪 Lab Overviews

### 🔹 Lab 3 — Docker Network + Packet Capture
Focuses on the basics of packet movement and application-layer headers.
* **Concepts:** VLAN simulation, IP forwarding, TCP file transfer, MIME type verification.
* **Analysis:** Capture traffic with `tcpdump` and analyze the TCP handshake and payload in **Wireshark**.
* **Tech Stack:** Docker Networking, Python Sockets.

### 🔹 Lab 4 — Simulated Internet + Stateless vs Stateful APIs
Simulates a multi-site network connected via a public "Internet" segment.
* **Concepts:** Static routing, DNAT, and MASQUERADE.
* **APIs:** Comparing **Stateless API** (independent requests) vs **Stateful API** (session-based).
* **Architecture:** `LAN A → Router → Simulated Internet → Router → LAN B`

### 🔹 Lab 5 — Internet Edge + WAN + Distributed Microservices
A complex enterprise-level simulation involving distributed services.
* **Concepts:** Edge routers, ISP WAN links, Gateway API architecture, and NAT overload.
* **Microservices Pipeline:**
    | Port | Service | Description |
    | :--- | :--- | :--- |
    | **8000** | Upload Service | Handles incoming data |
    | **8001** | Processing Service | Internal logic processing |
    | **8002** | AI Service | Inference/AI simulation |
    | **9000** | Gateway Service | API Orchestration |

### 🔹 Lab 6 — Resilient WAN + Secure Microservice Exposure

Enhances the enterprise edge network with resilience and security controls.

- **Concepts:** Dynamic routing (OSPF), WAN health monitoring, firewall ACL policies, controlled service exposure.
- **Security:** Only approved public services are reachable from the Internet while backend microservices remain protected.
- **Architecture:** Internet → Edge Router (NAT + Firewall) → ISP WAN → Internal Router → LAN Microservices
---

## 🛠 Requirements

Before starting, ensure you have the following installed:
* [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
* [Python 3.x](https://www.python.org/)
* [Wireshark](https://www.wireshark.org/)
* [Git](https://git-scm.com/)

---

## 🏃 How to Run the Labs

Each lab operates independently. Navigate to the specific lab directory to begin:

1. **Enter the lab directory:**
   ```bash
   cd "network lab 5"
   ```

2. **Start the environment:**
   ```bash
   docker compose up -d
   ```

3. **Verify status:**
   ```bash
   docker ps
   ```

4. **Shutdown the lab:**
   ```bash
   docker compose down
   ```

---

## 🎓 Learning Outcomes

Upon completion of these labs, you will understand:
1. **Packet Forwarding:** How routers handle traffic between different networks.
2. **NAT Mechanisms:** How private networks access the internet and expose services.
3. **WAN Connectivity:** The role of ISP links in connecting remote branches.
4. **Modern Architectures:** How microservices interact across network boundaries.
5. **Network Troubleshooting:** Using industry-standard tools to diagnose connectivity issues.

---

## 👨‍💻 Author

673380416-3 นายพัทธดนย์ คำนัน โบร์ท 

673380428-6 นายสิทธิโชค มุขนาค บูบู้ 

673380583-4 นายณัฐภัทร ฉ่ำตะคุ อ้น 

673380606-8 นายสรวิศ สุคงเจริญ โอ่ง 

673380608-4 นางสาวอมลวรรณ พิมพิชัย เนย

**Computer Networks Laboratory**  
Department of Computer Science

---

## 📘 Academic Integrity Notice

This repository contains laboratory work developed for the course:

**CP352005 — Computer Networks**  
Khon Kaen University

The content is published **solely for educational reference and learning purposes**.

Students enrolled in this course are **strictly prohibited** from copying, reproducing, redistributing, or submitting this work as their own academic assignment.

Any misuse of this material may constitute **academic misconduct** under university policies.

---
