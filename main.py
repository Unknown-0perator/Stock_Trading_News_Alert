import requests
import datetime
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = 'XUCGBMHJDN70X08C'  # https://www.alphavantage.co/support/#api-key Generate your own API key
NEWS_API_KEY = '1878e261593c4b98a8a8b7f636dbd67d'
# Your Account SID from twilio.com/console
TWILIO_ACCOUNT_SID = "Your Account SID"
# Your Auth Token from twilio.com/console
TWILIO_AUTH_TOKEN = "Your Auth Token"
Parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY,
}
TODAY_DATE = datetime.date.today()
YESTERDAY_DATE = TODAY_DATE - datetime.timedelta(days=1)
BEFORE_YESTERDAY_DATE = TODAY_DATE - datetime.timedelta(days=2)

response = requests.get(url=STOCK_ENDPOINT, params=Parameters)
data = response.json()
yesterday_closing_data = data['Time Series (Daily)'][str(YESTERDAY_DATE)]['4. close']

before_yesterday_closing_data = data['Time Series (Daily)'][str(BEFORE_YESTERDAY_DATE)]['4. close']
difference = float(yesterday_closing_data) - float(before_yesterday_closing_data)
toward_sign = None
if difference > 0:
    toward_sign = '🔺'
else:
    toward_sign = '🔻'
diff_percentage = round((difference / float(yesterday_closing_data)) * 100)

if abs(diff_percentage) > 5:
    news_parameters = {
        'q': COMPANY_NAME,
        'from': BEFORE_YESTERDAY_DATE,
        'sortBy': 'popularity',
        'apiKey': NEWS_API_KEY
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()['articles']
    three_articles = news_data[:3]  # Top three articles about the Company name
formatted_articles = [f"{STOCK_NAME}: {toward_sign}{diff_percentage}%"
                      f"\nHeadline: {article['title']}"
                      f"\nBrief: {article['description']}" for article in three_articles]
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
        to="Your verified number",
        from_="Twilio phone number",
        body=article,
    )
