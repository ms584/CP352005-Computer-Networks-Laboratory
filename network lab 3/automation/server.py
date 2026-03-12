"""
CP352005 Computer Networks Laboratory
Network Lab 3: MIME File Transfer over Router-on-a-Stick
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

import argparse
import json
import mimetypes
import os
import socket
import struct
from pathlib import Path


def recv_exact(conn: socket.socket, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError("socket closed before expected bytes arrived")
        data.extend(chunk)
    return bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=65432)
    parser.add_argument("--save-dir", default="/app/received")
    args = parser.parse_args()

    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((args.host, args.port))
        srv.listen(5)
        print(f"[server] listening on {args.host}:{args.port}", flush=True)

        while True:
            conn, addr = srv.accept()
            with conn:
                print(f"[server] connection from {addr[0]}:{addr[1]}", flush=True)
                header_len = struct.unpack("!I", recv_exact(conn, 4))[0]
                header = json.loads(recv_exact(conn, header_len).decode("utf-8"))
                payload_size = int(header["size"])
                payload = recv_exact(conn, payload_size)

                filename = header.get("filename", "received.bin")
                out_path = save_dir / filename
                out_path.write_bytes(payload)

                guessed_mime, _ = mimetypes.guess_type(out_path.name)
                ack = {
                    "status": "ok",
                    "saved_as": str(out_path),
                    "received_size": len(payload),
                    "declared_mime": header.get("mime_type"),
                    "guessed_mime": guessed_mime,
                }
                conn.sendall(json.dumps(ack).encode("utf-8"))
                print(f"[server] saved {filename} ({payload_size} bytes)", flush=True)
                print(f"[server] header={header}", flush=True)


if __name__ == "__main__":
    main()
