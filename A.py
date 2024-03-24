import requests
import hashlib
import hmac
import time

def get_server_time():
    url = 'https://api.binance.com/api/v3/time'
    response = requests.get(url)
    return response.json()['serverTime']

def generate_signature(data, secret_key):
    return hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

def get_crypto_price(symbol, timestamp, api_key, secret_key):
    endpoint = f'https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1d&startTime={timestamp}&limit=1'
    headers = {
        'X-MBX-APIKEY': api_key,
    }
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            price = float(data[0][4])  # Mengambil harga penutup
            return price
        else:
            return f"Tidak dapat menemukan data harga untuk simbol {symbol}"
    else:
        return f"Permintaan gagal dengan kode status {response.status_code}"

# Contoh penggunaan:
symbols = ['BTC', 'BNB', 'ADA', 'DOT', 'SOL', 'XRP', 'DOGE', 'XLM']
timestamp = get_server_time() - (86400000 * 30)  # Mendapatkan waktu server dan mengurangkan 30 hari (dalam milidetik)
api_key = 'knkGeFTOXDxdUPQ783FvyuLKL6KcIBYHwIGaczIyDXvQSipzJToxKI9J7qLyttLT'  # Ganti dengan API key Binance Anda
secret_key = 'pa04RmmpZZmI4u83EWbLMy8kguJLxEeQtcQjfJBIUKJIZ6SEjAMsAiBmblXaKzJe'  # Ganti dengan Secret key Binance Anda
for symbol in symbols:
    harga = get_crypto_price(symbol, timestamp, api_key, secret_key)
    print(f'Harga {symbol} pada tanggal {time.strftime("%Y-%m-%d", time.gmtime(timestamp // 1000))}: ${harga}')
