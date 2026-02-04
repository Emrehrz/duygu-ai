import time
from collections import defaultdict

from config import settings


RATE_LIMIT = settings.rate_limit  # dakika başına istek limiti
WINDOW = settings.rate_limit_window  # saniye cinsinden pencere

requests_log = defaultdict(list)


def is_rate_limited(ip: str) -> bool:
    now = time.time()
    window_start = now - WINDOW

    # Eski kayıtları temizle
    requests_log[ip] = [ts for ts in requests_log[ip] if ts > window_start]

    if len(requests_log[ip]) >= RATE_LIMIT:
        return True

    requests_log[ip].append(now)
    return False
