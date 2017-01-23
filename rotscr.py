from pydbus import SystemBus
from gi.repository import GLib
from pynput import keyboard
import os


def start():
    bus = SystemBus()
    sensors = bus.get("net.hadess.SensorProxy")
    sensors.ClaimAccelerometer()
    sensors.onPropertiesChanged = handle_change
    with keyboard.Listener(on_press=key_pressed) as listener:
        GLib.MainLoop().run()
        listener.join()


def key_pressed(key):
    if key.char != None:
        return

    if str(key) == "<0>":
        os.system("xinput set-prop 'SynPS/2 Synaptics TouchPad' 'Device Enabled' 0")
    elif str(key) == "<269025173>":
        os.system("xinput set-prop 'SynPS/2 Synaptics TouchPad' 'Device Enabled' 1")


def handle_change(namespace, options, _):
    if namespace != "net.hadess.SensorProxy":
        return
    if not "AccelerometerOrientation" in options:
        return
    rotate(options["AccelerometerOrientation"])


def rotate(orientation):
    if orientation == "normal":
        os.system("xrandr --output eDP-1 --rotate normal")
        os.system("xinput set-prop 'ELAN Touchscreen' 'Coordinate Transformation Matrix' 1 0 0 0 1 0 0 0 1")
    elif orientation == "left-up":
        os.system("xrandr --output eDP-1 --rotate left")
        os.system("xinput set-prop 'ELAN Touchscreen' 'Coordinate Transformation Matrix' 0 -1 1 1 0 0 0 0 1")
    elif orientation == "right-up":
        os.system("xrandr --output eDP-1 --rotate right")
        os.system("xinput set-prop 'ELAN Touchscreen' 'Coordinate Transformation Matrix' 0 1 0 -1 0 1 0 0 1")
    elif orientation == "bottom-up":
        os.system("xrandr --output eDP-1 --rotate inverted")
        os.system("xinput set-prop 'ELAN Touchscreen' 'Coordinate Transformation Matrix' -1 0 1 0 -1 1 0 0 1")

if __name__ == "__main__":
    start()