from pytrends.request import TrendReq
from urllib.parse import parse_qs
import json
import random
import time

def handler(request):
    query = parse_qs(request.query)
    keyword = query.get("keyword", [""])[0].strip().upper()

    if not keyword:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing keyword"})
        }

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        time.sleep(random.uniform(1.5, 3.5))
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
        data = pytrends.interest_over_time()

        score = int(data[keyword].iloc[-1]) if not data.empty and keyword in data.columns else 0

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
