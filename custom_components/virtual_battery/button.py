"""Button platform for the Virtual Battery integration."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Virtual Battery button."""
    name = entry.data[CONF_NAME]
    
    button = VirtualBatteryResetButton(hass, entry.entry_id, name)
    async_add_entities([button])

class VirtualBatteryResetButton(ButtonEntity):
    """Implementation of a Virtual Battery Reset button."""

    def __init__(self, hass, entry_id, name):
        """Initialize the Virtual Battery Reset button."""
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = f"{name} Reset"
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_reset"
        
        # Set up device info to associate with the same device as the sensor
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
        )

    async def async_press(self) -> None:
        """Handle the button press - reset the battery to 100%."""
        if DOMAIN in self._hass.data and "entities" in self._hass.data[DOMAIN]:
            for entity in self._hass.data[DOMAIN]["entities"]:
                if entity._entry_id == self._entry_id:
                    await entity.async_reset_battery()
                    _LOGGER.debug("Reset button pressed for %s", self._attr_name)
                    break
