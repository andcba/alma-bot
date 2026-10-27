
ALMA BOT BINGX - Guia para dejarlo funcionando 24/7

1. Crear cuenta y API Keys en BingX (2 min)
- Entra a BingX.com y crea cuenta (Argentina permitido)
- Perfil -> API Management -> Crear API
- Permisos: SOLO Spot Trading (NO habilitar Withdrawals / Retiros)
- Guarda API Key y Secret Key

2. Instalar
pip install ccxt pandas

3. Configurar keys
Opcion segura: set BINGX_API_KEY=tu_key y BINGX_SECRET_KEY=tu_secret como variables de entorno

4. Dejarlo funcionando 24/7 - 3 OPCIONES:

OPCION 1 - MAS FACIL (Gratis): Railway.app
- Subi el archivo a Railway.app
- Agrega variables BINGX_API_KEY y BINGX_SECRET_KEY
- Comando: python alma_bot_bingx.py
- Queda online 24/7

OPCION 2 - VPS BARATO:
- VPS Hostinger/Contabo $3/mes
- nohup python3 alma_bot_bingx.py &

OPCION 3 - EN TU PC:
- python alma_bot_bingx.py (no cierres la ventana)

MODO SEGURO: viene en simulacion. Descomenta la linea create_market_buy_order para operar real.

Ventaja BingX: minimo $1 por orden vs $5 en Binance. Con $10 podes diversificar.
