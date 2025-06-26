"""Adds config flow for The Screentime Network."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    STNApiClient,
    STNApiClientAuthenticationError,
    STNApiClientCommunicationError,
    STNApiClientError,
)
from .const import DOMAIN, LOGGER


class STNFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for The Screentime Network."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    handle=user_input[CONF_USERNAME],
                    api_key=user_input[CONF_API_TOKEN],
                )
            except STNApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except STNApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except STNApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(unique_id=user_input[CONF_USERNAME])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"The Screentime Network ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USERNAME,
                        default=(user_input or {}).get(CONF_USERNAME, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(
                        CONF_API_TOKEN,
                        default=(user_input or {}).get(CONF_API_TOKEN, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, handle: str, api_key: str) -> None:
        """Validate credentials."""
        client = STNApiClient(
            handle=handle,
            api_key=api_key,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
