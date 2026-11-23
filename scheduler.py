import asyncio
import logging

from config import SEARCH_INTERVAL
from database import initialize, save_result
from tiktok_scanner import scan_tiktok
from instagram_scanner import scan_instagram
from vision_filter import filter_candidates

logger = logging.getLogger(__name__)

searching = False


async def run_scan_cycle():

    sources = [
        ("tiktok", scan_tiktok),
        ("instagram", scan_instagram)
    ]

    for platform, scanner in sources:

        try:
            candidates = await asyncio.to_thread(scanner)

            for candidate in candidates:
                candidate["platform"] = platform

            confirmed = filter_candidates(candidates)

            for result in confirmed:

                saved = save_result(result)

                if saved:
                    logger.info(
                        "Confirmed result: %s",
                        result.get("live_url")
                    )

        except Exception:
            logger.exception(
                "Error scanning %s", platform
            )


async def start_scheduler():

    global searching

    initialize()
    searching = True

    logger.info("SalemSniper scheduler started")

    while searching:

        await run_scan_cycle()

        await asyncio.sleep(SEARCH_INTERVAL)


def stop_scheduler():

    global searching
    searching = False
