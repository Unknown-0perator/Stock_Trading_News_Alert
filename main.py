import requests
import datetime

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = 'API'  # https://www.alphavantage.co/support/#api-key Generate your own API key
TODAY_DATE = datetime.date.today()
YESTERDAY_DATE = TODAY_DATE - datetime.timedelta(days=1)
BEFORE_YESTERDAY_DATE = TODAY_DATE - datetime.timedelta(days=2)

Parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY,
}


response = requests.get(url=STOCK_ENDPOINT, params=Parameters)
data = response.json()
yesterday_closing_data = data['Time Series (Daily)'][str(YESTERDAY_DATE)]['4. close']

before_yesterday_closing_data = data['Time Series (Daily)'][str(BEFORE_YESTERDAY_DATE)]['4. close']
difference = abs(float(yesterday_closing_data) - float(before_yesterday_closing_data))
diff_percentage = (difference/float(yesterday_closing_data)) * 100
print(diff_percentage)
if diff_percentage > 5:
    print('Get News')

