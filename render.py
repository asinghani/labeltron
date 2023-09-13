from PIL import ImageFont, ImageDraw, Image
import io
import os
import hashlib
import config

VALID_SIZES  = ["small", "medium", "large"]
VALID_WIDTHS = ["12mm", "24mm"]

def render_png(image):
    b = io.BytesIO()
    image.save(b, format="PNG")
    return b.getvalue()

def render_pbm(image):
    b = io.BytesIO()
    image.save(b, format="PPM")
    return b.getvalue()

def render_label(text, border=False, for_print=False):
    if "=//=" in text:
        width, size, text = text.split("=//=")
    else:
        width = "12mm"
        size = "large"

    dim     = 2 if (width == "24mm") else 1
    dimfont = 2.25 if (width == "24mm") else 1

    while len(text) and text[-1] == "\n": text = text[:-1]

    if len(text) == 0:
        text = " "

    textsize = {"small": 0.6, "medium": 0.8, "large": 1.0}.get(size, 1.0)

    text = "\n".join(text.splitlines()[:3])

    lines = len(text.splitlines())
    fontsize = int({1: 44, 2: 22, 3: 14}[lines] * dimfont * textsize)
    ycoord = {1: 32, 2: 32, 3: 32}[lines] * dimfont
    padding = 30 * dim
    height = 64 * dim

    font = ImageFont.truetype("Geneva.ttf", fontsize, index=0)

    image = Image.new(mode="1", size=(1, 1), color=255)
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, anchor="mm", align="center", font=font)
    width = int(bbox[2]-bbox[0])
    # while width % 8 != 0: width += 1 ## unsure if needed

    image = Image.new(mode="1", size=(width+padding, height), color=255)
    draw = ImageDraw.Draw(image)

    if border:
        draw.rectangle(((0, 0), (width+padding-1, height-1)), outline=(0))

    draw.text((width/2+(padding//2), ycoord), text, anchor="mm", align="center", fill=(0), font=font)

    if for_print:
        image = image.rotate(-90, expand=True)

    return image
