"""Config flow for Virtual Battery integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv, device_registry as dr
from homeassistant.helpers.selector import (
    DeviceSelector,
    DeviceSelectorConfig,
    DurationSelector,
    DurationSelectorConfig,
)

from .const import (
    DOMAIN,
    CONF_DISCHARGE_DAYS,
    CONF_TARGET_DEVICE,
    DEFAULT_DISCHARGE_DAYS,
    MIN_DISCHARGE_DAYS
)

_LOGGER = logging.getLogger(__name__)

DURATION_SELECTOR = DurationSelector(DurationSelectorConfig(enable_day=True))


def _duration_to_days(duration: dict) -> float:
    """Convert a duration selector value to fractional days."""
    return cv.time_period_dict(duration).total_seconds() / 86400


def _days_to_duration(days: float) -> dict:
    """Convert fractional days to a duration selector value."""
    total_seconds = round(days * 86400)
    whole_days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return {"days": whole_days, "hours": hours, "minutes": minutes, "seconds": seconds}

class VirtualBatteryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Battery."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                discharge_days = _duration_to_days(user_input[CONF_DISCHARGE_DAYS])
                if discharge_days < MIN_DISCHARGE_DAYS:
                    errors[CONF_DISCHARGE_DAYS] = "discharge_days_invalid"
                else:
                    # Validate target device exists if specified
                    target_device = user_input.get(CONF_TARGET_DEVICE)
                    if target_device:
                        device_registry = dr.async_get(self.hass)
                        device = device_registry.async_get(target_device)
                        if device is None:
                            errors[CONF_TARGET_DEVICE] = "device_not_found"
                    
                    if not errors:
                        # Check for duplicate names
                        await self.async_set_unique_id(user_input["name"])
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=user_input["name"],
                            data={**user_input, CONF_DISCHARGE_DAYS: discharge_days},
                        )
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error("Unexpected exception: %s", ex)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required(
                    CONF_DISCHARGE_DAYS, default=_days_to_duration(DEFAULT_DISCHARGE_DAYS)
                ): DURATION_SELECTOR,
                vol.Optional(CONF_TARGET_DEVICE): DeviceSelector(
                    DeviceSelectorConfig()
                ),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VirtualBatteryOptionsFlow()

class VirtualBatteryOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Virtual Battery."""

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        errors = {}

        if user_input is not None:
            try:
                discharge_days = _duration_to_days(user_input[CONF_DISCHARGE_DAYS])
                if discharge_days < MIN_DISCHARGE_DAYS:
                    errors[CONF_DISCHARGE_DAYS] = "discharge_days_invalid"
                else:
                    # Update data in config entry
                    data = {**self.config_entry.data, CONF_DISCHARGE_DAYS: discharge_days}
                    self.hass.config_entries.async_update_entry(self.config_entry, data=data)
                    return self.async_create_entry(title="", data={CONF_DISCHARGE_DAYS: discharge_days})
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error("Unexpected exception: %s", ex)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_DISCHARGE_DAYS,
                    default=_days_to_duration(
                        self.config_entry.data.get(CONF_DISCHARGE_DAYS, DEFAULT_DISCHARGE_DAYS)
                    )
                ): DURATION_SELECTOR,
            }),
            errors=errors,
        )