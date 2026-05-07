import os
import time
import threading
import requests as req
from http.server import BaseHTTPRequestHandler, HTTPServer

# CONFIGURAÇÕES
T = "8782276108:AAGfrEJi-GQS83hIb30cEojbHl9P_1aHgRA"
C = "@sinais_do_dois_l"
# Aqui guardamos os IDs das últimas velas para não repetir
L = []

class ServidorSimples(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot 2L - Monitorando 24h")

def rodar_servidor_web():
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
    print("=== MONITOR TURBO 2L ATIVADO ===")
    U = "https://api.tipminer.com/api/v1/history/sortenabet/aviator"
    
    while True:
        try:
            res = req.get(U, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
            if res.status_code == 200:
                rodadas = res.json().get("data", [])
                
                for rd in rodadas[:10]: # Olhamos as 10 mais recentes
                    v = float(rd.get("multiplier", 0))
                    # Usamos o ID único da rodada em vez da hora para não ter erro
                    id_rodada = rd.get("_id") or rd.get("id") or rd.get("created_at")
                    
                    if v >= 50.0 and id_rodada not in L:
                        L.append(id_rodada)
                        # Mantém a lista limpa
                        if len(L) > 50: L.pop(0)
                        
                        msg = f"🚨 *VELA GIGANTE DETECTADA!*\n\n🎯 *RESULTADO:* {v}x\n⏱ *HORÁRIO:* {rd.get('created_at', '').split(' ')[-1]}\n\n✅ *A 2L OUTLET AVISOU!*"
                        send(msg)
                        print(f"Sinal enviado: {v}x")
            
            time.sleep(10) # Checa a cada 10 segundos agora!
        except:
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=rodar_servidor_web, daemon=True).start()
    monitorar()
