# Virtual Battery - AI Coding Agent Instructions

## Project Overview

Home Assistant custom component that simulates a virtual battery with configurable discharge periods. Useful for tracking battery replacement intervals for non-smart devices (smoke detectors, remotes, key finders).

**Platform**: Home Assistant integration (HACS-compatible)  
**Version**: 1.0.2 (see [manifest.json](../custom_components/virtual_battery/manifest.json))  
**Min HA Version**: 2023.8.0

## Architecture & Data Flow

### Entity Structure

Each virtual battery instance creates **one device** with **four entities**:

1. **Battery Level Sensor** (`VirtualBatterySensor`) - Main sensor with auto-discharge logic
2. **Time Since Reset Sensor** (`TimeSinceResetSensor`) - Tracks days since last reset
3. **Time Until Empty Sensor** (`TimeUntilEmptySensor`) - Estimates remaining discharge time
4. **Reset Button** (`VirtualBatteryResetButton`) - One-click reset to 100%

All entities share the same `DeviceInfo` identifier: `(DOMAIN, entry_id)`

### State Management Pattern

Battery state persists across HA restarts using `RestoreEntity`:

- State restoration happens in `async_added_to_hass()` via `_async_restore_state_from_last_stored()`
- Critical attributes: `last_reset` (ISO datetime), `last_update` (ISO datetime), `discharge_days` (int)
- Battery level is **calculated**, not stored - computed from `last_reset` timestamp and `discharge_days`
- Handles edge cases: NaN values, infinite values, negative time deltas (clock changes)

### Service Architecture

Three services registered in `__init__.py` that locate entities via `hass.data[DOMAIN]["entities"]` list:

- `reset_battery_level` - Resets to 100%, updates `last_reset` to now
- `set_battery_level` - **Backdates `last_reset`** to make level calculation accurate going forward
- `set_discharge_days` - Updates discharge rate, recalculates discharge per interval

### Event System

Battery fires HA bus events when crossing thresholds (direction matters):

- `virtual_battery_full` - Battery rises to ≥95% (threshold: `BATTERY_LEVEL_CHARGING`)
- `virtual_battery_low` - Battery drops below 20% (threshold: `BATTERY_LEVEL_LOW`)
- `virtual_battery_critical` - Battery drops below 10% (threshold: `BATTERY_LEVEL_CRITICAL`)

Events include `entity_id` and `battery_level` in data payload.

## Development Patterns

### Discharge Calculation Logic

Battery level is time-based, not interval-based:

```python
# From sensor.py
discharge_percentage = (minutes_since_reset / (discharge_days * 24 * 60)) * 100
battery_level = 100 - discharge_percentage
```

Update interval: `SCAN_INTERVAL = timedelta(minutes=1)` (from [const.py](../custom_components/virtual_battery/const.py))

### Config Flow Pattern

- Uses `async_set_unique_id(user_input["name"])` to prevent duplicate battery names
- Options flow updates config entry data directly: `hass.config_entries.async_update_entry()`
- Changes propagate via `async_update_options()` listener in `__init__.py`

### Entity Registration

Sensors must self-register in `hass.data[DOMAIN]["entities"]` list for service discovery:

```python
# From sensor.py async_setup_entry
hass.data[DOMAIN]["entities"].append(battery_sensor)
```

Time sensors reference their parent battery sensor, NOT the hass.data list.

## File Responsibilities

- **[**init**.py](../custom_components/virtual_battery/__init__.py)** - Entry setup, service registration, options update listener
- **[sensor.py](../custom_components/virtual_battery/sensor.py)** - Battery level calculation, state restoration, event firing, time sensors
- **[button.py](../custom_components/virtual_battery/button.py)** - Reset button entity that finds matching sensor by entry_id
- **[config_flow.py](../custom_components/virtual_battery/config_flow.py)** - User/options flows, validation
- **[const.py](../custom_components/virtual_battery/const.py)** - All constants, thresholds, service names
- **[services.yaml](../custom_components/virtual_battery/services.yaml)** - Service UI definitions for HA Developer Tools

## Testing & Debugging

### Manual Testing Workflow

1. Copy `custom_components/virtual_battery/` to HA config directory
2. Restart Home Assistant
3. Add integration via UI: Settings → Devices & Services → Add Integration
4. Test services in Developer Tools → Services
5. Monitor logs: `homeassistant.components.virtual_battery` logger

### Common Issues

- **Battery level jumps after restart**: Check `last_reset` persistence in state attributes
- **Services not working**: Verify entity is in `hass.data[DOMAIN]["entities"]` list (add debug log)
- **Time sensors not updating**: Ensure `_notify_sensors()` is called after battery changes
- **Negative time since reset**: Clock change detected - code handles by resetting `last_reset` to now

## Conventions

### Code Style

- Use `_LOGGER.debug()` for calculation details (e.g., battery level changes >1%)
- Use `_LOGGER.warning()` for state restoration failures or missing entities
- All datetime objects use `dt_util.utcnow()` for timezone consistency
- Validate numeric values with `_validate_value()` helper to handle NaN/infinity

### Naming

- Entity names: `{user_name} Battery Level`, `{user_name} Time Since Reset`
- Unique IDs: `{DOMAIN}_{entry_id}`, `{DOMAIN}_{entry_id}_time_since_reset`
- Attributes use `ATTR_*` constants from const.py (e.g., `ATTR_DISCHARGE_DAYS`)

### Translation Structure

Translations in `translations/{lang}.json` follow Home Assistant i18n pattern. Keys match config flow step IDs and error codes.

## Dependencies & Integration

- **No external Python packages** (requirements: [])
- **Core HA APIs**: `RestoreEntity`, `SensorEntity`, `ButtonEntity`, config_entries, device_registry
- **HACS Metadata**: [hacs.json](../hacs.json) defines minimum HACS version (1.6.0)

## Making Changes

When modifying discharge logic, remember:

1. Update `_calculate_discharge_rate()` for new discharge calculation
2. Update `_calculate_current_battery_level()` to apply new rate
3. Ensure `set_battery_level()` still backdates `last_reset` correctly
4. Test state restoration to verify calculations persist correctly

When adding new services:

1. Define constant in [const.py](../custom_components/virtual_battery/const.py)
2. Register handler in [**init**.py](../custom_components/virtual_battery/__init__.py) `async_setup_entry()`
3. Add UI definition to [services.yaml](../custom_components/virtual_battery/services.yaml)
4. Update [README.md](../README.md) with examples

When adding new entity types:

1. Add platform to `PLATFORMS` list in [**init**.py](../custom_components/virtual_battery/__init__.py)
2. Create new `{platform}.py` file with `async_setup_entry()`
3. Ensure entity shares same `DeviceInfo` identifier
4. Register in `hass.data[DOMAIN]["entities"]` if needs service access
