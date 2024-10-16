import os
import fcntl

from utils.display import Display

global buffer
buffer = b""
display3 = Display(address=0x3C)
display4 = Display(address=0x3D)


def main():
    global buffer
    while True:
        try:
            hid_device = "/dev/hidg0"  # Adjust if your device is different
            # Open the HID device in binary read mode
            with open(hid_device, "rb") as hidg:
                # Set the file descriptor to non-blocking mode
                fd = hidg.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                print()
                print("Waiting for incoming HID reports from the host...")
                while True:
                    try:
                        # Read up to 64 bytes (or adjust based on your HID report size)
                        data = hidg.read(64)
                        if data:
                            buffer += data  # Append new data to the buffer

                            # Split the buffer into messages based on the delimiter
                            while b"\n" in buffer:
                                # Find the position of the first delimiter
                                index = buffer.find(b"\n")

                                # Extract the complete message
                                message = buffer[:index]

                                # Remove the processed message from the buffer
                                buffer = buffer[index + 1 :]

                                # Process the complete message
                                msg = message.decode("utf-8", errors="replace")
                                msgSplit = msg.split(",")
                                display3.show(msgSplit[4], msgSplit[5])
                                display4.show(msgSplit[6], msgSplit[7])

                    except BlockingIOError:
                        # No data available at the moment
                        pass
                    except KeyboardInterrupt:
                        print("\nExiting...")
                        exit(0)
                        break
        except KeyboardInterrupt:
            print("\nProcess interrupted by user (Ctrl+C)")
            # Exit the program
            exit(0)
        except Exception as e:
            print(f"Error: {e}")
            print("Restart process")
            continue


if __name__ == "__main__":
    main()
