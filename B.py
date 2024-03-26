import requests
import json

def get_binance_portfolio(api_key, secret_key):
    # Ganti URL Binance sesuai dengan akun Anda (live atau testnet)
    base_url = 'https://api.binance.com'
    #base_url = 'https://testnet.binance.vision'  # Uncomment this line for Binance testnet

    # Endpoint untuk mendapatkan informasi akun
    endpoint = '/api/v3/account'

    # Waktu kadaluarsa permintaan (dalam milidetik)
    request_timeout = 5000

    # Tambahkan header dengan API key
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Kirim permintaan GET ke Binance API
    response = requests.get(base_url + endpoint, headers=headers, timeout=request_timeout)
    
    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        # Parsing data JSON
        account_info = json.loads(response.text)
        
        # Inisialisasi total portofolio dan dictionary untuk menyimpan jumlah koin per simbol
        total_portfolio_value = 0
        symbol_balances = {}
        
        # Loop melalui saldo aset
        for asset in account_info['balances']:
            free_balance = float(asset['free'])
            locked_balance = float(asset['locked'])
            total_balance = free_balance + locked_balance
            
            if total_balance > 0:
                symbol = asset['asset']
                symbol_balances[symbol] = total_balance
                total_portfolio_value += total_balance
        
        # Tampilkan total nilai portofolio dan saldo per simbol di terminal
        print("Total Portfolio Value:", total_portfolio_value)
        print("Symbol Balances:")
        for symbol, balance in symbol_balances.items():
            print(symbol, ":", balance)
    else:
        print("Failed to retrieve account information. Status code:", response.status_code)

# Masukkan API key dan secret key Anda di sini
api_key = 'your_api_key'
secret_key = 'your_secret_key'

get_binance_portfolio(api_key, secret_key)
