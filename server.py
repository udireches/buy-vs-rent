"""Local web UI for the buy vs. rent model.

Run:  python3 server.py   then open http://127.0.0.1:8000
"""

import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from buy_vs_rent import DEFAULTS, simulate

HOST, PORT = "127.0.0.1", 8000
INDEX = Path(__file__).parent / "static" / "index.html"

# key, label, min, max, step, format ("$" or "%")
SLIDERS = [
    ("HOME_PRICE",       "House price",        100_000, 2_000_000, 10_000, "$"),
    ("DOWN_PCT",         "Down payment",       0,       1,         0.01,   "%"),
    ("CLOSING_PCT",      "Closing costs",      0,       0.06,      0.0025, "%"),
    ("MORTGAGE_RATE",    "Mortgage rate",      0.02,    0.12,      0.00125, "%"),
    ("PROPERTY_TAX_PCT", "Property tax",       0,       0.03,      0.0005, "%"),
    ("INSURANCE_PCT",    "Home insurance",     0,       0.015,     0.0005, "%"),
    ("MAINTENANCE_PCT",  "Maintenance",        0,       0.03,      0.001,  "%"),
    ("HOA_MONTHLY",      "HOA / month",        0,       1_000,     25,     "$"),
    ("APPRECIATION",     "Home appreciation",  -0.02,   0.10,      0.0025, "%"),
    ("SELLING_PCT",      "Selling costs",      0,       0.10,      0.005,  "%"),
    ("RENT_MONTHLY",     "Rent / month",       500,     10_000,    50,     "$"),
    ("RENT_GROWTH",      "Rent growth",        -0.02,   0.10,      0.0025, "%"),
    ("RENTERS_INS_MO",   "Renter's insurance / month", 0, 100,     5,      "$"),
    ("INVEST_RETURN",    "Investment return",  0,       0.12,      0.0025, "%"),
]
LIMITS = {k: (lo, hi) for k, _, lo, hi, _, _ in SLIDERS}


def run(query):
    params = {}
    for key, values in parse_qs(query).items():
        if key in LIMITS:
            try:
                v = float(values[0])
            except ValueError:
                continue
            lo, hi = LIMITS[key]
            params[key] = min(max(v, lo), hi)
    pmt, rows = simulate(params)
    names = ("year", "own_cost", "rent_cost", "home_value", "balance",
             "buyer_nw", "renter_nw", "advantage")
    return {"payment": pmt, "rows": [dict(zip(names, r)) for r in rows]}


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype, status=200):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj):
        self._send(json.dumps(obj).encode(), "application/json")

    def do_GET(self):
        url = urlparse(self.path)
        if url.path in ("/", "/index.html"):
            self._send(INDEX.read_bytes(), "text/html; charset=utf-8")
        elif url.path == "/api/defaults":
            self._json({
                "defaults": DEFAULTS,
                "sliders": [dict(key=k, label=l, min=lo, max=hi, step=s, fmt=f)
                            for k, l, lo, hi, s, f in SLIDERS],
            })
        elif url.path == "/api/simulate":
            self._json(run(url.query))
        else:
            self._send(b"Not found", "text/plain", 404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"Buy vs. rent UI running at {url}  (Ctrl+C to stop)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
