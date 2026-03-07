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
│   ├── automation/
│   ├── captures/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── README.md
│
├── network lab 4/           # NAT & Stateless/Stateful APIs
│   ├── automation/
│   ├── docker-compose.yml
│   └── README.md
│
├── network lab 5/           # Enterprise Edge & WAN Microservices
│   ├── automation/
│   │   └── start_services.py
│   ├── docker-compose.yml
│   └── README.md
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

## 📖 Academic Integrity Notice

This repository is provided for **learning and reference only**.

Students taking the Computer Networks course must **not copy or submit
this work as their own assignment**.

Doing so may violate academic integrity policies.

---
