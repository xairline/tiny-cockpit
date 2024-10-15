#!/bin/bash

# Create xac_joystick gadget
cd /sys/kernel/config/usb_gadget/
mkdir -p xac_joystick
cd xac_joystick

# Define USB specification
echo 0x1d6b > idVendor  # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Joystick Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB    # USB2
echo 0x02   > bDeviceClass
echo 0x00   > bDeviceSubClass
echo 0x00   > bDeviceProtocol

# Device information
mkdir -p strings/0x409
echo "xa001" > strings/0x409/serialnumber
echo "X Airline" > strings/0x409/manufacturer
echo "Poor Man's Cockpit" > strings/0x409/product

# Create configuration file
mkdir -p configs/c.1/strings/0x409
echo 0x80 > configs/c.1/bmAttributes
echo 250  > configs/c.1/MaxPower # 250 mA
echo "Cockpit configuration" > configs/c.1/strings/0x409/configuration

# Define the functions of the device
mkdir functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo 6 > functions/hid.usb0/report_length

# Write the HID report descriptor to the report_desc file
echo -ne '\x05\x01\x09\x04\xA1\x01\x05\x09\x19\x01\x29\x0F\x15\x00\x25\x01\x95\x0F\x75\x01\x81\x02\x95\x01\x75\x01\x81\x03\x95\x40\x75\x08\x15\x00\x26\xFF\x00\x09\x00\x91\x02\xC0' > functions/hid.usb0/report_desc

# Link the configuration file
ln -s functions/hid.usb0 configs/c.1

# Activate device
sudo ls /sys/class/udc > UDC

sleep 10