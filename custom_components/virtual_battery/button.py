"""Button platform for the Virtual Battery integration."""
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, CONF_TARGET_DEVICE

_LOGGER = logging.getLogger(__name__)


def get_button_device_info(hass: HomeAssistant, entry_id: str, target_device_id: str | None) -> DeviceInfo:
    """Get device info for button, either for existing device or the virtual battery device."""
    if target_device_id:
        device_registry = dr.async_get(hass)
        device = device_registry.async_get(target_device_id)
        if device:
            # Return DeviceInfo that will attach to the existing device
            return DeviceInfo(
                identifiers=device.identifiers,
            )
        else:
            _LOGGER.warning(
                "Target device %s not found for button, using virtual battery device",
                target_device_id
            )
    
    # Use the virtual battery device identifiers
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Virtual Battery button."""
    name = entry.data[CONF_NAME]
    target_device = entry.data.get(CONF_TARGET_DEVICE)
    
    # Get device info (either for existing device or virtual battery device)
    device_info = get_button_device_info(hass, entry.entry_id, target_device)
    
    button = VirtualBatteryResetButton(hass, entry.entry_id, name, device_info)
    async_add_entities([button])

class VirtualBatteryResetButton(ButtonEntity, RestoreEntity):
    """Implementation of a Virtual Battery Reset button."""

    def __init__(self, hass, entry_id, name, device_info: DeviceInfo):
        """Initialize the Virtual Battery Reset button."""
        self._hass = hass
        self._entry_id = entry_id
        self._attr_name = f"{name} Reset"
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_reset"
        
        # Set up device info (passed in from setup to handle target device logic)
        self._attr_device_info = device_info

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        
        # Restore state is typically less important for a button,
        # but it's good practice to implement for consistency
        await self.async_get_last_state()

    async def async_press(self) -> None:
        """Handle the button press - reset the battery to 100%."""
        if DOMAIN in self._hass.data and "entities" in self._hass.data[DOMAIN]:
            for entity in self._hass.data[DOMAIN]["entities"]:
                if hasattr(entity, '_entry_id') and entity._entry_id == self._entry_id:
                    await entity.async_reset_battery()
                    _LOGGER.debug("Reset button pressed for %s", self._attr_name)
                    return
            _LOGGER.warning("Could not find matching sensor entity for button %s", self._attr_name)
