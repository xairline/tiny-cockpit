import os
import fcntl
import threading
import time

from utils.tft_display import TftDisplay
from utils.hid import HID
from utils.oled_display import OledDisplay

global buffer
msg_buffer = []


def main():
    my_hid = HID(msg_buffer)
    display1 = TftDisplay(
        cs=1, dc="GPIO24", rst="GPIO25", msg_buffer=msg_buffer, buffer_indicator=0
    )
    display2 = TftDisplay(
        cs=0, dc="GPIO23", rst=None, msg_buffer=msg_buffer, buffer_indicator=2
    )
    display3 = OledDisplay(address=0x3C, msg_buffer=msg_buffer, buffer_indicator=4)
    display4 = OledDisplay(address=0x3D, msg_buffer=msg_buffer, buffer_indicator=6)

    # Start the value fetching thread
    fetch_thread = threading.Thread(target=my_hid.recieve_input)
    fetch_thread.daemon = True  # Daemon thread will exit when the main program exits
    fetch_thread.start()

    # Start the display 1 thread
    display1_thread = threading.Thread(target=display1.show)
    display1_thread.daemon = True  # Daemon thread will exit when the main program exits
    display1_thread.start()

    # Start the display 2 thread
    display2_thread = threading.Thread(target=display2.show)
    display2_thread.daemon = True  # Daemon thread will exit when the main program exits
    display2_thread.start()

    # Start the display 3 thread
    display3_thread = threading.Thread(target=display3.show)
    display3_thread.daemon = True  # Daemon thread will exit when the main program exits
    display3_thread.start()

    # Start the display 4 thread
    display4_thread = threading.Thread(target=display4.show)
    display4_thread.daemon = True  # Daemon thread will exit when the main program exits
    display4_thread.start()

    # Wait for the threads to finish
    fetch_thread.join()
    display3_thread.join()
    display4_thread.join()


if __name__ == "__main__":
    main()
