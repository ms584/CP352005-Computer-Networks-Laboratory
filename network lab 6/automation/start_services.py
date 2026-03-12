"""
CP352005 Computer Networks Laboratory
Network Lab 6: Resilient WAN & Secure Microservice Exposure
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

SERVICES = {
    8000: "Upload Service",
    8001: "Processing Service",
    8002: "AI Service",
    9000: "Gateway Service"
}

class MicroserviceHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "healthy",
            "service": SERVICES.get(self.server.server_port, "Unknown"),
            "port": self.server.server_port,
            "server_time": time.time()
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            "status": "success",
            "message": "Workflow completed across WAN",
            "service": SERVICES.get(self.server.server_port, "Unknown"),
            "port": self.server.server_port,
            "server_time": time.time()
        }
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        return

def start_server(port, name):
    try:
        handler = MicroserviceHandler
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            print(f"[+] Started {name} on port {port}", flush=True)
            httpd.serve_forever()
    except OSError:
        print(f"[-] Port {port} is already in use", flush=True)

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