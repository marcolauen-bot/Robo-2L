import os, time, threading, requests as req
from http.server import BaseHTTPRequestHandler, HTTPServer

T = "8782276108:AAGfrEJi-GQS83hIb30cEojbHl9P_1aHgRA"
C = "@sinais_do_dois_l"
L = []

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"ROBO 2L ATIVO")

def send(m):
    try: req.post(f"https://api.telegram.org/bot{T}/sendMessage", json={"chat_id":C, "text":m, "parse_mode":"Markdown"}, timeout=15)
    except: pass

def monitorar():
    # Testando link alternativo da TipMiner que costuma ser mais aberto
    U = "https://api.tipminer.com/api/v1/history/sortenabet/aviator?limit=20"
    while True:
        try:
            # Adicionei um cabeçalho que simula um navegador real para evitar bloqueios
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json"
            }
            r = req.get(U, headers=headers, timeout=20)
            
            if r.status_code == 200:
                data = r.json().get("data", [])
                for rd in data:
                    v = float(rd.get("multiplier", 0))
                    rid = rd.get("_id") or rd.get("id")
                    
                    if v >= 50.0 and rid not in L:
                        L.append(rid)
                        if len(L) > 100: L.pop(0)
                        msg = f"🚨 *ALERTA DE VELA ROSA*\n\n🎯 *RESULTADO:* {v}x\n⏱ *HORA:* {rd.get('created_at','').split(' ')[-1]}\n\n✅ *LOJA 2L OUTLET*"
                        send(msg)
            
            time.sleep(5) # Diminuí para 5 segundos! Agora ele vai "metralhar" a API
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=lambda: HTTPServer(('0.0.0.0', port), S).serve_forever(), daemon=True).start()
    monitorar()
