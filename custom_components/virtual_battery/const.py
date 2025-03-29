"""Constants for the Virtual Battery integration."""
from datetime import timedelta
from homeassistant.const import CONF_NAME

DOMAIN = "virtual_battery"

# Configuration
CONF_DISCHARGE_DAYS = "discharge_days"
DEFAULT_DISCHARGE_DAYS = 30
MIN_DISCHARGE_DAYS = 1
MAX_DISCHARGE_DAYS = 365
DEFAULT_NAME = "Virtual Battery"

# Attributes
ATTR_DISCHARGE_DAYS = "discharge_days"
ATTR_LAST_RESET = "last_reset"
ATTR_LAST_UPDATE = "last_update"
ATTR_BATTERY_LEVEL = "battery_level"

# Services
SERVICE_RESET_BATTERY_LEVEL = "reset_battery_level"
SERVICE_SET_BATTERY_LEVEL = "set_battery_level"
SERVICE_SET_DISCHARGE_DAYS = "set_discharge_days"

# Misc
SCAN_INTERVAL = timedelta(minutes=1)
