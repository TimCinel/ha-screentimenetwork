"""Test The Screentime Network API."""

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from custom_components.screentimenetwork.api import (
    STNApiClient,
    STNApiClientAuthenticationError,
    STNApiClientCommunicationError,
)


async def test_api_get_data_success():
    """Test successful API call."""
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value={
        "data": {
            "totalScreenTime": 150.5
        }
    })
    mock_resp.raise_for_status = MagicMock()
    
    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_resp)
    
    client = STNApiClient(
        handle="testuser",
        api_key="test_api_key",
        session=mock_session
    )
    
    result = await client.async_get_data()
    
    assert result == {"data": {"totalScreenTime": 150.5}}
    mock_session.request.assert_called_once_with(
        method="get",
        url="https://api.thescreentimenetwork.com/v1/getScreenTimeToday?handle=testuser",
        headers={"x-api-key": "test_api_key"},
        json=None,
    )


async def test_api_auth_error():
    """Test API authentication error."""
    mock_resp = AsyncMock()
    mock_resp.status = 401
    mock_resp.raise_for_status = MagicMock()
    
    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_resp)
    
    client = STNApiClient(
        handle="testuser",
        api_key="invalid_key",
        session=mock_session
    )
    
    # The auth error should be raised directly from _verify_response_or_raise
    with pytest.raises(STNApiClientAuthenticationError, match="Invalid credentials"):
        await client.async_get_data()


async def test_api_timeout_error():
    """Test API timeout error."""
    mock_session = AsyncMock()
    mock_session.request = AsyncMock(side_effect=TimeoutError())
    
    client = STNApiClient(
        handle="testuser",
        api_key="test_api_key",
        session=mock_session
    )
    
    with pytest.raises(STNApiClientCommunicationError):
        await client.async_get_data()