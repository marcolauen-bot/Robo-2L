import datetime as dt
import time
import threading
import requests as req
from http.server import BaseHTTPRequestHandler, HTTPServer

T, C = "8782276108:AAGfrEJi-GQS83hIb30cEojbHl9P_1aHgRA", "@sinais_do_dois_l"
L = {"h": None}

# --- PARTE DO SERVIDOR WEB PARA O PLANO GRÁTIS DO RENDER ---
class ServidorSimples(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Robo 2L Ativo!")

def rodar_servidor_web():
    server = HTTPServer(('0.0.0.0', 10000), ServidorSimples)
    server.serve_forever()

# --- MONITOR DAS VELAS ---
def send(m):
    try: 
        req.post(f"https://api.telegram.org/bot{T}/sendMessage", json={"chat_id": C, "text": m, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Erro Telegram: {e}")

def monitorar():
    print("\n=== MONITOR INTELIGENTE ATIVO ===")
    U = "https://api.tipminer.com/api/v1/history/sortenabet/aviator"
    H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    while True:
        try:
            res = req.get(U, headers=H, timeout=20)
            if res.status_code == 200:
                rodadas = res.json().get("data", [])
                for rd in reversed(rodadas[:15]):
                    h = rd.get("created_at", "").split(" ")[-1]
                    v = float(rd.get("multiplier", 0))
                    
                    # Pega qualquer vela a partir de 50x (sem limite máximo de 100x)
                    if v >= 50.0 and L["h"] != h:
                        L["h"] = h
                        
                        # Análise inteligente para sugerir a próxima possível vela
                        if v < 100.0:
                            alvo = "Possível Vela: 50x+"
                        elif 100.0 <= v < 300.0:
                            alvo = "Possível Vela: 100x+"
                        else:
                            alvo = f"Possível Vela Gigante: {int(v // 100) * 100}x+"

                        msg = f"🚨 *VELA GIGANTE DETECTADA!* 🚨\n\n🎯 *VALOR:* {v}x\n⏱ *HORÁRIO:* {h}\n\n📊 *ANÁLISE DE TENDÊNCIA:*\n🚀 *{alvo}*"
                        send(msg)
                        print(f"   [!] SINAL DISPARADO: {v}x às {h} ({alvo})")
            time.sleep(25)
        except Exception as e:
            print(f"Erro na verificação: {e}")
            time.sleep(10)

if __name__ == "__main__":
    t = threading.Thread(target=rodar_servidor_web)
    t.daemon = True
    t.start()
    monitorar()
