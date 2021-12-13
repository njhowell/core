"""Platform for light integration."""
from __future__ import annotations

import logging


from njhowell_busylight import Auth, BusyLightAPI
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import (ATTR_BRIGHTNESS, PLATFORM_SCHEMA,
                                            LightEntity)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_USERNAME, default='admin'): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Busy Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    username = config[CONF_USERNAME]
    password = config.get(CONF_PASSWORD)

    
    auth = Auth.Auth(host, password)
    api = BusyLightAPI.BusyLightAPI(auth)
    light = api.get_light()

    # Add devices
    add_entities([BusyLight(light)])


def setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    add_entities,
):
    config = hass.data[DOMAIN][config_entry.entry_id]
    auth = Auth.Auth(config[CONF_HOST], config[CONF_PASSWORD])
    api = BusyLightAPI.BusyLightAPI(auth)
    light = api.get_light()

    # Add devices
    add_entities([BusyLight(light)])



class BusyLight(LightEntity):
    """Representation of a Busy Light."""

    def __init__(self, light) -> None:
        """Initialize aBusy Light."""
        self._light = light
        self._name = light.name
        self._state = None
        self._brightness = None

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            # If desired, the name for the device could be different to the entity
            "name": self.name,
        }

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def unique_id(self) -> str:
        return "busylight-uniqueid-123"

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.
        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._light.control(True)

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._light.control(False)

    def update(self) -> None:
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._light.update()
        self._state = self._light.is_on
        