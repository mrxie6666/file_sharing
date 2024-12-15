import os
import http.server
import socketserver
import threading
import logging
import voluptuous as vol
from homeassistant.const import CONF_PATH, CONF_PORT
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

DOMAIN = "file_sharing"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_PATH): cv.isdir,
                vol.Optional(CONF_PORT, default=8000): cv.port,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data[DOMAIN] = {}

    path = config[DOMAIN][CONF_PATH]
    port = config[DOMAIN][CONF_PORT]

    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = path

    with socketserver.TCPServer(("", port), handler) as httpd:
        _LOGGER.info(f"Serving at port {port}")
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return True