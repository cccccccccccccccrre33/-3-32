import os

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# OKX
OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_API_SECRET = os.getenv("OKX_API_SECRET")
OKX_API_PASS = os.getenv("OKX_API_PASS")

# Монеты и таймфрейм
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']  # можно менять
TIMEFRAME = '1h'

# Индикаторы
RSI_PERIOD = 14
EMA_PERIOD = 20

# Настройки сигналов
LEVERAGE = 5  # плечо
STOP_LOSS_PERCENT = 1.5  # стоп-лосс %
TAKE_PROFIT_PERCENT = 3  # тейк-профит %
