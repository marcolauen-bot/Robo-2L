import os
import time
import threading
import requests as req
from http.server import BaseHTTPRequestHandler, HTTPServer

# CONFIGURAÇÕES
T = "8782276108:AAGfrEJi-GQS83hIb30cEojbHl9P_1aHgRA"
C = "@sinais_do_dois_l"
L = {"h": None}

class ServidorSimples(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot 2L Online")

def rodar_servidor_web():
    # Pega a porta que o Render mandar ou usa 10000 por padrao
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), ServidorSimples)
    server.serve_forever()

def send(m):
    try:
        url = f"https://api.telegram.org/bot{T}/sendMessage"
        payload = {"chat_id": C, "text": m, "parse_mode": "Markdown"}
        req.post(url, json=payload, timeout=10)
    except:
        pass

def monitorar():
    print("=== MONITOR INICIADO ===")
    U = "https://api.tipminer.com/api/v1/history/sortenabet/aviator"
    while True:
        try:
            res = req.get(U, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            if res.status_code == 200:
                rodadas = res.json().get("data", [])
                for rd in reversed(rodadas[:25]):
                    h = rd.get("created_at", "").split(" ")[-1]
                    v = float(rd.get("multiplier", 0))
                    if v >= 50.0 and L["h"] != h:
                        L["h"] = h
                        msg = f"🚨 *VELA GIGANTE!*\n\n🎯 *RESULTADO:* {v}x\n⏱ *HORÁRIO:* {h}"
                        send(msg)
            time.sleep(15)
        except:
            time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=rodar_servidor_web, daemon=True).start()
    monitorar()
