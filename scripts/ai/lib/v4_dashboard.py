"""Standard-library dashboard server for the V4 project-local console."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .v4_core import build_read_model, write_read_model

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
}

def serve(root: Path, host: str, port: int) -> None:
    web_root = root / "scripts" / "ai" / "dashboard"

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:
            return

        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/api/state":
                try:
                    model = build_read_model(root)
                    write_read_model(root, model["project"].get("run_id"))
                    body = json.dumps(model, ensure_ascii=False).encode("utf-8")
                    self._send(200, body, CONTENT_TYPES[".json"])
                except Exception as exc:
                    body = json.dumps(
                        {"error": type(exc).__name__, "message": str(exc)},
                        ensure_ascii=False,
                    ).encode("utf-8")
                    self._send(500, body, CONTENT_TYPES[".json"])
                return

            route = parsed.path
            if route in {"", "/"}:
                route = "/index.html"
            candidate = (web_root / route.lstrip("/")).resolve()
            try:
                candidate.relative_to(web_root.resolve())
            except ValueError:
                self._send(403, b"forbidden", "text/plain; charset=utf-8")
                return
            if not candidate.is_file():
                self._send(404, b"not found", "text/plain; charset=utf-8")
                return
            self._send(
                200,
                candidate.read_bytes(),
                CONTENT_TYPES.get(candidate.suffix, "application/octet-stream"),
            )

    server = ThreadingHTTPServer((host, port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
