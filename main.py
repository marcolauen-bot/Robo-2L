import datetime as dt
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
        self.wfile.write(b"Robo 2L Online e Rápido!")

def rodar_servidor_web():
    server = HTTPServer(('0.0.0.0', 10000), ServidorSimples)
    server.serve_forever()

def send(m):
    try:
        url = f"https://api.telegram.org/bot{T}/sendMessage"
        payload = {"chat_id": C, "text": m, "parse_mode": "Markdown"}
        req.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Erro Telegram: {e}")

def monitorar():
    print("\n=== MONITOR TURBO ATIVO: VARRENDO O GRÁFICO ===")
    U = "https://api.tipminer.com/api/v1/history/sortenabet/aviator"
    H = {"User-Agent": "Mozilla/5.0"}

    while True:
        try:
            res = req.get(U, headers=H, timeout=20)
            if res.status_code == 200:
                rodadas = res.json().get("data", [])
                # Aumentamos para olhar as últimas 25 rodadas para não perder o delay da API
                for rd in reversed(rodadas[:25]):
                    h = rd.get("created_at", "").split(" ")[-1]
                    v = float(rd.get("multiplier", 0))
                    
                    if v >= 50.0 and L["h"] != h:
                        L["h"] = h
                        
                        if v < 100.0:
                            alvo = "Possível Vela: 50x+"
                        elif 100.0 <= v < 300.0:
                            alvo = "Possível Vela: 100x+"
                        else:
                            alvo = f"Possível Vela Gigante: {int(v // 100) * 100}x+"

                        msg = f"🚨 *VELA GIGANTE DETECTADA!*\n\n🎯 *RESULTADO:* {v}x\n⏱ *HORÁRIO:* {h}\n\n📊 *TENDÊNCIA:* {alvo}"
                        send(msg)
                        print(f"[!] SINAL ENVIADO: {v}x às {h}")
            
            # Reduzimos o tempo de espera para 15 segundos (Mais rápido!)
            time.sleep(15)
        except Exception as e:
            print(f"Erro na verificacao: {e}")
            time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=rodar_servidor_web)
    t.daemon = True
    t.start()
    monitorar()
