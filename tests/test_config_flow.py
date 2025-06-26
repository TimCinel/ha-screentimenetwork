"""Test The Screentime Network config flow."""

from unittest.mock import AsyncMock, patch

from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.screentimenetwork.api import (
    STNApiClientAuthenticationError,
    STNApiClientCommunicationError,
    STNApiClientError,
)
from custom_components.screentimenetwork.const import DOMAIN


async def test_form_user(hass: HomeAssistant):
    """Test user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.screentimenetwork.config_flow.STNApiClient",
    ) as mock_client:
        mock_client.return_value.async_get_data = AsyncMock(
            return_value={"data": {"totalScreenTime": 123}}
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_API_TOKEN: "test_api_key",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "The Screentime Network (testuser)"
    assert result2["data"] == {
        CONF_USERNAME: "testuser",
        CONF_API_TOKEN: "test_api_key",
    }


async def test_form_invalid_auth(hass: HomeAssistant):
    """Test invalid authentication."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.screentimenetwork.config_flow.STNApiClient",
    ) as mock_client:
        mock_client.return_value.async_get_data = AsyncMock(
            side_effect=STNApiClientAuthenticationError("Invalid credentials")
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_API_TOKEN: "wrong_key",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"]["base"] == "auth"


async def test_form_cannot_connect(hass: HomeAssistant):
    """Test connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.screentimenetwork.config_flow.STNApiClient",
    ) as mock_client:
        mock_client.return_value.async_get_data = AsyncMock(
            side_effect=STNApiClientCommunicationError("Cannot connect")
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_API_TOKEN: "test_api_key",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"]["base"] == "connection"


async def test_form_unknown_error(hass: HomeAssistant):
    """Test unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.screentimenetwork.config_flow.STNApiClient",
    ) as mock_client:
        mock_client.return_value.async_get_data = AsyncMock(
            side_effect=STNApiClientError("Unknown error")
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_API_TOKEN: "test_api_key",
            },
        )

    assert result2["type"] == FlowResultType.FORM
    assert result2["errors"]["base"] == "unknown"


async def test_form_already_configured(hass: HomeAssistant):
    """Test already configured."""
    entry = config_entries.ConfigEntry(
        version=1,
        minor_version=1,
        domain=DOMAIN,
        title="The Screentime Network (testuser)",
        data={
            CONF_USERNAME: "testuser",
            CONF_API_TOKEN: "test_api_key",
        },
        source=config_entries.SOURCE_USER,
        unique_id="testuser",
        entry_id="test",
        discovery_keys={},
        options={},
        subentries_data={},
    )
    hass.config_entries._entries[entry.entry_id] = entry

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.screentimenetwork.config_flow.STNApiClient",
    ) as mock_client:
        mock_client.return_value.async_get_data = AsyncMock(
            return_value={"data": {"totalScreenTime": 123}}
        )

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "testuser",
                CONF_API_TOKEN: "test_api_key",
            },
        )

    assert result2["type"] == FlowResultType.ABORT
    assert result2["reason"] == "already_configured"
