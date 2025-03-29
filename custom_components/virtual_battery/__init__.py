"""The Virtual Battery integration."""
import asyncio
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
    MAX_DISCHARGE_DAYS,
    MIN_DISCHARGE_DAYS,
    SERVICE_RESET_BATTERY_LEVEL,
    SERVICE_SET_BATTERY_LEVEL,
    SERVICE_SET_DISCHARGE_DAYS,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Virtual Battery component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Virtual Battery from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    async def reset_battery_level(call: ServiceCall) -> None:
        """Reset battery level to 100%."""
        entity_id = call.data.get("entity_id")
        
        if not entity_id:
            _LOGGER.error("Missing entity_id in reset_battery_level service call")
            return
            
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                if entity.entity_id == entity_id:
                    await entity.async_reset_battery()
                    _LOGGER.info("Reset battery level for %s", entity_id)
                    break
            else:
                _LOGGER.error("Entity %s not found for reset_battery_level service", entity_id)

    async def set_battery_level(call: ServiceCall) -> None:
        """Set battery level to specified value."""
        entity_id = call.data.get("entity_id")
        battery_level = call.data.get(ATTR_BATTERY_LEVEL)
        
        if not entity_id:
            _LOGGER.error("Missing entity_id in set_battery_level service call")
            return
            
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                if entity.entity_id == entity_id:
                    await entity.async_set_battery_level(battery_level)
                    _LOGGER.info("Set battery level to %s for %s", battery_level, entity_id)
                    break
            else:
                _LOGGER.error("Entity %s not found for set_battery_level service", entity_id)

    async def set_discharge_days(call: ServiceCall) -> None:
        """Set discharge days to specified value."""
        entity_id = call.data.get("entity_id")
        discharge_days = call.data.get(ATTR_DISCHARGE_DAYS)
        
        if not entity_id:
            _LOGGER.error("Missing entity_id in set_discharge_days service call")
            return
            
        if "entities" in hass.data[DOMAIN]:
            for entity in hass.data[DOMAIN]["entities"]:
                if entity.entity_id == entity_id:
                    await entity.async_set_discharge_days(discharge_days)
                    _LOGGER.info("Set discharge days to %s for %s", discharge_days, entity_id)
                    break
            else:
                _LOGGER.error("Entity %s not found for set_discharge_days service", entity_id)

    # Register services
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
                vol.Coerce(int), vol.Range(min=MIN_DISCHARGE_DAYS, max=MAX_DISCHARGE_DAYS)
            ),
        })
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
