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
import socket
import struct
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=65432)
    args = parser.parse_args()

    path = Path(args.file)
    data = path.read_bytes()
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    header = {
        "mime_type": mime_type,
        "size": len(data),
        "filename": path.name,
    }
    header_bytes = json.dumps(header).encode("utf-8")
    packet = struct.pack("!I", len(header_bytes)) + header_bytes + data

    with socket.create_connection((args.host, args.port), timeout=10) as sock:
        sock.sendall(packet)
        response = sock.recv(4096)

    print("[client] sent header:")
    print(json.dumps(header, indent=2))
    print("[client] server response:")
    print(response.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
