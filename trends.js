import fetch from "node-fetch";

export default async function handler(req, res) {
  const { keyword = "TSLA" } = req.query;
  try {
    const reqBody = {
      comparisonItem: [{ keyword, geo: "US", time: "now 7-d" }],
      category: 0,
      property: "",
    };
    const url = `https://trends.google.com/trends/api/explore?hl=en-US&tz=-480&req=${encodeURIComponent(JSON.stringify(reqBody))}`;

    const response = await fetch(url);
    if (!response.ok) {
      return res.status(response.status).json({ error: `Google returned ${response.status}` });
    }

    const text = await response.text();
    const match = text.match(/average\":(\d+)/);
    const score = match ? parseFloat(match[1]) : 0;

    res.setHeader("Access-Control-Allow-Origin", "*");
    res.status(200).json({ keyword, score });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
