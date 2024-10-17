import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from utils import font

data_padding_left = 0
data_padding_top = 15


class OledDisplay:
    def __init__(self, address=0x3C, msg_buffer=None, buffer_indicator=None):
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=address)
        # Clear display.
        self.disp.fill(0)
        self.disp.show()
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.fontSize = 16
        self.fontTitle = ImageFont.truetype(font.REGULAR_FONT, self.fontSize)
        self.fontData = ImageFont.truetype(font.NUMBER_FONT, self.fontSize + 2)
        self.fontSeparator = ImageFont.load_default()
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0
        self.buffer_indicator = buffer_indicator
        self.msg_buffer = msg_buffer
        self.hash_title = None
        self.hash_data = None

    def show(self):
        while True:
            try:
                draw = False
                if len(self.msg_buffer) == 0:
                    continue

                title = self.msg_buffer[self.buffer_indicator]
                val1 = self.msg_buffer[self.buffer_indicator + 1]

                # handle title display
                if self.hash_title == hash(self.msg_buffer[self.buffer_indicator]):
                    pass
                else:
                    self.hash_title = hash(self.msg_buffer[self.buffer_indicator])
                    self.draw.rectangle((0, 0, 60, 16), 0, 0)
                    self.draw.text(
                        (self.x, self.top + 0),
                        f"{title}",
                        font=self.fontTitle,
                        fill=255,
                    )
                    draw = True

                if self.hash_data == hash(self.msg_buffer[self.buffer_indicator + 1]):
                    pass
                else:
                    self.hash_data = hash(self.msg_buffer[self.buffer_indicator + 1])
                    self.draw.rectangle((self.x + data_padding_left, 16, 128, 50), 0, 0)
                    self.draw.text(
                        (self.x + data_padding_left, self.top + self.fontSize + 2),
                        f"{val1}",
                        font=(
                            ImageFont.truetype(
                                font.NUMBER_FONT,
                                self.fontSize * 2.5 + 2,
                            )
                        ),
                        fill=255,
                    )
                    draw = True

                if draw:
                    self.disp.image(self.image)
                    self.disp.show()

            except Exception as e:
                print(f"Error: {e}")
                self.disp.fill(0)
                self.disp.show()

    def clear(self):
        self.disp.fill(0)
        self.disp.show()

    def error(self, title, val1, val2):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text(
            (self.x, self.top + 0),
            f"{title}",
            font=self.fontTitle,
            fill=255,
        )
        self.draw.text(
            (self.x, self.top + self.fontSize + 2),
            f"{val1}",
            font=self.fontTitle,
            fill=255,
        )
        self.draw.text(
            (self.x, self.top + self.fontSize * 2),
            f"----------------------------------------------------------------------------------------------------------------------",
            font=self.fontTitle,
            fill=255,
        )
        self.draw.text(
            (self.x, self.top + self.fontSize * 3),
            f"{val2}",
            font=self.fontTitle,
            fill=255,
        )

        # Display image.
        self.disp.image(self.image)
        self.disp.show()
        # time.sleep(0.1)
