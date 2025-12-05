import ccxt
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from telegram import Bot
import config
import time

# ===== Telegram бот =====
bot = Bot(token=config.BOT_TOKEN)

# ===== OKX подключение =====
exchange = ccxt.okx({
    'apiKey': config.OKX_API_KEY,
    'secret': config.OKX_API_SECRET,
    'password': config.OKX_API_PASS,
    'enableRateLimit': True,
})

symbols = config.SYMBOLS
timeframe = config.TIMEFRAME
last_signals = {symbol: None for symbol in symbols}

# ===== Функция расчета сигнала =====
def get_signal(df):
    df['rsi'] = RSIIndicator(df['close'], window=config.RSI_PERIOD).rsi()
    df['ema'] = EMAIndicator(df['close'], window=config.EMA_PERIOD).ema_indicator()

    last_price = df['close'].iloc[-1]
    last_rsi = df['rsi'].iloc[-1]
    last_ema = df['ema'].iloc[-1]

    signal = None
    direction = None

    # Простая логика сигнала
    if last_rsi < 30 and last_price > last_ema:
        direction = "LONG"
    elif last_rsi > 70 and last_price < last_ema:
        direction = "SHORT"

    if direction:
        # Расчет точек входа, стоп-лосс и тейк-профит
        entry_price = last_price
        if direction == "LONG":
            stop_loss = entry_price * (1 - config.STOP_LOSS_PERCENT/100)
            take_profit = entry_price * (1 + config.TAKE_PROFIT_PERCENT/100)
        else:
            stop_loss = entry_price * (1 + config.STOP_LOSS_PERCENT/100)
            take_profit = entry_price * (1 - config.TAKE_PROFIT_PERCENT/100)

        signal = (
            f"{direction}\n"
            f"Цена входа: {entry_price:.2f}\n"
            f"Стоп-лосс: {stop_loss:.2f}\n"
            f"Тейк-профит: {take_profit:.2f}\n"
            f"RSI: {last_rsi:.2f}, EMA: {last_ema:.2f}\n"
            f"Плечо: {config.LEVERAGE}x"
        )
    return signal

# ===== Проверка рынка =====
def check_market():
    for symbol in symbols:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
            signal = get_signal(df)
            if signal and signal != last_signals[symbol]:
                bot.send_message(chat_id=config.CHAT_ID, text=f"{symbol} сигнал:\n{signal}")
                last_signals[symbol] = signal
        except Exception as e:
            print(f"Ошибка с {symbol}: {e}")

# ===== Основной цикл =====
if __name__ == "__main__":
    while True:
        check_market()
        time.sleep(10)  # проверка каждые 10 секунд
