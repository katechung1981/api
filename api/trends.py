from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import time, random

app = Flask(__name__)

@app.route("/api/trends")
def get_trend():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "missing keyword"}), 400

    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        time.sleep(random.uniform(1.5, 3.5))  # 加入隨機延遲
        pytrends.build_payload([keyword], timeframe="now 7-d", geo="US")
        data = pytrends.interest_over_time()
        if data.empty:
            return jsonify({"keyword": keyword, "score": 0})
        score = float(data[keyword].mean())
        return jsonify({"keyword": keyword, "score": round(score, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
