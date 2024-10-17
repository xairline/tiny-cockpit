import fcntl
import os


class HID:
    def __init__(self, msg_buffer):
        self.hid_device = "/dev/hidg0"
        self.msg_buffer = msg_buffer
        self.buffer = b""
        self.counter = 0

    def send_output_report(self):
        pass

    # send keypresses to the host
    def send_keypress(self, key):
        pass

    def recieve_input(self):
        while True:
            try:
                # Open the HID device in binary read mode
                with open(self.hid_device, "rb") as hidg:
                    # Set the file descriptor to non-blocking mode
                    fd = hidg.fileno()
                    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                    while True:
                        try:
                            # Read up to 64 bytes (or adjust based on your HID report size)
                            data = hidg.read(64)
                            if data:
                                self.buffer += data  # Append new data to the buffer

                                # Split the buffer into messages based on the delimiter
                                while b"\n" in self.buffer:
                                    # Find the position of the first delimiter
                                    index = self.buffer.find(b"\n")

                                    # Extract the complete message
                                    message = self.buffer[:index]

                                    # Remove the processed message from the buffer
                                    self.buffer = self.buffer[index + 1 :]

                                    # Process the complete message
                                    msg = message.decode("utf-8", errors="replace")
                                    self.msg_buffer.clear()
                                    self.msg_buffer.extend(msg.split(","))
                                    self.counter += 1
                                    if self.counter > 100:
                                        self.counter = 0
                                        print(
                                            f"msg processed: last msg: {self.msg_buffer}"
                                        )
                                    # print(self.msg_buffer)

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
