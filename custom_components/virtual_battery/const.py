"""Constants for the Virtual Battery integration."""
from datetime import timedelta
from homeassistant.const import CONF_NAME

DOMAIN = "virtual_battery"

# Configuration
CONF_DISCHARGE_DAYS = "discharge_days"
DEFAULT_DISCHARGE_DAYS = 30
MIN_DISCHARGE_DAYS = 1
DEFAULT_NAME = "Virtual Battery"

# Attributes
ATTR_DISCHARGE_DAYS = "discharge_days"
ATTR_LAST_RESET = "last_reset"
ATTR_LAST_UPDATE = "last_update"
ATTR_BATTERY_LEVEL = "battery_level"
ATTR_TIME_SINCE_RESET = "time_since_reset"
ATTR_TIME_UNTIL_EMPTY = "time_until_empty"

# Services
SERVICE_RESET_BATTERY_LEVEL = "reset_battery_level"
SERVICE_SET_BATTERY_LEVEL = "set_battery_level"
SERVICE_SET_DISCHARGE_DAYS = "set_discharge_days"

# Battery Level Thresholds
BATTERY_LEVEL_LOW = 20
BATTERY_LEVEL_CRITICAL = 10
BATTERY_LEVEL_FULL = 100
BATTERY_LEVEL_CHARGING = 95  # Consider battery "full" when reaching this level

# Events
EVENT_BATTERY_LEVEL_LOW = "virtual_battery_low"
EVENT_BATTERY_LEVEL_CRITICAL = "virtual_battery_critical"
EVENT_BATTERY_LEVEL_FULL = "virtual_battery_full"

# Misc
SCAN_INTERVAL = timedelta(minutes=1)
