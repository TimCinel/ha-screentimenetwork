"""Custom types for The Screentime Network."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import STNApiClient
    from .coordinator import STNDataUpdateCoordinator


type STNConfigEntry = ConfigEntry[STNData]


@dataclass
class STNData:
    """Data for The Screentime Network integration."""

    client: STNApiClient
    coordinator: STNDataUpdateCoordinator
    integration: Integration
