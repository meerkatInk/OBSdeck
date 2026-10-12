#!/usr/bin/env python3
"""Serves OBS Deck to your Steam Deck (or any device) and keeps the button layout on this PC.

Run it on the PC that runs OBS:   python serve.py   (or double-click start-server.bat)
Then open the address it prints on the Steam Deck.

Only the page itself and its small API are served; nothing else in this folder is exposed.
The OBS password is never sent anywhere by this server.
"""
import argparse
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGE = ROOT / "index.html"
LAYOUT = ROOT / "layout.json"
MAX_BODY = 20 * 1024 * 1024  # layouts with custom images are still far smaller than this


def obs_websocket_config():
    """Reads OBS's own WebSocket settings so the page can pick the right port automatically."""
    bases = []
    if os.environ.get("APPDATA"):
        bases.append(Path(os.environ["APPDATA"]) / "obs-studio")
    bases += [Path.home() / ".config" / "obs-studio", Path.home() / "Library" / "Application Support" / "obs-studio"]
    for base in bases:
        try:
            data = json.loads((base / "plugin_config" / "obs-websocket" / "config.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        return {
            "obsPort": data.get("server_port", 4455),
            "authRequired": bool(data.get("auth_required", True)),
            "enabled": bool(data.get("server_enabled", False)),
        }
    return {}


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is sent; this just picks the LAN interface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


class Handler(BaseHTTPRequestHandler):
    server_version = "OBSDeck/1.0"

    def _send(self, code, body=b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD" and body:
            self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        elif path == "/api/layout":
            try:
                body = LAYOUT.read_bytes()
            except FileNotFoundError:
                body = b"null"
            self._send(200, body)
        elif path == "/api/info":
            self._send(200, json.dumps(obs_websocket_config()).encode())
        else:
            self._send(404, b"Not found", "text/plain")

    do_HEAD = do_GET

    def do_PUT(self):
        if self.path.split("?", 1)[0] != "/api/layout":
            return self._send(404, b"Not found", "text/plain")
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return self._send(413, b'{"error":"layout too large"}')
        try:
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or not isinstance(data.get("pages"), list):
                raise ValueError
        except ValueError:
            return self._send(400, b'{"error":"invalid layout"}')
        tmp = LAYOUT.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, LAYOUT)
        self._send(204)

    def log_message(self, fmt, *args):
        if self.command == "PUT":
            print(f"Layout saved ({self.client_address[0]})")
        elif not self.path.startswith("/api/"):
            print(f"Page opened by {self.client_address[0]}")


def main():
    parser = argparse.ArgumentParser(description="Serve OBS Deck on your local network.")
    parser.add_argument("--port", type=int, default=8080, help="port to serve on (default 8080)")
    args = parser.parse_args()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), Handler)
    url = f"http://{lan_ip()}:{args.port}"
    print("OBS Deck is running.\n")
    print(f"  On the Steam Deck, open:  {url}")
    print(f"  On this PC:               http://localhost:{args.port}\n")
    obs = obs_websocket_config()
    if obs and not obs["enabled"]:
        print("  ! OBS's WebSocket server is off: OBS -> Tools -> WebSocket Server Settings -> Enable.\n")
    print("Keep this window open while you use it. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
