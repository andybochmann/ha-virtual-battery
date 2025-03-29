"""Config flow for Virtual Battery integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class VirtualBatteryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Battery."""

    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            # Check if entry with same name already exists
            existing_entries = {
                entry.data.get("name"): entry 
                for entry in self._async_current_entries()
            }
            
            if user_input["name"] in existing_entries:
                errors["name"] = "already_configured"
            else:
                # Validation passed, create the config entry
                return self.async_create_entry(
                    title=user_input["name"],
                    data=user_input,
                )
        
        # Provide a form for the user to fill out
        data_schema = vol.Schema({
            vol.Required("name", default="Virtual Battery"): str,
            vol.Required("discharge_days", default=7): vol.All(
                vol.Coerce(int),
                vol.Range(min=1, max=365)
            ),
            # Add more configuration fields as needed
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )