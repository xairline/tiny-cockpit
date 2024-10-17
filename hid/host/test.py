import hid
import sys
import time


def send_output_report():
    # Device Vendor ID and Product ID
    VID = 0x1D6B  # Replace with your device's Vendor ID
    PID = 0x0104  # Replace with your device's Product ID

    # Open the device
    try:
        device = hid.Device(vid=VID, pid=PID)
        # Prepare an Output report
        # Ensure the report length matches your device's expected Output report size
        report_length = 64  # Adjust if necessary

        # Example data to send (64 bytes)
        report_data = bytes("SPD,123,HDG,456,ALT,789,V/S,123\n", "utf-8")

        # Send the Output report
        # On macOS, prepend the report ID if required (often 0 for HID devices without report IDs)
        report_id = 0x00
        report = bytes([report_id]) + report_data

        # Write the report
        bytes_written = device.write(report)

        if bytes_written > 0:
            print(f"Successfully sent {bytes_written} bytes to the device.")
        else:
            print("Failed to send data to the device.")

        device.close()

    except IOError as e:
        print(f"IOError: {e}")
        print("Ensure the device is connected and the VID/PID are correct.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        device.close()


if __name__ == "__main__":
    send_output_report()
