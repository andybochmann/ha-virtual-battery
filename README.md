# 🔋 Virtual Battery for Home Assistant

A custom Home Assistant integration that creates a virtual battery with configurable discharge periods.

![GitHub release (latest by date)](https://img.shields.io/github/v/release/andybochmann/ha-virtual-battery)
![HACS Validation](https://img.shields.io/badge/HACS-Custom-orange.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🏷️ Create virtual batteries with custom names
- ⏱️ Configure discharge periods (1-365 days)
- 🔄 Reset battery level to 100%
- 🎚️ Set custom battery levels
- 🔧 Modify discharge periods
- 📊 Track battery level over time
- 🖥️ UI-based configuration
- 📦 HACS installation support
- 🔘 Device with reset button for each battery

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
4. Follow the configuration steps

## 🧰 Usage

After configuration, you'll have a virtual battery device with two entities:
1. A sensor showing the battery level that will automatically discharge over the configured time period
2. A button that can be pressed to reset the battery level to 100%

## 🛠️ Services

The integration provides the following services:

### Reset Battery Level
- **Service**: `virtual_battery.reset_battery_level`
- **Parameters**:
  - `entity_id`: The entity ID of the virtual battery to reset
- **Description**: Resets the battery level to 100%

### Set Battery Level
- **Service**: `virtual_battery.set_battery_level`
- **Parameters**:
  - `entity_id`: The entity ID of the virtual battery to set
  - `battery_level`: The new battery level (0-100)
- **Description**: Sets the battery level to a specific value

### Set Discharge Days
- **Service**: `virtual_battery.set_discharge_days`
- **Parameters**:
  - `entity_id`: The entity ID of the virtual battery to modify
  - `discharge_days`: The new number of discharge days (1-365)
- **Description**: Changes the number of days to discharge the battery

## 📊 Entity Attributes

Each virtual battery entity provides the following attributes:

- `discharge_days`: Number of days to discharge the battery
- `last_reset`: Timestamp of the last battery level reset
- `last_update`: Timestamp of the last battery level update

## 📋 Examples

### Service Call Examples

```yaml
# Reset battery level
service: virtual_battery.reset_battery_level
target:
  entity_id: sensor.my_virtual_battery

# Set battery level to 50%
service: virtual_battery.set_battery_level
target:
  entity_id: sensor.my_virtual_battery
data:
  battery_level: 50

# Set discharge days to 14
service: virtual_battery.set_discharge_days
target:
  entity_id: sensor.my_virtual_battery
data:
  discharge_days: 14
```

### Dashboard Example

```yaml
type: entities
entities:
  - entity: sensor.my_virtual_battery
    secondary_info: last-changed
title: My Virtual Battery
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Credits

Created and maintained by [Andy Bochmann](https://github.com/andybochmann)