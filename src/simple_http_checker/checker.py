import logging
import requests
from typing import Collection

logger = logging.getLogger(__name__)


def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """Check the status of a list of URLs and return their status.
    Args:
        urls (list[str]): A list of URLs to check.
        timeout (int): The timeout for the HTTP request in seconds.
    Returns:
        dict[str, str]: A dictionary mapping each URL to its status.
    """
    logger.info(f"Checking {len(urls)} URLs with a timeout of {timeout} seconds.")
    results = {}
    for url in urls:
        status = "Unknown"
        try:
            response = requests.get(url, timeout=5)
            status = (
                f"{response.status_code} OK"
                if response.status_code == 200
                else f"{response.status_code} {response.reason}"
            )
            results[url] = status
        except requests.exceptions.Timeout as e:
            status = "Timeout"
            logger.warning(f"Timeout checking {url}: {e}")
        except requests.exceptions.ConnectionError as e:
            status = "Connection Error"
            logger.warning(f"Connection error checking {url}: {e}")
        except Exception as e:
            status = f"REQUESTS ERROR: {type(e).__name__}"
            logger.error(
                f"An unexpected error occurred while checking {url}: {e}", exc_info=True
            )
        results[url] = status
        logger.debug(f"Checked {url:<40}  -> {status}")

    logger.info("Finished checking URLs.")
    return results
