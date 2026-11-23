import json
import urllib.request

from config import TIKTOK_FEED_URL, TIKTOK_API_TOKEN


def scan_tiktok():

    if not TIKTOK_FEED_URL or not TIKTOK_API_TOKEN:
        return []

    request = urllib.request.Request(
        TIKTOK_FEED_URL,
        headers={
            "Authorization": f"Bearer {TIKTOK_API_TOKEN}",
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        if isinstance(data, dict):
            return data.get("results", [])

        return data if isinstance(data, list) else []

    except Exception as error:
        print(f"TikTok scanner error: {error}")
        return []
