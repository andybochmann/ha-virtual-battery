# 📚 Virtual Battery Documentation

## Overview

The Virtual Battery integration allows you to create virtual battery entities in Home Assistant that discharge over time. This can be useful for simulating battery-powered devices, tracking maintenance intervals, or creating visual indicators for various time-based events.

Each virtual battery is created as a device with a sensor entity (the battery level) and a button entity (to reset the battery to 100%).

## How It Works

The virtual battery starts at 100% and gradually decreases to 0% over the configured number of days. The discharge rate is calculated based on the configured discharge period and is updated every minute.

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/andybochmann/ha-virtual-battery` as repository
6. Set category to "Integration"
7. Click "ADD"
8. Search for "Virtual Battery" in the Integrations tab
9. Click "DOWNLOAD"
10. Restart Home Assistant

### Manual Installation

1. Download the latest release from GitHub
2. Extract the `virtual_battery` folder from the zip file
3. Copy this folder to your Home Assistant's `custom_components` directory
4. Restart Home Assistant

## Configuration

### Adding the Integration

1. Go to "Configuration" > "Devices & Services"
2. Click "+ ADD INTEGRATION"
3. Search for "Virtual Battery"
4. Enter a name for your virtual battery
5. Set the discharge period (in days, from 1 to 365)
6. Click "Submit"

### Configuration Options

- **Name**: A friendly name for your virtual battery
- **Discharge Days**: The number of days it takes for the battery to discharge from 100% to 0%

## Services

### `virtual_battery.reset_battery_level`

Resets the battery level to 100%.

**Parameters:**
- `entity_id`: The entity ID of the virtual battery to reset

**Example:**
```yaml
service: virtual_battery.reset_battery_level
target:
  entity_id: sensor.my_virtual_battery
```

### `virtual_battery.set_battery_level`

Sets the battery level to a specific value.

**Parameters:**
- `entity_id`: The entity ID of the virtual battery to set
- `battery_level`: The new battery level (0-100)

**Example:**
```yaml
service: virtual_battery.set_battery_level
target:
  entity_id: sensor.my_virtual_battery
data:
  battery_level: 75
```

### `virtual_battery.set_discharge_days`

Changes the number of days to discharge the battery.

**Parameters:**
- `entity_id`: The entity ID of the virtual battery to modify
- `discharge_days`: The new number of discharge days (1-365)

**Example:**
```yaml
service: virtual_battery.set_discharge_days
target:
  entity_id: sensor.my_virtual_battery
data:
  discharge_days: 30
```

## Attributes

Each virtual battery entity provides the following attributes:

- `discharge_days`: Number of days to discharge the battery
- `last_reset`: Timestamp of the last battery level reset
- `last_update`: Timestamp of the last battery level update

## Entities

### Battery Level Sensor

Each virtual battery creates a sensor entity with the following properties:
- **Device Class**: Battery
- **Unit of Measurement**: %
- **State Class**: Measurement

### Reset Button

Each virtual battery device also includes a button entity that can be pressed to reset the battery level to 100%. This provides a convenient way to reset the battery without calling a service.

## Use Cases

### Maintenance Reminders

Create a virtual battery that discharges over 90 days to track when maintenance is due:
- Reset to 100% when maintenance is performed
- Create an automation to notify you when the battery drops below 10%

### Energy Usage Visualization

Create a virtual battery that represents your daily energy allocation:
- Set to discharge over 1 day
- Reset it daily or when specific conditions are met
- Use it to visualize how much of your daily energy budget has been used

### Plant Watering Tracker

Create a virtual battery that discharges over the typical watering interval for a plant:
- Reset it when you water the plant
- Create an automation to notify you when it's time to water again

## Automations

### Example: Notification when battery is low

```yaml
automation:
  - alias: "Notify when virtual battery is low"
    trigger:
      platform: numeric_state
      entity_id: sensor.my_virtual_battery
      below: 20
    action:
      service: notify.mobile_app
      data:
        title: "Battery Low"
        message: "Virtual battery is below 20%, time to take action!"
```

### Example: Reset battery on schedule

```yaml
automation:
  - alias: "Reset virtual battery every month"
    trigger:
      platform: time
      at: "00:00:00"
    condition:
      condition: time
      weekday:
        - mon
      day: "1"
    action:
      service: virtual_battery.reset_battery_level
      target:
        entity_id: sensor.my_virtual_battery
```

## Troubleshooting

### The battery level isn't updating

- Check that the Home Assistant time is correct
- Restart the integration by going to Configuration > Integrations > Virtual Battery > CONFIGURE

### The battery discharges too quickly or too slowly

- Adjust the discharge days setting using the `virtual_battery.set_discharge_days` service

## Technical Details

### State Persistence

The Virtual Battery integration uses Home Assistant's `RestoreEntity` system to ensure that battery states, including last reset time and discharge days, are properly restored after Home Assistant restarts. This ensures your virtual batteries continue to discharge at the correct rate even after system reboots or service disruptions.

## Support

If you encounter any issues or have feature requests, please [create an issue on GitHub](https://github.com/andybochmann/ha-virtual-battery/issues).
