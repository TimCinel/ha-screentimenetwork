"""Test The Screentime Network sensor."""

from unittest.mock import MagicMock

from custom_components.screentimenetwork.sensor import ENTITY_DESCRIPTIONS, STNSensor


async def test_sensor_native_value():
    """Test sensor native value calculation."""
    coordinator = MagicMock()
    coordinator.data = {"data": {"totalScreenTime": 123.5}}
    coordinator.config_entry.entry_id = "test_entry_id"

    sensor = STNSensor(
        coordinator=coordinator,
        entity_description=ENTITY_DESCRIPTIONS[0],
    )

    assert sensor.native_value == 123.5


async def test_sensor_no_data():
    """Test sensor with no data."""
    coordinator = MagicMock()
    coordinator.data = None
    coordinator.config_entry.entry_id = "test_entry_id"

    sensor = STNSensor(
        coordinator=coordinator,
        entity_description=ENTITY_DESCRIPTIONS[0],
    )

    assert sensor.native_value is None


async def test_sensor_empty_data():
    """Test sensor with empty data."""
    coordinator = MagicMock()
    coordinator.data = {}
    coordinator.config_entry.entry_id = "test_entry_id"

    sensor = STNSensor(
        coordinator=coordinator,
        entity_description=ENTITY_DESCRIPTIONS[0],
    )

    assert sensor.native_value == 0


async def test_sensor_entity_description():
    """Test sensor entity description."""
    entity_desc = ENTITY_DESCRIPTIONS[0]

    assert entity_desc.key == "screentimenetwork"
    assert entity_desc.name == "Screen Time Today"
    assert entity_desc.icon == "mdi:timer-sand"
    assert entity_desc.native_unit_of_measurement == "min"
