"""
CP352005 Computer Networks Laboratory
Lab 3 
Author: นายพัทธดนย์ คำนัน โบร์ท
Student ID: 673380416-3
Author: นายสิทธิโชค มุขนาค บูบู้ 
Student ID: 673380428-6 
Author: นายณัฐภัทร ฉ่ำตะคุ อ้น 
Student ID: 673380583-4 
Author: นายสรวิศ สุคงเจริญ โอ่ง 
Student ID: 673380606-8 
Author: นางสาวอมลวรรณ พิมพิชัย เนย
Student ID: 673380608-4 

Academic Use Only
"""

import http.server
import socketserver
import threading
import json
import time
import uuid

SERVICES = {
    3000: "Stateless API",
    3001: "Stateful API"
}

SESSIONS = {}

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class MicroserviceHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        port = self.server.server_address[1]
        service = SERVICES.get(port, "Unknown")

        if self.path == "/info":
            self._send_json(200, {
                "status": "healthy",
                "service": service,
                "port": port,
                "server_time": time.time()
            })
            return

        if port == 3001 and self.path == "/data":
            session_id = self.headers.get("Session-ID")
            if not session_id:
                self._send_json(400, {
                    "status": "error",
                    "message": "Missing Session-ID header"
                })
                return

            session = SESSIONS.get(session_id)
            if not session:
                self._send_json(404, {
                    "status": "error",
                    "message": "Invalid or expired session"
                })
                return

            self._send_json(200, {
                "status": "success",
                "service": service,
                "session_id": session_id,
                "session_data": session
            })
            return

        self._send_json(404, {
            "status": "error",
            "message": "Not found"
        })

    def do_POST(self):
        port = self.server.server_address[1]
        service = SERVICES.get(port, "Unknown")

        if port == 3001 and self.path == "/session":
            session_id = str(uuid.uuid4())
            SESSIONS[session_id] = {
                "created_at": time.time(),
                "client_ip": self.client_address[0],
                "service": service
            }
            self._send_json(200, {
                "status": "success",
                "message": "Session created",
                "service": service,
                "session_id": session_id
            })
            return

        if port == 3000:
            self._send_json(200, {
                "status": "success",
                "message": "Stateless endpoint does not store session",
                "service": service
            })
            return

        self._send_json(404, {
            "status": "error",
            "message": "Not found"
        })

    def log_message(self, format, *args):
        return

def start_server(port, name):
    try:
        with ReusableTCPServer(("0.0.0.0", port), MicroserviceHandler) as httpd:
            print(f"[+] Started {name} on port {port}", flush=True)
            httpd.serve_forever()
    except OSError as e:
        print(f"[-] Failed to start {name} on port {port}: {e}", flush=True)

print("--- Starting Microservices ---", flush=True)
threads = []

for port, name in SERVICES.items():
    t = threading.Thread(target=start_server, args=(port, name), daemon=True)
    t.start()
    threads.append(t)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping services...", flush=True)