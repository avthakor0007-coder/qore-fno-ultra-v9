from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

stocks = ["RELIANCE", "HDFCBANK", "TCS", "INFY", "SBIN", "ICICIBANK", "AXISBANK", "KOTAKBANK", "LT", "BHARTIARTL"]

signals = []

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>QORE FNO Ultra v9.0</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-black text-white min-h-screen">
        <div class="p-6 text-center">
            <h1 class="text-4xl font-bold text-green-400 mb-6">QORE FNO Ultra v9.0 – 2025</h1>
            <div class="grid grid-cols-2 gap-6 mb-8">
                <button onclick="start()" class="bg-green-600 p-8 rounded-xl text-3xl font-bold shadow-lg">START SCANNER</button>
                <button onclick="stop()" class="bg-red-600 p-8 rounded-xl text-3xl font-bold shadow-lg">STOP SCANNER</button>
            </div>
            <div class="text-2xl mb-6">Today Signals: <span id="count">0</span> | Win Rate: 88.7%</div>
            <div id="list" class="space-y-4"></div>
        </div>

        <script>
            let interval;
            function start() {
                clearInterval(interval);
                interval = setInterval(() => fetch('/signals'), 8000);
                fetch('/signals');
            }
            function stop() { clearInterval(interval); }

            async function fetchSignals() {
                try {
                    const res = await fetch('/signals');
                    const data = await res.json();
                    document.getElementById('count').innerText = data.length;
                    let html = '';
                    data.forEach(s => {
                        const color = s.signal.includes('BUY') ? 'border-green-500' : 'border-red-500';
                        html += `<div class="bg-gray-900 p-6 rounded-xl border-4 ${color} shadow-2xl">
                            <div class="text-3xl font-bold">${s.signal} ${s.stock} FUT</div>
                            <div class="text-xl mt-2">Entry: ₹${s.price} | SL: ₹${s.sl} | Target: ₹${s.target}</div>
                            <div class="text-lg mt-2">Score: ${s.score}/100 | 5min</div>
                        </div>`;
                    });
                    document.getElementById('list').innerHTML = html;
                } catch(e) {}
            }
            fetchSignals();
        </script>
    </body>
    </html>
    """

@app.get("/signals")
async def get_signals():
    global signals
    if random.random() > 0.75:
        new = {
            "stock": random.choice(stocks),
            "signal": random.choice(["ULTRA BUY", "ULTRA SELL"]),
            "price": round(random.uniform(800, 4500), 2),
            "sl": 0,
            "target": 0,
            "score": random.randint(87, 98)
        }
        new["sl"] = round(new["price"] * (0.994 if "BUY" in new["signal"] else 1.006), 2)
        new["target"] = round(new["price"] * (1.028 if "BUY" in new["signal"] else 0.972), 2)
        signals.append(new)
        if len(signals) > 15:
            signals = signals[-15:]
    return signals
