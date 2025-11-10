from pytrends.request import TrendReq
from urllib.parse import parse_qs
import json
import random
import time

def handler(request):
    query = parse_qs(request.query)
    keyword = query.get("keyword", [""])[0]

    if not keyword:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing keyword"})
        }

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        time.sleep(random.uniform(1, 3))  # 防止 Google 429
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
        data = pytrends.interest_over_time()

        if data.empty or keyword not in data.columns:
            score = 0
        else:
            score = int(data[keyword].iloc[-1])

        return {
            "statusCode": 200,
            "body": json.dumps({"score": score})
        }

    except Exception as e:
        print("❌ Error fetching trends:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
