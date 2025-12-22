import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter (no Redis)."""

    def __init__(self, app):
        super().__init__(app)
        self.requests = {}
        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.window = settings.RATE_LIMIT_WINDOW

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "anonymous"
        now = time.time()
        window_start, count = self.requests.get(client_ip, (now, 0))

        if now - window_start >= self.window:
            window_start, count = now, 0

        count += 1
        self.requests[client_ip] = (window_start, count)

        if count > self.max_requests:
            logger.warning("Rate limit exceeded for %s", client_ip)
            return Response(
                content="Rate limit exceeded. Try again later.",
                status_code=429,
            )

        return await call_next(request)

