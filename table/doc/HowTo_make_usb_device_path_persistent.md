## Writing udev rules
1. Plug in USB device
2. Collect information about device
   * Find device in `lsusb`
   * Gather more information with `sudo lsusb -vs <BUS>:<DEVICE>`, for example `sudo lsusb -vs 002:017`
   * Best suited for udev rules are idVendor, idProduct and iSerial (if available) For the USB SNES Gamepad I find:
     * idVendor     0x0810 Personal Communication Systems, Inc.
     * idProduct	0xe501 SNES Gamepad
3. Write udev rules with root editor in `/etc/udev/rules.d/`
   * Use comments and prefer a high-numbered file name, for example `73-gamepad.rules`
   * Write udev rules. `SUBSYSTEM=="input", ATTRS{idProduct}=="e501", ATTRS{idVendor}=="0810", SYMLINK+="gamepad", OWNER="<USERNAME>"`
     * I don't know what happens if two devices with these attributes get connected
     * It may happen that the user doesn't have read access on the created symlink. If that happens, add the OWNER attribute
   * Debugging with `sudo udevadm test /sys/class/input/eventX`
   
For more information see https://wiki.ubuntuusers.de/udev/#udev-Regel-schreiben-und-speichern

     
