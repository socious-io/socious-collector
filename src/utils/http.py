import aiohttp
import asyncio
from typing import Optional, Dict, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from src.utils.logger import get_logger

logger = get_logger('http_client')


class AsyncHTTPClient:
    """
    Async HTTP client with retry logic and connection pooling.
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self._session

    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        reraise=True
    )
    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make an async GET request with retry logic.

        Args:
            url: Request URL
            params: Query parameters
            headers: Request headers
            proxy: Proxy URL (optional)

        Returns:
            JSON response as dict
        """
        session = await self._get_session()
        logger.debug(f"GET {url} params={params}")

        try:
            async with session.get(url, params=params, headers=headers, proxy=proxy) as response:
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"GET {url} -> {response.status}")
                return data
        except aiohttp.ClientResponseError as e:
            logger.error(f"HTTP error {e.status} for GET {url}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Request failed for GET {url}: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
        reraise=True
    )
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make an async POST request with retry logic.

        Args:
            url: Request URL
            data: Form data
            json_data: JSON body
            headers: Request headers
            proxy: Proxy URL (optional)

        Returns:
            JSON response as dict
        """
        session = await self._get_session()
        logger.debug(f"POST {url}")

        try:
            async with session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                proxy=proxy
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.debug(f"POST {url} -> {response.status}")
                return result
        except aiohttp.ClientResponseError as e:
            logger.error(f"HTTP error {e.status} for POST {url}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Request failed for POST {url}: {e}")
            raise


# Global HTTP client instance
http_client = AsyncHTTPClient()


async def async_get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    proxy: Optional[str] = None
) -> Dict[str, Any]:
    """Convenience function for GET requests."""
    return await http_client.get(url, params=params, headers=headers, proxy=proxy)


async def async_post(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    proxy: Optional[str] = None
) -> Dict[str, Any]:
    """Convenience function for POST requests."""
    return await http_client.post(url, data=data, json_data=json_data, headers=headers, proxy=proxy)
