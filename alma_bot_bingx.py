
# ALMA BOT - VERSION BINGX - $10 -> $100K
# Optimizado para cuenta de $10 (minimo $1 por orden en BingX Spot)

import ccxt
import pandas as pd
import time
import os
from datetime import datetime

CONFIG = {
    "exchange": "bingx",
    "activos": ["SOL/USDT", "PEPE/USDT", "WIF/USDT", "BONK/USDT", "BTC/USDT"],
    "timeframe": "5m",
    "capital_inicial": 10.0,
    "objetivo_fase1": 1000.0,
    "objetivo_final": 100000.0,
    "riesgo_por_trade": 0.20,
    "stop_loss": 0.04,
    "take_profit": 0.12,
    "trailing_stop": 0.06,
    "ema_rapida": 9,
    "ema_lenta": 21,
    "rsi_periodo": 14,
    "rsi_compra_max": 45,
    "rsi_venta": 70,
    "volumen_mult": 1.5,
}

class AlmaBingXBot:
    def __init__(self, api_key, secret_key):
        self.config = CONFIG
        self.balance_inicial = CONFIG["capital_inicial"]
        self.exchange = ccxt.bingx({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'},
        })
        try:
            self.exchange.load_markets()
            print("Conectado a BingX correctamente")
            balance = self.exchange.fetch_balance()
            usdt = balance['USDT']['free'] if 'USDT' in balance else 0
            print(f"Balance USDT en BingX: ${usdt:.2f}")
        except Exception as e:
            print(f"Error conectando a BingX: {e}")

    def calcular_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def analizar(self, simbolo):
        try:
            ohlcv = self.exchange.fetch_ohlcv(simbolo, self.config["timeframe"], limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['ema9'] = df['close'].ewm(span=self.config["ema_rapida"]).mean()
            df['ema21'] = df['close'].ewm(span=self.config["ema_lenta"]).mean()
            df['rsi'] = self.calcular_rsi(df['close'], self.config["rsi_periodo"])
            df['vol_avg'] = df['volume'].rolling(20).mean()
            u = df.iloc[-1]
            a = df.iloc[-2]
            cruce_alcista = a['ema9'] < a['ema21'] and u['ema9'] > u['ema21']
            rsi_ok = 28 < u['rsi'] < self.config["rsi_compra_max"]
            vol_ok = u['volume'] > u['vol_avg'] * self.config["volumen_mult"]
            if cruce_alcista and rsi_ok and vol_ok:
                return "COMPRAR", u['close']
            if u['rsi'] > self.config["rsi_venta"] or u['ema9'] < u['ema21']:
                return "VENDER", u['close']
            return "ESPERAR", u['close']
        except Exception as e:
            print(f"Error analizando {simbolo}: {e}")
            return "ERROR", 0

    def comprar(self, simbolo, precio_actual):
        try:
            balance = self.exchange.fetch_balance()
            usdt_free = balance['USDT']['free']
            monto_usdt = usdt_free * self.config["riesgo_por_trade"]
            if monto_usdt < 1.1:
                print(f"Balance muy bajo para operar: ${usdt_free:.2f}")
                return None
            cantidad = monto_usdt / precio_actual
            print(f"COMPRANDO {simbolo} | Cantidad: {cantidad:.4f} | Precio: {precio_actual} | Monto: ${monto_usdt:.2f}")
            # MODO SIMULACION - descomenta para real:
            # orden = self.exchange.create_market_buy_order(simbolo, cantidad)
            orden = {"id": "simulado", "symbol": simbolo, "amount": cantidad, "price": precio_actual}
            sl = precio_actual * (1 - self.config["stop_loss"])
            tp = precio_actual * (1 + self.config["take_profit"])
            print(f"   -> SL: ${sl:.6f} | TP: ${tp:.6f}")
            return orden
        except Exception as e:
            print(f"Error en compra {simbolo}: {e}")
            return None

    def run(self):
        print(f"ALMA BOT BINGX - $10 -> $100K | Balance inicial: ${self.balance_inicial} | Objetivo Fase1: ${self.config['objetivo_fase1']}")
        while True:
            for simbolo in self.config["activos"]:
                senal, precio = self.analizar(simbolo)
                hora = datetime.now().strftime("%H:%M:%S")
                print(f"[{hora}] {simbolo} @ ${precio:.6f} -> {senal}")
                if senal == "COMPRAR":
                    self.comprar(simbolo, precio)
                    time.sleep(10)
            print("--- Esperando 60s ---\n")
            time.sleep(60)

if __name__ == "__main__":
    API_KEY = os.getenv("BINGX_API_KEY") or "PEGA_TU_API_KEY_AQUI"
    SECRET_KEY = os.getenv("BINGX_SECRET_KEY") or "PEGA_TU_SECRET_AQUI"
    if "PEGA_TU" in API_KEY:
        print("Primero configura tus API Keys de BingX")
    else:
        bot = AlmaBingXBot(API_KEY, SECRET_KEY)
        bot.run()
