import os

SEARCH_INTERVAL = int(os.getenv("SEARCH_INTERVAL", "300"))

MIN_CONFIDENCE = float(
    os.getenv("MIN_CONFIDENCE", "0.90")
)

PLATFORMS = ["tiktok", "instagram"]

ALERT_MODE = "confirmed"
SEARCH_LEVEL = "maximum"

TIKTOK_FEED_URL = os.getenv("TIKTOK_FEED_URL", "")
INSTAGRAM_FEED_URL = os.getenv("INSTAGRAM_FEED_URL", "")

TIKTOK_API_TOKEN = os.getenv("TIKTOK_API_TOKEN", "")
INSTAGRAM_API_TOKEN = os.getenv("INSTAGRAM_API_TOKEN", "")
