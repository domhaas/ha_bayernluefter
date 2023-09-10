"""
Connect to a Bayernluefter via it's web interface and read and write data
Switch to control the power state
"""
import logging

from pyernluefter import Bayernluefter

from homeassistant.const import STATE_UNKNOWN

try:
    from homeassistant.components.switch import SwitchEntity
except ImportError:
    from homeassistant.components.switch import SwitchDevice as SwitchEntity

_LOGGER = logging.getLogger(__name__)

DOMAIN = "bayernluefter"

DEFAULT_NAME = "Bayernluefter"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Bayernluefter component"""

    if discovery_info is None:
        _LOGGER.warning(
            "Bayernluefter Sensor explicitly configured, should be discovered. Look at documentation for correct setup instructions."
        )
        return False
    domain = discovery_info["domain"]
    name = discovery_info["name"]
    bayernluefter = hass.data[domain][name]
    ent = [
        BayernluefterPowerSwitch(name=f"{name} Power", bayernluefter=bayernluefter)
    ]
    async_add_entities(ent)


class BayernluefterPowerSwitch(SwitchEntity):
    """
    Representation of a switch that toggles a digital output of the UVR1611.
    """

    def __init__(self, name, bayernluefter: Bayernluefter):
        """Initialize the switch."""
        self._bayernluefter = bayernluefter
        self._name = name

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        _LOGGER.error("switch isOn")
        _LOGGER.error(self._bayernluefter.raw_converted())
        return self._bayernluefter.raw_converted()["_SystemOn"]

    async def async_turn_on(self, **kwargs):
        """Turn the device on."""
        _LOGGER.error("switch turn_on")
        await self._bayernluefter.power_on()
        """self._assumed_state = True"""

    async def async_turn_off(self, **kwargs):
        """Turn the device off."""
        _LOGGER.error("switch turn_off")
        await self._bayernluefter.power_off()

    async def async_toggle(self, **kwargs):
        _LOGGER.error("switch toggle")
        await self._bayernluefter.button_power()
        
    async def async_update(self):
        _LOGGER.error("switch update")
        await self._bayernluefter.update()
