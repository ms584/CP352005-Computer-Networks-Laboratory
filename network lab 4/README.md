# Network Lab 4: Simulated Internet & Private LANs
## Stateless vs Stateful Services Analysis

This lab demonstrates how multiple LAN networks communicate through routers and a simulated public network (Internet). The environment uses **Docker containers** to emulate routers, clients, servers, and microservices.

### 🎯 Key Focus Areas:
* **Static Routing:** Communication between isolated LAN networks.
* **Network Address Translation (NAT):** Implementing DNAT and MASQUERADE.
* **Service Exposure:** Accessing internal services through a simulated internet.
* **API Architectures:** Comparing **Stateless** vs. **Stateful** service behaviors.

---

## 🌐 Network Topology

```text
                Simulated Internet
                  10.10.12.0/29
                        |
             -------------------------
             |                       |
          Router R1              Router R2
         10.10.12.1              10.10.12.2
             |                       |
           LAN A                   LAN B
       192.168.10.0/24         192.168.20.0/24
         |        |              |        |
      ServerA   ClientA       ServerB   ClientB
    .10.10    .10.50        .20.10    .20.50
```

---

## 🔢 Address Table

| Device | Interface | IP Address | Gateway |
| :--- | :--- | :--- | :--- |
| **R1** | LAN | `192.168.10.1` | - |
| **R1** | Public | `10.10.12.1` | - |
| **R2** | LAN | `192.168.20.1` | - |
| **R2** | Public | `10.10.12.2` | - |
| **ServerA** | eth0 | `192.168.10.10` | `192.168.10.1` |
| **ClientA** | eth0 | `192.168.10.50` | `192.168.10.1` |
| **ServerB** | eth0 | `192.168.20.10` | `192.168.20.1` |
| **ClientB** | eth0 | `192.168.20.50` | `192.168.20.1` |

---

## 🛠 Infrastructure Setup

The entire system is built using **Docker Compose**.

1. **Start the environment:**
   ```bash
   docker compose down -v
   docker compose up --build -d
   ```

2. **Verify running containers:**
   Expected nodes: `r1`, `r2`, `server_a`, `server_b`, `client_a`, `client_b`.

3. **Check Service Logs:**
   The servers run two microservices (Stateless on `:3000` and Stateful on `:3001`).
   ```bash
   docker logs server_a
   docker logs server_b
   ```

---

## 🛣 Routing Configuration

Static routing is manually configured to bridge the two LANs.

* **Router R1:** `192.168.20.0/24` via `10.10.12.2`
* **Router R2:** `192.168.10.0/24` via `10.10.12.1`

**Verification:**
```bash
docker exec R1 ip route
docker exec R2 ip route
```

---

## 🔒 NAT Configuration

Router R2 acts as a gateway, exposing LAN B services to the internet using **DNAT**.

### Port Forwarding (DNAT) Rules:
* `10.10.12.2:3000` → `192.168.20.10:3000`
* `10.10.12.2:3001` → `192.168.20.10:3001`

**Verify iptables rules:**
```bash
docker exec R2 iptables -t nat -L -n -v
```

---

## 🧪 Connectivity & Service Testing

### 1. Basic Connectivity (ICMP)
```bash
# ClientA to ServerB
docker exec ClientA ping -c 4 192.168.20.10
```

### 2. Local Service Testing (Inside LAN A)
**Stateless API:**
```bash
docker exec -it ClientA curl -v http://192.168.10.10:3000/info
```

**Stateful API (Session-based):**
```bash
# Step 1: Create Session
docker exec -it ClientA curl -X POST http://192.168.10.10:3001/session

# Step 2: Use the returned Session-ID to get data
docker exec -it ClientA curl http://192.168.10.10:3001/data -H "Session-ID: <ID_FROM_STEP_1>"
```

### 3. Accessing via Simulated Internet (NAT)
```bash
# Access ServerB (LAN B) from ClientA (LAN A) using R2's Public IP
docker exec -it ClientA curl http://10.10.12.2:3000/info
```

---

## 📊 Stateless vs Stateful Comparison

| Feature | Stateless | Stateful |
| :--- | :--- | :--- |
| **Session Storage** | No | Yes (Server Memory) |
| **Independence** | Each request is unique | Requests are linked |
| **Headers Required** | Standard HTTP | `Session-ID` required |
| **Scalability** | High (Easy to load balance) | Lower (Requires Session Sticky) |
| **Memory Usage** | Minimal | Increases with user count |

---

## 🔄 Packet Flow (DNAT Example)

1. **Request:** `ClientA` → `R1` → `Simulated Internet (10.10.12.2:3000)`
2. **Translation:** `R2` receives packet, applies **DNAT** to rewrite destination to `192.168.20.10:3000`.
3. **Delivery:** Packet reaches `ServerB`.
4. **Response:** `ServerB` replies; `R2` applies **MASQUERADE** to translate source back to `10.10.12.2`.
5. **Completion:** `ClientA` receives the response.

---

## 💡 Engineering Reflection

* **Scalability:** Stateless services are preferred for modern cloud architectures as they handle scaling without worrying about session data synchronization.
* **Security:** NAT/DNAT provides a layer of obfuscation, protecting internal IP schemes from being exposed directly to the public network.
* **Routing:** Proper static or dynamic routing is the backbone of inter-network communication.

---

**Author:** Network Laboratory 4 - CP532005 Computer Networks Practice

673380416-3 นายพัทธดนย์ คำนัน โบร์ท 

673380428-6 นายสิทธิโชค มุขนาค บูบู้ 

673380583-4 นายณัฐภัทร ฉ่ำตะคุ อ้น 

673380606-8 นายสรวิศ สุคงเจริญ โอ่ง 

673380608-4 นางสาวอมลวรรณ พิมพิชัย เนย

---