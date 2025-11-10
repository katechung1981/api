from pytrends.request import TrendReq
from urllib.parse import parse_qs
import json

def handler(request):
    query = parse_qs(request.query)
    keyword = query.get("keyword", [""])[0]

    if not keyword:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing keyword"})
        }

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
    data = pytrends.interest_over_time()

    if data.empty:
        score = 0
    else:
        score = int(data[keyword].iloc[-1])

    return {
        "statusCode": 200,
        "body": json.dumps({"score": score})
    }
