"""Fixtures for The Screentime Network integration tests."""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable loading of custom integrations in all tests."""
    return


@pytest.fixture
def mock_setup_entry():
    """Mock setup entry."""
    with patch(
        "custom_components.screentimenetwork.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def mock_stn_api():
    """Mock STNApiClient."""
    with patch("custom_components.screentimenetwork.api.STNApiClient") as mock_client:
        client = mock_client.return_value
        client.async_get_data.return_value = {"data": {"totalScreenTime": 123.5}}
        yield client
