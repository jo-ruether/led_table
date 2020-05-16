import evdev
from evdev import ecodes, categorize
from table.core.Postman import Topics
from table.utils.Commands import CMD
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def listen_to_usb_input(postman, config_handler):
    key_mapping = {
        ecodes.EV_KEY: {  # Value 1 (pressed) and 0 (released)
            288: CMD.X,
            291: CMD.Y,
            289: CMD.A,
            290: CMD.B,
            297: CMD.START,
            296: CMD.SELECT,
            293: CMD.R,
            292: CMD.L
        },
        ecodes.EV_ABS: {
            0: {    # Value between 0 (left) and 255 (right); 127 means not pressed
                0:      CMD.LEFT,
                255:    CMD.RIGHT
            },
            1: {    # Value between 0 (up) and 255 (down); 127 means not pressed
                0:      CMD.UP,
                255:    CMD.DOWN
            }
        }
    }

    controller_path = config_handler.get_value("UsbInput", "device_path")

    device = evdev.InputDevice(controller_path)

    for event in device.read_loop():
        if (event.type == ecodes.EV_KEY) and (event.code in key_mapping[ecodes.EV_KEY]):
            # Button event
            logger.debug(f"Button key on USB controller pressed.")
            if event.value == 1:
                # Pressed (not released)
                postman.send(Topics.INPUT, key_mapping[ecodes.EV_KEY][event.code])

        elif (event.type == ecodes.EV_ABS) and (event.code in key_mapping[ecodes.EV_ABS]):
            # Arrow event
            logger.debug(f"Arrow key on USB controller pressed.")
            if (event.value == 0) or (event.value == 255):
                # Pressed (not released)
                postman.send(Topics.INPUT, key_mapping[ecodes.EV_ABS][event.code][event.value])
        else:
            if event.type == ecodes.EV_SYN:
                # Synchronization event
                continue

            logger.debug(f"Got unknown input from usb controller: {categorize(event)}")