"""Config flow for Virtual Battery integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_DISCHARGE_DAYS,
    DEFAULT_DISCHARGE_DAYS,
    MIN_DISCHARGE_DAYS
)

_LOGGER = logging.getLogger(__name__)

class VirtualBatteryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Battery."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate discharge days
                if not user_input[CONF_DISCHARGE_DAYS] >= MIN_DISCHARGE_DAYS:
                    errors[CONF_DISCHARGE_DAYS] = "discharge_days_invalid"
                else:
                    # Check for duplicate names
                    await self.async_set_unique_id(user_input["name"])
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=user_input["name"],
                        data=user_input,
                    )
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error("Unexpected exception: %s", ex)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required(CONF_DISCHARGE_DAYS, default=DEFAULT_DISCHARGE_DAYS): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=MIN_DISCHARGE_DAYS)
                ),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VirtualBatteryOptionsFlow(config_entry)

class VirtualBatteryOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Virtual Battery."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        errors = {}

        if user_input is not None:
            try:
                if not user_input[CONF_DISCHARGE_DAYS] >= MIN_DISCHARGE_DAYS:
                    errors[CONF_DISCHARGE_DAYS] = "discharge_days_invalid"
                else:
                    # Update data in config entry
                    data = {**self.config_entry.data, CONF_DISCHARGE_DAYS: user_input[CONF_DISCHARGE_DAYS]}
                    self.hass.config_entries.async_update_entry(self.config_entry, data=data)
                    return self.async_create_entry(title="", data=user_input)
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error("Unexpected exception: %s", ex)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_DISCHARGE_DAYS,
                    default=self.config_entry.data.get(CONF_DISCHARGE_DAYS, DEFAULT_DISCHARGE_DAYS)
                ): vol.All(
                    vol.Coerce(int),
                    vol.Range(min=MIN_DISCHARGE_DAYS)
                ),
            }),
            errors=errors,
        )