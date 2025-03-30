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
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
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

class VirtualBatterySensor(SensorEntity, RestoreEntity):
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
        
        # Set up device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=name,
            manufacturer="Virtual Battery",
            model="Virtual Battery Sensor",
            entry_type=DeviceEntryType.SERVICE,
        )
        
        # Don't restore state here - will be done in async_added_to_hass

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        
        # Restore the state after the entity is fully initialized
        await self._async_restore_state_from_last_stored()
        
        # Register update interval
        self.async_on_remove(
            async_track_time_interval(
                self._hass, self._async_update, SCAN_INTERVAL
            )
        )

    async def _async_restore_state_from_last_stored(self):
        """Restore state using RestoreEntity."""
        last_state = await self.async_get_last_state()
        
        if last_state is None:
            _LOGGER.debug("No previous state found for %s", self.entity_id)
            return

        try:
            # Restore attributes
            attrs = last_state.attributes
            
            if ATTR_LAST_RESET in attrs and ATTR_LAST_UPDATE in attrs and ATTR_DISCHARGE_DAYS in attrs:
                self._last_reset = datetime.fromisoformat(attrs[ATTR_LAST_RESET])
                self._last_update = datetime.fromisoformat(attrs[ATTR_LAST_UPDATE])
                self._discharge_days = attrs[ATTR_DISCHARGE_DAYS]
                
                # Try to restore the state value
                if last_state.state not in (None, '', 'unknown', 'unavailable'):
                    try:
                        # Store the restored battery level
                        self._battery_level = float(last_state.state)
                    except (ValueError, TypeError):
                        # Fall back to calculating based on time since last reset
                        self._calculate_discharge_rate()
                        self._calculate_current_battery_level()
                        _LOGGER.warning("Could not convert state %s to float, calculated level: %.2f", 
                                       last_state.state, self._battery_level)
                else:
                    # If state isn't available, calculate based on time since last reset
                    self._calculate_discharge_rate()
                    self._calculate_current_battery_level()
                
                _LOGGER.debug(
                    "Restored state for %s: level=%.2f, discharge_days=%d, last_reset=%s",
                    self.entity_id, 
                    self._battery_level, 
                    self._discharge_days, 
                    self._last_reset.isoformat()
                )
            else:
                _LOGGER.debug("Incomplete state attributes for %s, using defaults", self.entity_id)
                # Ensure we recalculate in this case
                self._calculate_discharge_rate()
                self._calculate_current_battery_level()
        except (ValueError, KeyError) as ex:
            _LOGGER.warning("Error restoring previous state for %s: %s", self.entity_id, ex)
            # Ensure we recalculate in this case
            self._calculate_discharge_rate()
            self._calculate_current_battery_level()

    def _calculate_discharge_rate(self):
        """Calculate the discharge rate based on discharge days."""
        # For X days: 100% / (X days * 24 hours * 60 minutes) * SCAN_INTERVAL_minutes
        self._discharge_per_interval = 100 / (self._discharge_days * 24 * 60) * (SCAN_INTERVAL.total_seconds() / 60)

    def _calculate_current_battery_level(self):
        """Calculate the current battery level based on time since last reset."""
        if self._last_reset:
            current_time = dt_util.utcnow()
            time_since_reset = current_time - self._last_reset
            
            # Ensure time_since_reset is not negative (could happen with clock changes)
            if time_since_reset.total_seconds() < 0:
                _LOGGER.warning("Detected negative time since reset, adjusting to current time")
                self._last_reset = current_time
                time_since_reset = timedelta(seconds=0)
                
            minutes_since_reset = time_since_reset.total_seconds() / 60
            
            # Calculate total discharge since last reset
            total_discharge = (minutes_since_reset / (self._discharge_days * 24 * 60)) * 100
            
            # Update the battery level
            self._battery_level = max(0, 100 - total_discharge)
            
            _LOGGER.debug(
                "Calculated battery level for %s: %.2f%% (minutes since reset: %.2f)",
                self.entity_id,lf.entity_id,
                self._battery_level,                self._battery_level,
                minutes_since_reset
            )

    async def _async_update(self, now=None):    @property
        """Update the battery level based on time passed."""
        previous_level = self._battery_level"""
        y_level, 2)
        if self._battery_level <= 0:
            self._battery_level = 0
            # Also update last_update timestamp for consistent tracking):
            self._last_update = dt_util.utcnow()        """Return the state attributes."""
            
            if previous_level != self._battery_level:ays,
                _LOGGER.debug("%s: Battery reached 0%%", self.entity_id)
                    ATTR_LAST_UPDATE: self._last_update.isoformat(),
            self.async_write_ha_state()
            return
one):
        self._calculate_current_battery_level()ased on time passed."""
        self._last_update = dt_util.utcnow()
        
        # Log significant changes for debuggingnt tracking
        if abs(previous_level - self._battery_level) > 1.0:
            _LOGGER.debug(
                "%s: Battery level changed from %.2f%% to %.2f%% (discharge days: %d, last reset: %s)",
                self.entity_id,
                previous_level,
                self._battery_level,)
                self._discharge_days,.async_write_ha_state()
                self._last_reset.isoformat()
            )elf):
                    """Reset battery level to 100%."""
        self.async_write_ha_state()

    async def async_reset_battery(self):
        """Reset battery level to 100%."""
        self._battery_level = 100
        self._last_reset = dt_util.utcnow()el(self, battery_level):
        self._last_update = dt_util.utcnow()        """Set battery level to specific value."""






























        self.async_write_ha_state()        self._last_update = dt_util.utcnow()        self._calculate_discharge_rate()        self._discharge_days = discharge_days        """Set discharge days to specific value."""    async def async_set_discharge_days(self, discharge_days):        self.async_write_ha_state()        self._last_update = current_time                        self._last_reset = current_time            # If battery is at 100%, reset timestamp is now        else:            self._last_reset = current_time - time_delta            time_delta = timedelta(minutes=minutes_to_discharge)            minutes_to_discharge = (discharge_percentage / 100) * (self._discharge_days * 24 * 60)            discharge_percentage = 100 - self._battery_level            # from a full charge, then set last_reset to that time in the past            # Calculate how much time would have needed to pass to reach this level        if self._battery_level < 100:        current_time = dt_util.utcnow()        # This ensures the discharge calculation will continue from this point correctly        # Calculate and set a new last_reset time based on the manually set battery level                self._battery_level = min(100, max(0, battery_level))        """Set battery level to specific value."""    async def async_set_battery_level(self, battery_level):        self.async_write_ha_state()        self._battery_level = min(100, max(0, battery_level))
        
        # Calculate and set a new last_reset time based on the manually set battery level
        # This ensures the discharge calculation will continue from this point correctly
        current_time = dt_util.utcnow()
        if self._battery_level < 100:
            # Calculate how much time would have needed to pass to reach this level
            # from a full charge, then set last_reset to that time in the past
            discharge_percentage = 100 - self._battery_level
            minutes_to_discharge = (discharge_percentage / 100) * (self._discharge_days * 24 * 60)
            time_delta = timedelta(minutes=minutes_to_discharge)
            self._last_reset = current_time - time_delta
        else:
            # If battery is at 100%, reset timestamp is now
            self._last_reset = current_time
            
        self._last_update = current_time
        self.async_write_ha_state()

    async def async_set_discharge_days(self, discharge_days):
        """Set discharge days to specific value."""
        self._discharge_days = discharge_days
        self._calculate_discharge_rate()
        self._last_update = dt_util.utcnow()
        self.async_write_ha_state()
