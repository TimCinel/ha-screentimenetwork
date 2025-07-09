# The Screentime Network Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

This integration provides a sensor for your screen time sourced from thescreentimenetwork.com.

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Go to HACS → Integrations → ⋮ → Custom repositories
3. Add repository URL: `https://github.com/TimCinel/ha-screentimenetwork`
4. Category: Integration
5. Click "Add"
6. Search for "The Screentime Network" in HACS and install it
7. Restart Home Assistant.

### Manual Installation

1. Download the `custom_components/screentimenetwork` directory from the [latest release](https://github.com/TimCinel/ha-screentimenetwork/releases).
2. Copy it into your `custom_components` directory.
3. Restart Home Assistant.

## Prerequisites

Before configuring this integration, you need:

1. **A Screentime Network account** - Sign up at [thescreentimenetwork.com/api/getting-started](https://www.thescreentimenetwork.com/api/getting-started)
2. **ClearSpace iOS app** - Install from [App Store](https://apps.apple.com/us/app/clearspace-reduce-screen-time/id1572515807)
   - Grant Screen Time permissions
   - Log in with your Screentime Network account
   - This app collects and reports your screen time data

## Configuration

1. In the Home Assistant UI, go to **Configuration** > **Integrations**.
2. Click the **+ ADD INTEGRATION** button.
3. Search for "The Screentime Network".
4. Enter your username (handle) and API key from thescreentimenetwork.com.

## Features

- Provides a sensor showing your screen time data
- Updates hourly from thescreentimenetwork.com
- Screen time values are approximate and rounded to the nearest 15-minute interval (due to Apple Screen Time API constraints)

## Support

For issues, please visit the [issue tracker](https://github.com/TimCinel/ha-screentimenetwork/issues).

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[commits-shield]: https://img.shields.io/github/commit-activity/y/TimCinel/ha-screentimenetwork.svg?style=for-the-badge
[commits]: https://github.com/TimCinel/ha-screentimenetwork/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/TimCinel/ha-screentimenetwork.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/TimCinel/ha-screentimenetwork.svg?style=for-the-badge
[releases]: https://github.com/TimCinel/ha-screentimenetwork/releases