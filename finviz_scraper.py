import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# Örnek kullanım
ticker = 'AAPL'  # Hisse kodu
df = scrape_finviz(ticker)
if df is not None:
    print(df)
