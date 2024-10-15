import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class Display:
    def __init__(self, address=0x3C):
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
        self.fontTitle = ImageFont.truetype(
            "/usr/share/fonts/truetype/DSEG7ModernMini-Regular.ttf", self.fontSize
        )
        self.fontData = ImageFont.truetype(
            "/usr/share/fonts/truetype/DSEG7ModernMini-Regular.ttf", self.fontSize + 2
        )
        self.fontSeparator = ImageFont.load_default(4)
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

    def show(self, title, val1, val2=None):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text(
            (self.x, self.top + 0),
            f"{title}",
            font=self.fontTitle,
            fill=255,
        )
        self.draw.text(
            (self.x, self.top + self.fontSize),
            f"{val1}",
            font=(
                self.fontData
                if val2
                else ImageFont.load_default(size=self.fontSize * 2.5 + 2)
            ),
            fill=255,
        )
        if val2:
            self.draw.text(
                (self.x, self.top + self.fontSize * 2 + 6),
                f"----------------------------------------------------------------------------------------------------------------------",
                font=self.fontSeparator,
                fill=255,
            )
            self.draw.text(
                (self.x, self.top + self.fontSize * 3 - 6),
                f"{val2}",
                font=self.fontData,
                fill=255,
            )

        # Display image.
        self.disp.image(self.image)
        self.disp.show()
        # time.sleep(0.1)

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
