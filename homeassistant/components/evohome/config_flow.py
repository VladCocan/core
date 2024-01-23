import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN
import evohomeasync2 as evo  # or evohomeasync if using the first version

class EvoHomeEUConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """EvoHomeEU configuration flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            # Validate the user input
            valid = await self.validate_input(user_input)
            if valid:
                return self.async_create_entry(title="EvoHomeEU", data=user_input)
            else:
                errors["base"] = "auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
            }),
            errors=errors,
        )

    async def validate_input(self, user_input):
        """Validate user input."""
        try:
            client = evo.EvohomeClient(
                user_input["username"],
                user_input["password"]
            )
            await client.login()
            return True
        except evo.AuthenticationError:
            return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EvoHomeEUOptionsFlowHandler(config_entry)

class EvoHomeEUOptionsFlowHandler(config_entries.OptionsFlow):
    """EvoHomeEU options flow handler."""

    def __init__(self, config_entry):
        """Initialize EvoHomeEU options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the EvoHomeEU options."""
        # Implement your options logic here
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
