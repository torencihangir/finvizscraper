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
            print("Failed to retrieve data")
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
        print(f"An error occurred: {e}")
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

# Örnek kullanım
tickers = ['AAPL', 'MSFT', 'GOOG']  # Hisse kodları listesi
df = scrape_multiple_tickers(tickers)
if df is not None:
    df.to_csv('finviz_data.csv', index=False)
    print("Data saved to finviz_data.csv")
