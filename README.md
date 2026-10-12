# 🔋 Virtual Battery for Home Assistant

A custom Home Assistant integration that creates a virtual battery with configurable discharge periods.

![GitHub release (latest by date)](https://img.shields.io/github/v/release/andybochmann/ha-virtual-battery)
![HACS Validation](https://img.shields.io/badge/HACS-Integration-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=andybochmann&repository=ha-virtual-battery&category=integration)

## ✨ Features

- 🏷️ Create virtual batteries with custom names
- ⏱️ Configure discharge periods (1 minute or more)
- 🔄 Reset battery level to 100%
- 🎚️ Set custom battery levels
- 🔧 Modify discharge periods
- 📊 Track battery level over time
- 🖥️ UI-based configuration
- 📦 HACS installation support
- 🔘 Device with reset button for each battery
- 🔗 **Attach to existing devices** - Add battery tracking to devices that don't natively report battery status

## 📥 Installation

### HACS Installation

1. Add this repository as a custom repository in HACS
2. Search for "Virtual Battery" in HACS and install it
3. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Extract the folder `virtual_battery` from the archive to: `<your-home-assistant-path>/config/custom_components/`
3. Restart Home Assistant

## ⚙️ Configuration

Configure the integration through the UI:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Virtual Battery**
4. Follow the configuration steps:
   - **Battery Name**: A unique name for your virtual battery
   - **Discharge Period**: How long the battery takes to fully discharge (days, hours, minutes, seconds; minimum 1 minute)
   - **Attach to Device** (optional): Select an existing device to add the battery entities to

### Attaching to Existing Devices

You can optionally attach the virtual battery entities to an existing device in Home Assistant. This is useful for:

- Adding battery tracking to devices that don't natively report battery status
- Keeping all related entities grouped under one device
- Maintaining a cleaner device list

If you leave the device selector empty, a new standalone "Virtual Battery" device will be created (default behavior).

**Important Limitations:**

- Device assignment can **only be set during initial creation** and cannot be changed later through the options flow
- If you need to change the device assignment, you must delete the virtual battery integration and recreate it with the new device selection
- If the target device is later removed from Home Assistant, the virtual battery entities will automatically fall back to a standalone device on the next restart
- On Home Assistant 2026.8 and later, attached entities are named after the chosen device (for example "Hallway Smoke Detector Smoke Battery Level"); entity IDs you already use don't change. Batteries attached with earlier versions of this integration are moved back onto the chosen device automatically

## 💡 Example Use Cases

Virtual Battery is useful for devices that do not natively report battery status but require regular replacement or recharging. Some example scenarios:

- **Smoke Detectors:** Track battery replacement intervals for detectors that lack smart battery reporting.
- **Remote Controls:** Set up reminders to replace or recharge batteries in remotes that aren't integrated with Home Assistant.
- **Key Finders/Trackers:** Monitor battery change intervals for Bluetooth trackers or key finders.
- **Short Timers:** Use a discharge period of a few minutes or hours and trigger announcements from the low/critical battery events.

By configuring a virtual battery with an appropriate discharge period, you can automate reminders and maintenance tasks for any device that needs regular attention.

## 🧰 Usage

After configuration, you'll have a virtual battery device with four entities (for a battery named "My Virtual Battery"):

1. `sensor.my_virtual_battery_battery_level`: the battery level, which discharges over the configured period
2. `sensor.my_virtual_battery_time_since_reset`: days since the last reset
3. `sensor.my_virtual_battery_time_until_empty`: days until the battery is empty
4. `button.my_virtual_battery_reset`: resets the battery level to 100%

The battery level updates once a minute. Very short discharge periods (under about 100 minutes) therefore drop in visible steps, e.g. a 10-minute battery loses 10% per update.

The two time sensors show minutes for discharge periods under 2 hours, hours for periods under a day, and days otherwise. Home Assistant picks this unit once, when the battery is created, so a battery whose period you change later (or one created with an earlier version) keeps its unit. To change it, open the sensor's settings in Home Assistant and pick another unit of measurement.

## 🛠️ Services

The integration provides the following services:

### Reset Battery Level

- **Service**: `virtual_battery.reset_battery_level`
- **Parameters**:
  - `entity_id`: One or more virtual battery level sensors to reset
- **Description**: Resets the battery level to 100%

### Set Battery Level

- **Service**: `virtual_battery.set_battery_level`
- **Parameters**:
  - `entity_id`: One or more virtual battery level sensors to set
  - `battery_level`: The new battery level (0-100)
- **Description**: Sets the battery level to a specific value

### Set Discharge Days

- **Service**: `virtual_battery.set_discharge_days`
- **Parameters**:
  - `entity_id`: One or more virtual battery level sensors to modify
  - `discharge_days`: The new number of discharge days. Decimals are allowed, e.g. `0.25` for 6 hours (minimum 1 minute, about `0.0007`)
- **Description**: Changes the number of days to discharge the battery

## 📊 Entity Attributes

Each virtual battery entity provides the following attributes:

- `discharge_days`: Number of days to discharge the battery (can be fractional, e.g. `0.25` for 6 hours)
- `last_reset`: Timestamp of the last battery level reset
- `last_update`: Timestamp of the last battery level update

## 📋 Examples

### Service Call Examples

```yaml
# Reset battery level
service: virtual_battery.reset_battery_level
target:
  entity_id: sensor.my_virtual_battery_battery_level

# Set battery level to 50%
service: virtual_battery.set_battery_level
target:
  entity_id: sensor.my_virtual_battery_battery_level
data:
  battery_level: 50

# Set discharge days to 14
service: virtual_battery.set_discharge_days
target:
  entity_id: sensor.my_virtual_battery_battery_level
data:
  discharge_days: 14
```

### Dashboard Example

```yaml
type: entities
entities:
  - entity: sensor.my_virtual_battery_battery_level
    secondary_info: last-changed
title: My Virtual Battery
```

## 📱 Dashboard Examples

### Basic Card

```yaml
type: entities
entities:
  - entity: sensor.my_virtual_battery_battery_level
    secondary_info: last-changed
  - entity: sensor.my_virtual_battery_time_since_reset
  - entity: sensor.my_virtual_battery_time_until_empty
title: My Virtual Battery
```

### Battery Card with Gauge

```yaml
type: vertical-stack
cards:
  - type: gauge
    entity: sensor.my_virtual_battery_battery_level
    min: 0
    max: 100
    severity:
      green: 50
      yellow: 20
      red: 10
  - type: entities
    entities:
      - entity: sensor.my_virtual_battery_time_since_reset
      - entity: sensor.my_virtual_battery_time_until_empty
```

### Template Examples

```yaml
# Format time since reset in a human-readable format
sensor:
  - platform: template
    sensors:
      virtual_battery_time_readable:
        friendly_name: "Battery Age"
        value_template: >
          {% set days = states('sensor.my_virtual_battery_time_since_reset') | float %}
          {% set total_hours = (days * 24) | round(0) %}
          {% set days_part = ((total_hours / 24) | int) %}
          {% set hours_part = (total_hours % 24) | int %}
          {% if days_part > 0 %}
            {{ days_part }}d {{ hours_part }}h
          {% else %}
            {{ hours_part }}h
          {% endif %}
```

## 🔄 Automation Examples

### Notify on Low Battery

```yaml
automation:
  - alias: "Virtual Battery Low"
    trigger:
      platform: numeric_state
      entity_id: sensor.my_virtual_battery_battery_level
      below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Virtual Battery Low"
          message: "Battery level is {{ states('sensor.my_virtual_battery_battery_level') }}%"
          data:
            icon: mdi:battery-low

  # Alternatively using the event:
  - alias: "Virtual Battery Critical"
    trigger:
      platform: event
      event_type: virtual_battery_critical
    action:
      - service: notify.mobile_app
        data:
          title: "Virtual Battery Critical!"
          message: "Battery {{ trigger.event.data.entity_id }} is critically low at {{ trigger.event.data.battery_level }}%"
```

### Reset Battery on Schedule

```yaml
automation:
  - alias: "Reset Virtual Battery Weekly"
    trigger:
      platform: time
      at: "00:00:00"
    condition:
      condition: time
      weekday: "monday"
    action:
      - service: virtual_battery.reset_battery_level
        target:
          entity_id: sensor.my_virtual_battery_battery_level
```

### Adjust Discharge Days Based on Season

```yaml
automation:
  - alias: "Adjust Battery Discharge - Summer"
    trigger:
      platform: time
      at: "00:00:00"
    condition:
      condition: sun
      after: summer_solstice
      before: winter_solstice
    action:
      - service: virtual_battery.set_discharge_days
        target:
          entity_id: sensor.my_virtual_battery_battery_level
        data:
          discharge_days: 45 # Longer discharge in summer
```

## 🎯 Events

The integration fires events when battery levels cross certain thresholds:

### Battery Full Event

- **Event**: `virtual_battery_full`
- **Triggered**: When battery level rises to 95% or above
- **Data**:
  - `entity_id`: The entity ID of the virtual battery
  - `battery_level`: Current battery level

### Low Battery Event

- **Event**: `virtual_battery_low`
- **Triggered**: When battery level drops below 20%
- **Data**:
  - `entity_id`: The entity ID of the virtual battery
  - `battery_level`: Current battery level

### Critical Battery Event

- **Event**: `virtual_battery_critical`
- **Triggered**: When battery level drops below 10%
- **Data**:
  - `entity_id`: The entity ID of the virtual battery
  - `battery_level`: Current battery level

### Example Automation Using Events

```yaml
automation:
  - alias: "Virtual Battery Low Alert"
    trigger:
      platform: event
      event_type: virtual_battery_low
    action:
      - service: notify.mobile_app
        data:
          title: "Low Battery Alert"
          message: "Virtual Battery {{ trigger.event.data.entity_id }} is at {{ trigger.event.data.battery_level }}%"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Credits

Created and maintained by [Andy Bochmann](https://github.com/andybochmann)
