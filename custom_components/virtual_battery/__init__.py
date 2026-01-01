"""The Virtual Battery integration."""
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_BATTERY_LEVEL,
    ATTR_DISCHARGE_DAYS,
    CONF_DISCHARGE_DAYS,
    DOMAIN,
    MIN_DISCHARGE_DAYS,
    SERVICE_RESET_BATTERY_LEVEL,
    SERVICE_SET_BATTERY_LEVEL,
    SERVICE_SET_DISCHARGE_DAYS,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BUTTON]

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


def _register_services(hass: HomeAssistant) -> None:
    """Register services for the Virtual Battery integration."""
    
    async def reset_battery_level(call: ServiceCall) -> None:
        """Reset battery level to 100%."""
        entity_id = call.data["entity_id"]
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                if entity.entity_id == entity_id:
                    await entity.async_reset_battery()
                    break

    async def set_battery_level(call: ServiceCall) -> None:
        """Set battery level to specified value."""
        entity_id = call.data["entity_id"]
        battery_level = call.data.get(ATTR_BATTERY_LEVEL)
        
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                if entity.entity_id == entity_id:
                    await entity.async_set_battery_level(battery_level)
                    break

    async def set_discharge_days(call: ServiceCall) -> None:
        """Set discharge days to specified value."""
        entity_id = call.data["entity_id"]
        discharge_days = call.data.get(ATTR_DISCHARGE_DAYS)
        
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                if entity.entity_id == entity_id:
                    await entity.async_set_discharge_days(discharge_days)
                    break

    hass.services.async_register(
        DOMAIN, SERVICE_RESET_BATTERY_LEVEL, reset_battery_level,
        schema=vol.Schema({
            vol.Required("entity_id"): cv.entity_id,
        })
    )
    
    hass.services.async_register(
        DOMAIN, 
        SERVICE_SET_BATTERY_LEVEL, 
        set_battery_level, 
        schema=vol.Schema({
            vol.Required("entity_id"): cv.entity_id,
            vol.Required(ATTR_BATTERY_LEVEL): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=100)
            ),
        })
    )
    
    hass.services.async_register(
        DOMAIN, 
        SERVICE_SET_DISCHARGE_DAYS, 
        set_discharge_days,
        schema=vol.Schema({
            vol.Required("entity_id"): cv.entity_id,
            vol.Required(ATTR_DISCHARGE_DAYS): vol.All(
                vol.Coerce(int), vol.Range(min=MIN_DISCHARGE_DAYS)
            ),
        })
    )


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Virtual Battery component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Virtual Battery from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Ensure we have a consistent data structure
    if "entities" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["entities"] = []
    
    # Register services only once (when first entry is set up)
    if not hass.services.has_service(DOMAIN, SERVICE_RESET_BATTERY_LEVEL):
        _register_services(hass)
        
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for config entry changes
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True

async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    try:
        # Update data structure with new options
        hass.data[DOMAIN][entry.entry_id] = entry.data
        
        # Find and update the entity associated with this entry
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                try:
                    if entity._entry_id == entry.entry_id:
                        # Update entity with new discharge days
                        if CONF_DISCHARGE_DAYS in entry.data:
                            await entity.async_set_discharge_days(entry.data[CONF_DISCHARGE_DAYS])
                            _LOGGER.debug(
                                "Updated discharge days for %s to %d from config entry",
                                entity.entity_id,
                                entry.data[CONF_DISCHARGE_DAYS],
                            )
                except Exception as entity_ex:
                    _LOGGER.error(
                        "Failed to update entity %s with new options: %s",
                        entity.entity_id if hasattr(entity, 'entity_id') else 'unknown',
                        entity_ex
                    )
    except Exception as ex:
        _LOGGER.error("Failed to update options for entry %s: %s", entry.entry_id, ex)
        # Re-raise to ensure Home Assistant knows the update failed
        raise

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        
        # Remove entities associated with this entry from the entities list
        if "entities" in hass.data[DOMAIN]:
            hass.data[DOMAIN]["entities"] = [
                entity for entity in hass.data[DOMAIN]["entities"]
                if not (hasattr(entity, '_entry_id') and entity._entry_id == entry.entry_id)
            ]

    return unload_ok
