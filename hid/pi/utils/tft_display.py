import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import st7735


class TftDisplay:
    def __init__(
        self, cs=0, dc="GPIO24", rst="GPIO25", msg_buffer=None, buffer_indicator=None
    ):
        self.msg_buffer = msg_buffer
        self.buffer_indicator = buffer_indicator
        self.disp = st7735.ST7735(
            port=0,
            cs=cs,
            width=128,
            height=160,
            dc=dc,
            rst=rst,
            backlight=None,
            invert=False,
            rotation=180,
            spi_speed_hz=4000000,
        )
        # Clear display.
        WIDTH = self.disp.width
        HEIGHT = self.disp.height
        self.disp.begin()

        self.img = Image.new("RGB", (WIDTH, HEIGHT))
        self.draw = ImageDraw.Draw(self.img)
        self.font_text = ImageFont.truetype(
            "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 20
        )
        self.font = ImageFont.truetype(
            "/usr/share/fonts/truetype/DSEG7ModernMini-Regular.ttf", 40
        )
        self.hash = None

    def show(self):
        padding = 25
        while True:
            try:
                if len(self.msg_buffer) == 0:
                    continue
                if self.hash == hash(
                    self.msg_buffer[self.buffer_indicator]
                    + self.msg_buffer[self.buffer_indicator + 1]
                ):
                    continue
                self.hash = hash(
                    self.msg_buffer[self.buffer_indicator]
                    + self.msg_buffer[self.buffer_indicator + 1]
                )
                self.draw.rectangle((0, 30, 128, 128), (0, 0, 0))
                self.draw.text(
                    (5, 15 + padding),
                    self.msg_buffer[self.buffer_indicator],
                    font=self.font_text,
                    fill=(255, 200, 155),
                )
                self.draw.text(
                    (5, 5 + padding * 2),
                    self.msg_buffer[self.buffer_indicator + 1],
                    font=self.font,
                    fill=(0, 255, 255),
                )
                self.disp.display(self.img)

            except Exception as e:
                print(f"Error: {e}")
                self.disp.begin()
