import fetch from "node-fetch";

export default async function handler(req, res) {
  const keyword = req.query.keyword || "TSLA";
  const url = `https://trends.google.com/trends/api/explore?hl=en-US&tz=-480&req={"comparisonItem":[{"keyword":"${keyword}","geo":"US","time":"now%207-d"}],"category":0,"property":""}`;

  try {
    const response = await fetch(url);
    const text = await response.text();
    res.status(200).json({ keyword, score: text.length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
}
