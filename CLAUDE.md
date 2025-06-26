# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant custom integration for The Screentime Network (thescreentimenetwork.com). It provides sensors for tracking screen time data.

## Key Information

- **Integration Name**: The Screentime Network
- **Domain**: `screentimenetwork`
- **Short name in code**: STN
- **Authentication**: API key (not username/password)
- **Integration Type**: Cloud polling
- **Update Interval**: Hourly

## Common Commands

- **Run linter**: `./scripts/lint`
- **Start Home Assistant for testing**: `./scripts/develop`
- **Install dependencies**: `./scripts/setup`

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
├── entity.py            # STNEntity base class
├── sensor.py            # STNSensor implementation
├── manifest.json        # Integration metadata
└── translations/
    └── en.json          # English translations
```

### Key Classes
- `STNApiClient`: Handles API communication with thescreentimenetwork.com
- `STNDataUpdateCoordinator`: Manages data updates using Home Assistant's DataUpdateCoordinator pattern
- `STNConfigEntry`: Type definition for configuration entries
- `STNFlowHandler`: Handles the configuration flow for adding the integration
- `STNSensor`: The sensor entity that displays screen time data

### Important Notes
- The API client currently points to jsonplaceholder.typicode.com (placeholder API)
- Authentication uses `CONF_API_TOKEN` from Home Assistant constants
- Only the sensor platform is enabled (no binary_sensor or switch platforms)
- The integration uses Home Assistant's config flow for setup via the UI

## TODO
- Update `api.py` to use the actual thescreentimenetwork.com API endpoints
- Implement proper data parsing for screen time metrics
- Add appropriate sensor attributes and units
- Consider adding additional sensor types if the API provides multiple metrics
- Add unit tests for the integration