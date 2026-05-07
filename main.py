cat > teste_bot.py << 'EOF'
import requests as req

T, C = "8782276108:AAGfrEJi-GQS83hIb30cEojbHl9P_1aHgRA", "@sinais_do_dois_l"

def testar():
    print("\n=== TESTANDO ENVIO DE SINAL DA 2L ===")
    msg = "🚀 *SINAL DE TESTE DIRETO DO iSH!*\n\n🎯 *VELA SIMULADA:* 55.00x\n\nSe você recebeu essa mensagem no canal, a comunicação com o Telegram está 100%!"
    
    url = f"https://api.telegram.org/bot{T}/sendMessage"
    try:
        res = req.post(url, json={"chat_id": C, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        if res.status_code == 200:
            print("[✓] SUCESSO! A mensagem chegou no seu canal do Telegram!")
        else:
            print(f"[X] ERRO DO TELEGRAM: Status {res.status_code}. Verifique se o Bot é administrador do canal.")
            print(res.text)
    except Exception as e:
        print(f"[X] ERRO DE CONEXÃO LOCAL: {e}")

if __name__ == "__main__":
    testar()
EOF
