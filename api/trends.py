from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import time

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/api/trends')
def get_trends():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "missing keyword"}), 400

    try:
        # 建立 payload
        pytrends.build_payload([keyword], timeframe='now 7-d', geo='US')
        interest = pytrends.interest_over_time()
        if interest.empty:
            score = 0
        else:
            # 取 7 天平均
            score = round(interest[keyword].mean())
        # 避免被封鎖，休息 2 秒
        time.sleep(2)
        return jsonify({"keyword": keyword, "score": score})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
