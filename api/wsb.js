export default async function handler(req, res) {
  try {
    const auth = Buffer.from(
      process.env.REDDIT_CLIENT_ID + ":" + process.env.REDDIT_CLIENT_SECRET
    ).toString("base64");

    // 正確的 OAuth 端點
    const tokenRes = await fetch("https://www.reddit.com/api/v1/access_token", {
      method: "POST",
      headers: {
        "Authorization": `Basic ${auth}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "grant_type=client_credentials",
    });

    const tokenData = await tokenRes.json();
    const accessToken = tokenData.access_token;

    // ✅ 改這裡：使用 Reddit OAuth API endpoint，而非 public Reddit JSON
    const redditRes = await fetch(
      "https://oauth.reddit.com/r/wallstreetbets/hot?limit=100",
      {
        headers: {
          "Authorization": `Bearer ${accessToken}`,
          "User-Agent": "MemeRadarBot/1.0 by yourname",
        },
      }
    );

    const text = await redditRes.text();

    if (!redditRes.ok || text.startsWith("<")) {
      console.error("⚠️ Reddit OAuth blocked request:", redditRes.status, text.slice(0, 200));
      return res.status(500).json({ error: "Reddit OAuth blocked request" });
    }

    const data = JSON.parse(text);
    res.setHeader("Cache-Control", "s-maxage=600, stale-while-revalidate");
    res.status(200).json(data);

  } catch (err) {
    console.error("Reddit proxy error:", err);
    res.status(500).json({ error: "Proxy internal error" });
  }
}
