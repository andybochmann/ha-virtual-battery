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
        super().__init__()
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = name
        self._discharge_days = discharge_days
        self._attr_unique_id = f"{DOMAIN}_{entry_id}"
        
        self._battery_level = 100
        self._last_reset = dt_util.utcnow()
        self._last_update = dt_util.utcnow()
        
        # Calculate discharge rate
        self._calculate_discharge_rate()
        
        # Don't restore state here - will be done in async_added_to_hass

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        
        # Restore the state after the entity is fully initialized
        self._restore_state()
        
        # Register update interval
        self.async_on_remove(
            async_track_time_interval(
                self._hass, self._async_update, SCAN_INTERVAL
            )
        )

    def _calculate_discharge_rate(self):
        """Calculate the discharge rate based on discharge days."""
        # For X days: 100% / (X days * 24 hours * 60 minutes) * SCAN_INTERVAL_minutes
        self._discharge_per_interval = 100 / (self._discharge_days * 24 * 60) * (SCAN_INTERVAL.total_seconds() / 60)

    def _restore_state(self):
        """Restore the state of the sensor from last_reset time."""
        if last_state := self._hass.states.get(self.entity_id):
            try:
                # Restore attributes
                attrs = last_state.attributes
                if ATTR_LAST_RESET in attrs:
                    self._last_reset = datetime.fromisoformat(attrs[ATTR_LAST_RESET])
                    self._last_update = datetime.fromisoformat(attrs[ATTR_LAST_UPDATE])
                    self._discharge_days = attrs[ATTR_DISCHARGE_DAYS]
                    
                    # Recalculate current battery level based on time since last reset
                    self._calculate_discharge_rate()
                    self._calculate_current_battery_level()
                else:
                    # If there was a state but no last_reset attribute, update state attributes
                    self.async_write_ha_state()
            except (ValueError, KeyError) as ex:
                _LOGGER.warning("Error restoring previous state: %s", ex)

    def _calculate_current_battery_level(self):
        """Calculate the current battery level based on time since last reset."""
        if self._last_reset:
            current_time = dt_util.utcnow()
            time_since_reset = current_time - self._last_reset
            minutes_since_reset = time_since_reset.total_seconds() / 60
            
            # Calculate total discharge since last reset
            total_discharge = (minutes_since_reset / (self._discharge_days * 24 * 60)) * 100
            self._battery_level = max(0, 100 - total_discharge)

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
            # Also update last_update timestamp for consistent tracking
            self._last_update = dt_util.utcnow()
            self.async_write_ha_state()
            return

        self._calculate_current_battery_level()
        self._last_update = dt_util.utcnow()
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
        self._calculate_discharge_rate()
        self._last_update = dt_util.utcnow()
        self.async_write_ha_state()
