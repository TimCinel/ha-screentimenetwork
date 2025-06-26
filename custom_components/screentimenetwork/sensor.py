"""Sensor platform for The Screentime Network."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfTime

from .entity import STNEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import STNDataUpdateCoordinator
    from .data import STNConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="screentimenetwork",
        name="Screen Time Today",
        icon="mdi:timer-sand",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: STNConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        STNSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class STNSensor(STNEntity, SensorEntity):
    """The Screentime Network Sensor class."""

    def __init__(
        self,
        coordinator: STNDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        if self.coordinator.data is None:
            return None
        # API returns data.totalScreenTime in minutes
        return self.coordinator.data.get("data", {}).get("totalScreenTime", 0)
