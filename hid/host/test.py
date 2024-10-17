import hid
import sys
import time


def send_output_report():
    # Device Vendor ID and Product ID
    VID = 0x1D6B  # Replace with your device's Vendor ID
    PID = 0x0104  # Replace with your device's Product ID

    # Open the device
    device = hid.Device(vid=VID, pid=PID)
    device.nonblocking = True
    # Prepare an Output report
    # Ensure the report length matches your device's expected Output report size
    report_length = 64  # Adjust if necessary

    count = 0
    # Write the report
    while True:
        try:
            count += 1
            if count > 200:
                count = 0
            # Example data to send (64 bytes)
            report_data = bytes(
                f"SPD,{123+count},HDG,{456+count},ALT,{78900+count},V/S,+-{1230+count}\n",
                "utf-8",
            )

            # Send the Output report
            # On macOS, prepend the report ID if required (often 0 for HID devices without report IDs)
            report_id = 0x00
            report = bytes([report_id]) + report_data
            bytes_written = device.write(report)
            time.sleep(0.3)
        except Exception as e:
            print(f"Failed to send data to the device: {e}")

    if bytes_written > 0:
        print(f"Successfully sent {bytes_written} bytes to the device.")
    else:
        print("Failed to send data to the device.")


if __name__ == "__main__":
    send_output_report()
