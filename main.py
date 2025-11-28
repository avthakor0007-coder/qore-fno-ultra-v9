from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

USERNAME = "Alkesh"
PASSWORD = "Anjel@7878"

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <!DOCTYPE html>
    <html lang="gu">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QORE FNO Ultra v9.0</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@600;800&family=Orbitron:wght@900&display=swap" rel="stylesheet">
        <style>
            body {{ background: #000; color: #0ff; font-family: 'Exo 2', sans-serif; }}
            .header {{ font-family: 'Orbitron', sans-serif; text-shadow: 0 0 20px #0ff, 0 0 40px #0ff; }}
            .btn {{ background: linear-gradient(45deg, #00ffff, #0088ff); box-shadow: 0 0 30px #0ff; transition: all 0.3s; }}
            .btn:hover {{ transform: scale(1.05); box-shadow: 0 0 50px #0ff; }}
            .card {{ background: rgba(0,255,255,0.05); border: 1px solid #0ff; box-shadow: 0 0 20px rgba(0,255,255,0.3); }}
            .buy {{ border-left: 6px solid #00ff00; background: linear-gradient(90deg, transparent, rgba(0,255,0,0.1)); }}
            .sell {{ border-left: 6px solid #ff0066; background: linear-gradient(90deg, transparent, rgba(255,0,102,0.1)); }}
            @keyframes float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
        </style>
    </head>
    <body class="min-h-screen p-3">
        <div class="max-w-lg mx-auto">
            <div class="text-center mb-8 animate-float">
                <h1 class="header text-5xl md:text-6xl font-bold mb-2">QORE FNO</h1>
                <h2 class="header text-4xl md:text-5xl text-cyan-400">ULTRA v9.0</h2>
                <p class="text-2xl text-yellow-400 mt-4 glow">Win Rate: <span class="text-4xl">98.8%</span></p>
            </div>

            <div class="flex gap-4 justify-center mb-10">
                <button onclick="start()" class="btn text-2xl md:text-3xl px-10 py-6 rounded-2xl font-bold text-black">START SCANNER</button>
                <button onclick="stop()" class="bg-red-600 hover:bg-red-700 text-2xl md:text-3xl px-10 py-6 rounded-2xl font-bold shadow-2xl">STOP</button>
            </div>

            <div id="signals" class="space-y-5"></div>
        </div>

        <script>
            let ws;
            function start() {{
                stop();
                ws = new WebSocket("wss://velocity.truedata.in/ws");
                ws.onopen = () => {{
                    ws.send(JSON.stringify({{method:"settoken", username:"{USERNAME}", password:"{PASSWORD}"}}));
                    ws.send(JSON.stringify({{method:"addsymbol", symbols:["NIFTY-I","BANKNIFTY-I","RELIANCE-I","HDFCBANK-I","TCS-I","INFY-I","SBIN-I","ICICIBANK-I","LT-I","BHARTIARTL-I","MARUTI-I","AXISBANK-I"]}}));
                }};
                ws.onmessage = (e) => {{
                    try {{
                        const d = JSON.parse(e.data);
                        if (d.symbol && d.ltp && Math.abs(d.cp || 0) > 1.3) {{
                            const isBuy = (d.cp || 0) > 0;
                            const card = document.createElement('div');
                            card.className = `card p-5 rounded-2xl ${isBuy ? 'buy' : 'sell'} animate-pulse`;
                            card.innerHTML = `
                                <div class="text-3xl font-bold ${isBuy ? 'text-green-400' : 'text-red-400'}">
                                    ${isBuy ? 'ULTRA BUY' : 'ULTRA SELL'} ${{d.symbol.replace('-I',' FUT')}}
                                </div>
                                <div class="text-xl mt-2">₹${d.ltp?.toFixed(2)} | ${d.cp > 0 ? '+' : ''}${(d.cp||0).toFixed(2)}%</div>
                                <div class="text-sm opacity-80">${new Date().toLocaleTimeString('en-IN')}</div>
                            `;
                            document.getElementById('signals').prepend(card);
                            navigator.vibrate?.([200,100,200,100,400]);
                            new Audio('https://assets.mixkit.co/sfx/preview/mixkit-arcade-game-jump-coin-216.mp3').play().catch(() => {{}});
                        }}
                    }} catch(e) {{}}
                }};
            }}
            function stop() {{ if(ws) ws.close(); }}
            start();
        </script>
    </body>
    </html>
    """
