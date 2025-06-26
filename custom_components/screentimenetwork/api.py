"""The Screentime Network API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class STNApiClientError(Exception):
    """Exception to indicate a general API error."""


class STNApiClientCommunicationError(
    STNApiClientError,
):
    """Exception to indicate a communication error."""


class STNApiClientAuthenticationError(
    STNApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise STNApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class STNApiClient:
    """The Screentime Network API Client."""

    def __init__(
        self,
        handle: str,
        api_key: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize The Screentime Network API Client."""
        self._handle = handle
        self._api_key = api_key
        self._session = session

    async def async_get_data(self) -> Any:
        """Get screen time data from the API."""
        return await self._api_wrapper(
            method="get",
            url=f"https://api.thescreentimenetwork.com/v1/getScreenTimeToday?handle={self._handle}",
            headers={"x-api-key": self._api_key},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except STNApiClientAuthenticationError:
            raise
        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise STNApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise STNApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise STNApiClientError(
                msg,
            ) from exception
