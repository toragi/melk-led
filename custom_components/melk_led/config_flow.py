from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class MelkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            address = user_input[CONF_ADDRESS].strip().upper()
            name = (user_input.get(CONF_NAME) or address).strip()
            await self.async_set_unique_id(address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=name,
                data={CONF_ADDRESS: address, CONF_NAME: name},
            )

        discovered = []
        for service_info in bluetooth.async_discovered_service_info(self.hass, False):
            name = service_info.name or ""
            if name.upper().startswith(("MELK", "ELK-", "LEDBLE")):
                discovered.append(f"{name} ({service_info.address})")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): str,
                    vol.Optional(CONF_NAME): str,
                }
            ),
            description_placeholders={
                "found": ", ".join(discovered[:8])
                if discovered
                else "пока не найдено — нужен активный Bluetooth proxy",
            },
        )

    async def async_step_bluetooth(self, discovery_info) -> FlowResult:
        address = discovery_info.address
        await self.async_set_unique_id(address)
        self._abort_if_unique_id_configured()
        name = discovery_info.name or address
        return self.async_create_entry(
            title=name,
            data={CONF_ADDRESS: address, CONF_NAME: name},
        )
