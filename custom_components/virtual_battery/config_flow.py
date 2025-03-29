"""Config flow for Virtual Battery integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import (
    CONF_DISCHARGE_DAYS,
    DEFAULT_DISCHARGE_DAYS,
    DEFAULT_NAME,
    DOMAIN,
    MAX_DISCHARGE_DAYS,
    MIN_DISCHARGE_DAYS,
)

_LOGGER = logging.getLogger(__name__)

class VirtualBatteryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Battery."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate input
            if user_input[CONF_DISCHARGE_DAYS] < MIN_DISCHARGE_DAYS or user_input[CONF_DISCHARGE_DAYS] > MAX_DISCHARGE_DAYS:
                errors[CONF_DISCHARGE_DAYS] = "discharge_days_invalid"
            else:
                # Create unique ID based on name
                await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_NAME]}")
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        # Show the configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                    vol.Required(CONF_DISCHARGE_DAYS, default=DEFAULT_DISCHARGE_DAYS): vol.All(
                        vol.Coerce(int), vol.Range(min=MIN_DISCHARGE_DAYS, max=MAX_DISCHARGE_DAYS)
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return VirtualBatteryOptionsFlow(config_entry)

class VirtualBatteryOptionsFlow(config_entries.OptionsFlow):
    """Handle options for the Virtual Battery integration."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_DISCHARGE_DAYS,
                        default=self.config_entry.data.get(CONF_DISCHARGE_DAYS, DEFAULT_DISCHARGE_DAYS),
                    ): vol.All(vol.Coerce(int), vol.Range(min=MIN_DISCHARGE_DAYS, max=MAX_DISCHARGE_DAYS)),
                }
            ),
        )
