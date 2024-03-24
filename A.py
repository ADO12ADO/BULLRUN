import requests
from datetime import datetime

def get_crypto_prices(symbols, date):
    api_key = 'dbe9d93e-6a86-47ff-87a4-2fd7d73fcfc4'  # Ganti dengan kunci API Anda
    date_str = date.strftime('%Y%m%d')
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical?symbol={",".join(symbols)}&time_start={date_str}&time_end={date_str}&convert=USD'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        prices = {}
        for symbol in symbols:
            if 'data' in data and symbol in data['data']:
                prices[symbol] = data['data'][symbol]['quote']['USD']['close']
            else:
                prices[symbol] = f"Tidak dapat menemukan data harga untuk simbol {symbol} pada tanggal {date_str}"
        return prices
    else:
        return f"Permintaan gagal dengan kode status {response.status_code}"

# Contoh penggunaan:
symbols = ['BTC', 'BNB', 'SOL', 'ADA', 'DOT']  # Ganti dengan simbol kripto yang diinginkan
tanggal = datetime(2020, 5, 11)  # Ganti dengan tanggal yang diinginkan
harga_crypto = get_crypto_prices(symbols, tanggal)
for symbol, harga in harga_crypto.items():
    print(f'Harga {symbol} pada tanggal {tanggal.strftime("%d %B %Y")}: ${harga}')
