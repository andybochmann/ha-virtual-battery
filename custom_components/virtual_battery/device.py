"""Attach virtual battery entities to their own device or to a device the user picked."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, Entity

from .const import CONF_TARGET_DEVICE, DOMAIN

try:
    from homeassistant.helpers.helper_integration import async_remove_helper_devices
except ImportError:  # Before HA 2026.8 a device could belong to several config entries.
    async_remove_helper_devices = None

_LOGGER = logging.getLogger(__name__)


@callback
def async_relink_target_device(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Remove the duplicate device HA 2026.8+ keeps for a battery attached the old way."""
    target_id = entry.data.get(CONF_TARGET_DEVICE)
    if async_remove_helper_devices is None or not target_id:
        return
    device_registry = dr.async_get(hass)
    if splits := device_registry.async_get_devices_for_composite_device_id(target_id):
        # HA 2026.8 split devices shared by several config entries, so the stored id now
        # names a composite. Follow it to the split that belongs to the device's owner.
        target = next(
            (split for split in splits if split.config_entry_id == split.composite_primary_config_entry),
            None,
        )
    else:
        target = device_registry.async_get(target_id)
    # Gone, or its owner integration was removed and the device now belongs to this battery:
    # relinking would delete the device itself.
    if target is None or target.config_entry_id == entry.entry_id:
        return
    if target.id != target_id:
        hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_TARGET_DEVICE: target.id})
    async_remove_helper_devices(hass, helper_config_entry_id=entry.entry_id, source_device_id=target.id)


def get_device(
    hass: HomeAssistant, entry_id: str, name: str, target_device_id: str | None
) -> DeviceInfo | dr.DeviceEntry:
    """Return the picked device to attach to, or device info for a standalone device."""
    if target_device_id:
        device = dr.async_get(hass).async_get(target_device_id)
        if device:
            _LOGGER.debug("Attaching virtual battery '%s' to existing device: %s", name, device.name)
            if async_remove_helper_devices:
                # HA 2026.8+: device info carrying another device's identifiers forks a copy.
                return device
            return DeviceInfo(identifiers=device.identifiers)
        _LOGGER.warning(
            "Target device %s not found, creating standalone device for '%s'", target_device_id, name
        )
    return DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        name=name,
        manufacturer="Virtual Battery",
        model="Virtual Battery Sensor",
        entry_type=DeviceEntryType.SERVICE,
    )


def attach_device(entity: Entity, device: DeviceInfo | dr.DeviceEntry) -> None:
    """Attach an entity to what get_device returned."""
    # Check for the entry: DeviceInfo is a TypedDict today but may become a dataclass.
    if isinstance(device, dr.DeviceEntry):
        entity.device_entry = device
    else:
        entity._attr_device_info = device
