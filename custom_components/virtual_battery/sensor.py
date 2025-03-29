"""Sensor platform for the Virtual Battery integration."""
import logging
from datetime import datetime, timedelta
import voluptuous as vol

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_DISCHARGE_DAYS,
    ATTR_LAST_RESET,
    ATTR_LAST_UPDATE,
    CONF_DISCHARGE_DAYS,
    DOMAIN,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Virtual Battery sensor."""
    name = entry.data[CONF_NAME]
    discharge_days = entry.data[CONF_DISCHARGE_DAYS]
    
    sensor = VirtualBatterySensor(hass, entry.entry_id, name, discharge_days)
    async_add_entities([sensor])

    # Store sensor instance in hass.data for service access
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if "entities" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["entities"] = []
    hass.data[DOMAIN]["entities"].append(sensor)

class VirtualBatterySensor(SensorEntity):
    """Implementation of a Virtual Battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, hass, entry_id, name, discharge_days):
        """Initialize the Virtual Battery sensor."""
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = name
        self._discharge_days = discharge_days
        self._attr_unique_id = f"{DOMAIN}_{name}"
        
        self._battery_level = 100
        self._last_reset = dt_util.utcnow()
        self._last_update = dt_util.utcnow()
        
        # Calculate discharge rate
        # For X days: 100% / (X days * 24 hours * 60 minutes) * SCAN_INTERVAL_minutes
        self._discharge_per_interval = 100 / (discharge_days * 24 * 60) * (SCAN_INTERVAL.total_seconds() / 60)
        
        # Register update interval
        async_track_time_interval(
            hass, self._async_update, SCAN_INTERVAL
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return round(self._battery_level, 2)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_DISCHARGE_DAYS: self._discharge_days,
            ATTR_LAST_RESET: self._last_reset.isoformat(),
            ATTR_LAST_UPDATE: self._last_update.isoformat(),
        }

    async def _async_update(self, now=None):
        """Update the battery level based on time passed."""
        if self._battery_level <= 0:
            self._battery_level = 0
            return

        # Calculate time since last update
        current_time = dt_util.utcnow()
        
        # Only discharge if some time has passed
        if self._last_update:
            time_delta = current_time - self._last_update
            intervals_passed = time_delta.total_seconds() / SCAN_INTERVAL.total_seconds()
            discharge_amount = self._discharge_per_interval * intervals_passed
            
            self._battery_level = max(0, self._battery_level - discharge_amount)
            self._last_update = current_time
            
            self.async_write_ha_state()

    async def async_reset_battery(self):
        """Reset battery level to 100%."""
        self._battery_level = 100
        self._last_reset = dt_util.utcnow()
        self._last_update = dt_util.utcnow()
        self.async_write_ha_state()

    async def async_set_battery_level(self, battery_level):
        """Set battery level to specific value."""
        self._battery_level = min(100, max(0, battery_level))
        self._last_update = dt_util.utcnow()
        self.async_write_ha_state()

    async def async_set_discharge_days(self, discharge_days):
        """Set discharge days to specific value."""
        self._discharge_days = discharge_days
        self._discharge_per_day = 100 / discharge_days
        self._discharge_per_interval = self._discharge_per_day / (24 * 60 / SCAN_INTERVAL.total_seconds() / 60)
        self._last_update = dt_util.utcnow()
        self.async_write_ha_state()
