# Changelog

All notable changes to the Virtual Battery integration will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Discharge periods shorter than a day: setup and options now use a days/hours/minutes picker, minimum 1 minute (#6, #7)
- `set_discharge_days` service accepts fractional days (e.g. `0.25` for 6 hours) (#7)
- Fix: adding a battery with a name that already exists now shows "already configured" instead of an unknown error (#7)
- Time Since Reset and Time Until Empty sensors show 4 decimals (about 9 seconds) for batteries shorter than a day; switch their display unit to minutes in the entity settings for easier reading (#7)
- Services accept a list of entities, so the `target:` examples in scripts and automations work (#8)
- A battery deleted and re-created with the same name no longer inherits the old battery's level, reset time and period (#9)
- Fix: reset and set-level calls no longer log `hass.helpers` errors, and the time sensors update right away (#10)
- Fix: `virtual_battery_full` now fires; setting the level below 20%/10% fires the low/critical events right away (#10)
- Fix: "Attach to Device" works on Home Assistant 2026.8 and later; duplicate devices from earlier versions are removed (#10)
- The reset button has a battery icon (#11)
- New batteries shorter than a day show their time sensors in minutes (under 2 hours) or hours instead of "0d"

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
