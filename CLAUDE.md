# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant custom integration for The Screentime Network (thescreentimenetwork.com). It provides sensors for tracking screen time data.

## Key Information

- **Integration Name**: The Screentime Network
- **Domain**: `screentimenetwork`
- **Short name in code**: STN
- **Authentication**: Username (handle) + API key
- **Integration Type**: Cloud polling
- **Update Interval**: Hourly
- **API Endpoint**: `https://api.thescreentimenetwork.com/v1/getScreenTimeToday`
- **Data Format**: Returns screen time in minutes via `data.totalScreenTime`

## Common Commands

- **Run linter**: `./scripts/lint`
- **Run tests**: `pytest`
- **Start Home Assistant for testing**: `./scripts/develop`
- **Install dependencies**: `./scripts/setup`
- **Install test dependencies**: `pip install -r requirements-test.txt`

## Architecture

### File Structure
```
custom_components/screentimenetwork/
├── __init__.py          # Integration setup and configuration entry
├── api.py               # STNApiClient for API communication
├── config_flow.py       # STNFlowHandler for UI configuration
├── const.py             # Constants (domain, attribution)
├── coordinator.py       # STNDataUpdateCoordinator for data fetching
├── data.py              # STNConfigEntry and STNData type definitions
├── entity.py            # STNEntity base class (no device grouping)
├── sensor.py            # STNSensor implementation
├── icon.png             # Integration icon (256x256)
├── icon@2x.png          # High-res integration icon (512x512)
├── manifest.json        # Integration metadata
└── translations/
    └── en.json          # English translations

tests/
├── __init__.py          # Test package
├── conftest.py          # Shared test fixtures
├── test_api.py          # API client tests
├── test_config_flow.py  # Configuration flow tests
└── test_sensor.py       # Sensor tests

.github/workflows/
└── ci.yml               # CI pipeline (lint, validate, test)
```

### Key Classes
- `STNApiClient`: Handles API communication with thescreentimenetwork.com
- `STNDataUpdateCoordinator`: Manages data updates using Home Assistant's DataUpdateCoordinator pattern
- `STNConfigEntry`: Type definition for configuration entries
- `STNFlowHandler`: Handles the configuration flow for adding the integration
- `STNSensor`: The sensor entity that displays screen time data (no device grouping)

### API Integration
The integration connects to The Screentime Network API:
```bash
curl "https://api.thescreentimenetwork.com/v1/getScreenTimeToday?handle=USERNAME" \
  -H 'x-api-key: API_KEY'
```

Response format:
```json
{
  "data": {
    "totalScreenTime": 150.5
  }
}
```

### Configuration
- **Username**: The user's handle on thescreentimenetwork.com
- **API Key**: Authentication token from the service
- **Unique ID**: Based on username to prevent duplicates

### Sensor Details
- **Name**: "Screen Time Today"
- **Icon**: `mdi:timer-sand` (hourglass)
- **Unit**: minutes
- **Device Class**: duration
- **State Class**: measurement
- **No Device**: Integration creates entities without device grouping

## Testing

### Test Coverage
- **API Client**: Success, authentication errors, timeouts
- **Config Flow**: User flow, validation, error handling, duplicate detection
- **Sensor**: Data parsing, empty data handling, entity descriptions

### Running Tests
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=custom_components.screentimenetwork

# Run specific test file
pytest tests/test_api.py -v
```

## CI/CD

The repository includes a comprehensive CI workflow (`.github/workflows/ci.yml`) that runs on:
- Push to master branch
- Pull requests to master
- Daily schedule (for validation)
- Manual trigger

### CI Jobs
1. **Lint**: Ruff linting and formatting checks
2. **Validate**: Home Assistant (hassfest) and HACS validation
3. **Test**: Full pytest suite on Python 3.13

### Code Quality
- **Linter**: Ruff with Home Assistant standards
- **Configuration**: `.ruff.toml` with test-specific ignores
- **Coverage**: Tests cover API, config flow, and sensor functionality

## Development Notes

### Requirements
- **Python**: 3.13+ (matches Home Assistant requirements)
- **Dependencies**: All provided by Home Assistant core (no external deps)
- **Testing**: Uses pytest-homeassistant-custom-component

### Important Implementation Details
- No device creation (entities appear directly under integration)
- Proper exception handling in API client with specific error types
- Uses Home Assistant's DataUpdateCoordinator pattern for efficient polling
- Follows Home Assistant integration best practices

### Icon Setup
- Local icons are included but not used (requires brands repository submission)
- To get custom icon: Submit PR to https://github.com/home-assistant/brands
- Current fallback: Home Assistant default integration icon