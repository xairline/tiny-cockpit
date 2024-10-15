# RaspberryPi Zero as a Virtual joystick
This project was developed to turn a RaspberryPi Zero into a virtual joystick

1. Download the GPIO Python package:
   ```
   sudo apt-get update
   sudo apt-get -y install rpi.gpio python3-gpiozero
   ```

1. Copy the USB device creation script to /usr/bin and make it executable
   ```
   sudo cp device.sh /usr/bin
   sudo chmod +x /usr/bin/device.sh
   ```
1. The RaspberryPi uses dynamic device creation so the creation script needs to be run every time the Pi boots. To configure the Zero to run the USB joystick device creation on boot add the following line above 'exit 0' to the file ```/etc/rc.local```
   ```
   /usr/bin/device.sh
   ```
1. Reboot the Zero
   ```
   sudo reboot
   ```