import requests, os

def run(arg: str, cfg: dict) -> str:
    key = cfg.get("NEWS_API_KEY") or os.getenv("NEWS_API_KEY")
    if not key:
        raise RuntimeError("NEWS_API_KEY missing in config.json")
    q = arg or "technology"
    url = f"https://newsapi.org/v2/everything?q={q}&sortBy=publishedAt&pageSize=5&apiKey={key}"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    items = data.get("articles", [])
    if not items:
        return "No news found."
    lines = [f"- {a['title']} ({a.get('source',{}).get('name','')})" for a in items]
    return "\n".join(lines)
