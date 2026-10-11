# Changelog

All notable changes to the Virtual Battery integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Discharge periods shorter than a day: setup and options now use a days/hours/minutes picker, minimum 1 minute (#6)
- `set_discharge_days` service accepts fractional days (e.g. `0.25` for 6 hours)
- Time Since Reset and Time Until Empty sensors show 4 decimals (about 9 seconds) for batteries shorter than a day; switch their display unit to minutes in the entity settings for easier reading

## [1.1.0] - 2026-01-02

- Ability to attach new virtual battery to existing devices
- Device assignment can only be set during initial creation (not changeable later)

## [1.0.3] - 2025-12-31

- Now compatible with Home Assistant 2025.x and later

## [1.0.2] - 2025-06-08

- Fix missing imports
- Change unit of measurement for time sensors from "days" to "d"
- Add example use cases to README file

## [1.0.1] - 2025-04-07

- Reorder fields in manifest.json for consistency

## [1.0.0] - 2025-04-06

- Initial release
- Virtual battery functionality with configurable discharge period
- Battery level sensor with state restoration
- Configuration UI with config flow
- Service API for battery control
- Multi-language support (English, German, French)
- HACS support
- Time-based sensors (Time Since Reset, Time Until Empty)
- Battery threshold configurations
- Button entity for battery reset
