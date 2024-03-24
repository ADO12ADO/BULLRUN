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

def get_crypto_price(symbol, timestamps, api_key, secret_key):
    prices = {}
    for timestamp in timestamps:
        endpoint = f'https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1d&startTime={timestamp}&limit=1'
        headers = {
            'X-MBX-APIKEY': api_key,
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                price = float(data[0][4])  # Mengambil harga penutup
                prices[timestamp] = price
            else:
                prices[timestamp] = f"Tidak dapat menemukan data harga untuk simbol {symbol}"
        else:
            prices[timestamp] = f"Permintaan gagal dengan kode status {response.status_code}"
    return prices

# Contoh penggunaan:
symbols = ['BTC', 'BNB', 'ADA', 'DOT', 'SOL', 'XRP', 'DOGE', 'XLM']
tanggal1 = '2020-05-11'
tanggal2 = '2021-04-11'
timestamps = [int(time.mktime(time.strptime(tanggal1, '%Y-%m-%d'))) * 1000, int(time.mktime(time.strptime(tanggal2, '%Y-%m-%d'))) * 1000]
api_key = 'knkGeFTOXDxdUPQ783FvyuLKL6KcIBYHwIGaczIyDXvQSipzJToxKI9J7qLyttLT'  # Ganti dengan API key Binance Anda
secret_key = 'pa04RmmpZZmI4u83EWbLMy8kguJLxEeQtcQjfJBIUKJIZ6SEjAMsAiBmblXaKzJe'  # Ganti dengan Secret key Binance Anda

for symbol in symbols:
    harga = get_crypto_price(symbol, timestamps, api_key, secret_key)
    if all(isinstance(value, float) for value in harga.values()):
        harga_tanggal1 = harga[timestamps[0]]
        harga_tanggal2 = harga[timestamps[1]]
        kenaikan = ((harga_tanggal2 - harga_tanggal1) / harga_tanggal1) * 100
        print(f'Kenaikan harga {symbol} dari {tanggal1} ke {tanggal2}: {kenaikan:.2f}%')
    else:
        print(f'Kenaikan harga {symbol}: {harga[timestamps[0]]}')
