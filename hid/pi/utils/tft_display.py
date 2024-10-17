import time
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
from utils import font
import st7735

data_padding_left = 25
data_padding_top = 15


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
        self.font_text = ImageFont.truetype(font.REGULAR_FONT, 20)
        self.font = ImageFont.truetype(font.NUMBER_FONT, 35)
        self.draw.rectangle((0, 0, 128, 128), (0, 0, 0))
        self.disp.display(self.img)
        self.hash_title = None
        self.hash_data = None

    def show(self):
        padding = 25
        while True:
            try:
                draw = False
                if len(self.msg_buffer) == 0:
                    continue

                # handle title display
                if self.hash_title == hash(self.msg_buffer[self.buffer_indicator]):
                    pass
                else:
                    self.hash_title = hash(self.msg_buffer[self.buffer_indicator])
                    self.draw.rectangle((5, 5 + padding, 80, 64), (0, 0, 0))
                    self.draw.text(
                        (5, 15 + padding),
                        self.msg_buffer[self.buffer_indicator],
                        font=self.font_text,
                    )
                    draw = True

                # handle data display
                if self.hash_data == hash(self.msg_buffer[self.buffer_indicator + 1]):
                    pass
                else:
                    self.hash_data = hash(self.msg_buffer[self.buffer_indicator + 1])
                    self.draw.rectangle(
                        (
                            data_padding_left,
                            data_padding_top + padding * 2,
                            120,
                            80 + padding,
                        ),
                        (0, 0, 0),
                    )
                    self.draw.text(
                        (data_padding_left, data_padding_top + padding * 2),
                        self.msg_buffer[self.buffer_indicator + 1],
                        font=self.font,
                        fill=(0, 255, 255),
                    )
                    draw = True

                if draw:
                    self.disp.display(self.img)

            except Exception as e:
                print(f"Error: {e}")
                self.disp.begin()
