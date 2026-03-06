# Network Lab 3: MIME File Transfer over Router-on-a-Stick

## Overview
This lab simulates inter-VLAN routing and application-level file transfer using a custom MIME-based protocol. The environment is built with **Docker containers** to emulate a router, client, server, and packet sniffer.

The objective is to observe how data travels through the network stack from **ARP → IP → TCP → Application (MIME)** and analyze the packets using **Wireshark**.

---

## 🎯 Lab Objectives
After completing this lab, you will be able to:
* Configure inter-VLAN communication (**Router-on-a-Stick** concept).
* Deploy a MIME-based file transfer client/server.
* Capture and analyze packets using **Wireshark**.
* Identify **ARP resolution** and **TCP handshake**.
* Inspect application-layer metadata inside TCP streams.

---

## 🌐 Network Topology

```text
      PC1 (Client) VLAN10
         192.168.10.10
               |
               |
            Router
         192.168.10.1
         192.168.20.1
               |
               |
      PC2 (Server) VLAN20
         192.168.20.20
```

**Docker containers:**
* `lab3-client`
* `lab3-router`
* `lab3-server`
* `lab3-sniffer`

---

## 🔢 Addressing Scheme

| Device | Interface | IP Address |
| :--- | :--- | :--- |
| **Router** | VLAN10 | `192.168.10.1` |
| **Router** | VLAN20 | `192.168.20.1` |
| **Client** | eth0 | `192.168.10.10` |
| **Server** | eth0 | `192.168.20.20` |

---

## 📂 Project Structure

```text
network-lab3
│
├── automation
│   ├── client.py
│   ├── server.py
│   ├── sample.png
│   └── received/
│
├── captures
│   └── lab3.pcap
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🛠 Requirements
* Docker & Docker Compose
* Wireshark
* Python 3

---

## 🚀 Starting the Lab

1. **Build and start the containers:**
   ```bash
   docker compose up --build -d
   ```

2. **Verify running containers:**
   ```bash
   docker ps
   ```
   *Expected containers: `lab3-router`, `lab3-client`, `lab3-server`, `lab3-sniffer`*

---

## 🧹 Clear ARP Cache
To force new ARP resolution during capture, run:
```bash
docker exec lab3-client ip neigh flush all
docker exec lab3-server ip neigh flush all
docker exec lab3-router ip neigh flush all
```

---

## 🧪 Connectivity Test
Verify routing between VLANs:
```bash
docker exec -it lab3-client ping -c 10 192.168.20.20
```
*Expected result: 0% packet loss.*

---

## 🔍 Start Packet Capture

1. **Access the router shell:**
   ```bash
   docker exec -it lab3-router sh
   ```

2. **Start `tcpdump`:**
   ```bash
   tcpdump -i any -w /tmp/lab3.pcap arp or tcp port 65432
   ```
   *This captures ARP packets and TCP packets on port 65432.*

---

## 📈 Generate Traffic

### 1. Generate ARP Traffic
```bash
docker exec -it lab3-client ping -c 1 192.168.20.20
```

### 2. Send MIME File
Transfer the file from client to server:
```bash
docker exec -it lab3-client sh -c \
"python /app/client.py /app/sample.png --host 192.168.20.20 --port 65432"
```

**Example output:**
```json
[client] sent header:
{
 "mime_type": "image/png",
 "size": 156,
 "filename": "sample.png"
}

[client] server response:
{
 "status": "ok",
 "saved_as": "/app/received/sample.png",
 "received_size": 156
}
```

---

## 💾 Stop & Export Capture
1. Stop `tcpdump` with `CTRL + C` inside the router container.
2. **Copy the capture file to your host:**
   ```bash
   docker cp lab3-router:/tmp/lab3.pcap .
   ```

---

## 🔬 Analyze with Wireshark
Open `lab3.pcap` in Wireshark.

### Useful Filters:
* **ARP packets:** `arp`
* **TCP handshake:** `tcp.port == 65432` (Look for SYN, SYN-ACK, ACK)
* **Data packets:** `tcp.len > 0`

### Inspect MIME Metadata:
Right-click on a TCP packet and select **Follow → TCP Stream**. You will see:
1. The JSON header (Metadata).
2. The binary payload (Image data).

---

## 📝 MIME Protocol Format
The custom protocol structure used in this lab:
1. **[4 bytes]**: Header length.
2. **[JSON header]**: Contains `mime_type`, `size`, and `filename`.
3. **[Binary payload]**: The actual file data.

---

## 🔄 Packet Flow Summary
1. **ARP Request/Reply**: To find MAC addresses.
2. **TCP Three-Way Handshake**: To establish connection.
3. **Data Transfer**: JSON MIME header + File payload.
4. **Server Response**: Confirmation.
5. **TCP Connection Termination**: FIN/ACK.

---

## 🎓 Learning Outcome
This lab demonstrates how application-level data is encapsulated across the network stack:
**Application (MIME) → TCP → IP → Ethernet**

By analyzing packets, we observe how network protocols cooperate to deliver data reliably across different network segments.

---

**Author:** Network Lab 3 - CP532005 Computer Networking Practice

673380416-3 นายพัทธดนย์ คำนัน โบร์ท 

673380428-6 นายสิทธิโชค มุขนาค บูบู้ 

673380432-5 นายอาณัฐ อารีย์ รักบี้

673380583-4 นายณัฐภัทร ฉ่ำตะคุ อ้น 

673380606-8 นายสรวิศ สุคงเจริญ โอ่ง 

673380608-4 นางสาวอมลวรรณ พิมพิชัย เนย

---