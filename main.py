import requests
import datetime as dt
from twilio.rest import Client

# setup account SSID and token for the SMS service

account_sid = "AC04b6d768ef5c9f7b9093afe4ed0ce2cb"
auth_token = "5976f3a890eb865e1eb50a94a970d077"
phone = "+18573845253"

# Get the past 2 days

previous_Date = dt.datetime.today() - dt.timedelta(days=1)
pd = str(previous_Date).split(" ")
day_before_yesterday = dt.datetime.today() - dt.timedelta(days=2)
dby = str(day_before_yesterday).split(" ")

# Search for the news about the stock we are interested in


def search_for_news(ticker):
    news_param = {
        "category": "business",
        "language": "en"

    }
    url = f"https://newsapi.org/v2/top-headlines?q={ticker}&apiKey=e0a6620162614d9faa8682ebfa509907"
    response = requests.get(url=url, params=news_param)
    response.raise_for_status()
    x = response.json()
    number_of_results = x['totalResults']
    if number_of_results > 3: number_of_results = 3
    hold = []
    combined_articles = ""
    for i in range(0, number_of_results):
        hold.append(
            f"Title:    {x['articles'][i]['title']}\n"f"Description:   {x['articles'][i]['description']}\n"f"Url:    {x['articles'][i]['url']}\n")

    for i in range(0, len(hold)):
        combined_articles += "\n" + hold[i]
    return combined_articles


def stock_close_price_tracker(stock_ticker):

    API = "OTF8N8SW7WUL1E1L"
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_ticker.upper(),
        "interval": "60min",
        "apikey": API

    }
    url = 'https://www.alphavantage.co/query?'
    r = requests.get(url, params=stock_parameters)
    data = r.json()

    # Get the past 2 days close

    day_before_yesterday_close = int(float((data['Time Series (Daily)'][f"{dby[0]}"]['4. close'])))
    previous_day_close = int(float((data['Time Series (Daily)'][f"{pd[0]}"]['4. close'])))

    # Calculate percentage change(UP/DOWN)

    percent_change_decrease = int((day_before_yesterday_close - previous_day_close) / previous_day_close * 100)
    percent_change_increase = int((previous_day_close - day_before_yesterday_close) / day_before_yesterday_close * 100)


    # Check to see if the stock moved up/down by more than 10 percent, if so find the news and send SMS

    if percent_change_increase >= 5 or percent_change_decrease <= -5:
        text_to_send = f"{stock_ticker} price changes by 5%\n"
        text_to_send += search_for_news(stock_ticker)
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body= text_to_send,
            from_=phone,
            to="+15713325482"
        )


stock_close_price_tracker("COIN")

