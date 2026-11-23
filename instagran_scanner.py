import json
import urllib.request

from config import INSTAGRAM_FEED_URL, INSTAGRAM_API_TOKEN


def scan_instagram():

    if not INSTAGRAM_FEED_URL or not INSTAGRAM_API_TOKEN:
        return []

    request = urllib.request.Request(
        INSTAGRAM_FEED_URL,
        headers={
            "Authorization": f"Bearer {INSTAGRAM_API_TOKEN}",
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
        print(f"Instagram scanner error: {error}")
        return []
