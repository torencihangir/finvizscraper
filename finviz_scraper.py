import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # Gecikme için gerekli kütüphane

def scrape_finviz(ticker):
    try:
        url = f'https://finviz.com/quote.ashx?t={ticker}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to retrieve data for", ticker)
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Tablo verilerini bul
        table = soup.find('table', class_='snapshot-table2')
        data = {}
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                for i in range(0, len(cols), 2):
                    key = cols[i].text
                    value = cols[i+1].text
                    data[key] = value
        
        return pd.DataFrame([data])
    except Exception as e:
        print(f"An error occurred for {ticker}: {e}")
        return None

def scrape_multiple_tickers(tickers):
    all_data = []
    for ticker in tickers:
        print(f"Scraping data for {ticker}...")
        data = scrape_finviz(ticker)
        if data is not None:
            data['Ticker'] = ticker  # Hisse kodunu ekle
            all_data.append(data)
        time.sleep(5)  # Her istekten sonra 5 saniye bekle
    
    # Pandas DataFrame'e dönüştür
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("No data retrieved.")
        return None

# Hisse kodları listesi
tickers = [
    'AAPL', 'ABNB', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEP', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANSS', 'APP', 'ARM', 
    'ASML', 'AVGO', 'AXON', 'AZN', 'BIIB', 'BKNG', 'BKR', 'CCEP', 'CDNS', 'CDW', 'CEG', 'CHTR', 'CMCSA', 
    'COST', 'CPRT', 'CRWD', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'DASH', 'DDOG', 'DXCM', 'EA', 'EXC', 'FANG', 
    'FAST', 'FTNT', 'GEHC', 'GFS', 'GILD', 'GOOG', 'GOOGL', 'HON', 'IDXX', 'INTC', 'INTU', 'ISRG', 'KDP', 'KHC', 
    'KLAC', 'LIN', 'LRCX', 'LULU', 'MAR', 'MCHP', 'MDB', 'MDLZ', 'MELI', 'META', 'MNST', 'MRVL', 'MSFT', 'MSTR', 
    'MU', 'NFLX', 'NVDA', 'NXPI', 'ODFL', 'ON', 'ORLY', 'PANW', 'PAYX', 'PCAR', 'PDD', 'PEP', 'PLTR', 'PYPL', 
    'QCOM', 'REGN', 'ROPR', 'ROST', 'SBUX', 'SNPS', 'TEAM', 'TMUS', 'TSLA', 'TTD', 'TTWO', 'TXN', 'VRSK', 'VRTX', 
    'WBD', 'WDAY', 'XEL', 'ZS'
]

df = scrape_multiple_tickers(tickers)
if df is not None:
    df.to_csv('finviz_data.csv', index=False)
    print("Data saved to finviz_data.csv")
