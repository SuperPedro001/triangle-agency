#!/usr/bin/env python3
"""Triangle Agency Backend API — simple key-value store"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os

DATA_DIR = "/var/www/triangle-agency/data"
os.makedirs(DATA_DIR, exist_ok=True)

def load(name):
    p = os.path.join(DATA_DIR, name + ".json")
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save(name, data):
    p = os.path.join(DATA_DIR, name + ".json")
    t = p + ".tmp"
    with open(t, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(t, p)

class H(BaseHTTPRequestHandler):
    def log_message(self, f, *a): pass
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()
    def _reply(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    def do_GET(self):
        p = self.path.rstrip("/")
        name = p.replace("/api/", "")
        data = load(name)
        if data is not None:
            self._reply(200, data)
        elif name == "status":
            self._reply(200, {"ok": True})
        else:
            self._reply(404, {"error": "not found"})
    def do_POST(self):
        p = self.path.rstrip("/")
        name = p.replace("/api/", "")
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        save(name, body)
        self._reply(200, {"ok": True})

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 3000), H).serve_forever()
