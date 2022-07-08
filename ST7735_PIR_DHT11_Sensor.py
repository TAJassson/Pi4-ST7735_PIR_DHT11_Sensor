import RPi.GPIO as GPIO
import time
from time import sleep
import dht11
import digitalio
import board
from PIL import Image, ImageDraw
from PIL import ImageFont
import adafruit_rgb_display.st7735 as st7735

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

pir = 22
dht = dht11.DHT11(pin = 2)
GPIO.setup(pir, GPIO.IN)
moved = 0

BORDER = 10
FONTSIZE = 12

BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
BLUE    = (255,   0,   0)
GREEN   = (  0, 255,   0)
RED     = (  0,   0, 255)
CYAN    = (255, 255,   0)
MAGENTA = (255,   0, 255)
YELLOW  = (  0, 255, 255)

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

BAUDRATE = 24000000 

spi = board.SPI()

disp = st7735.ST7735R(
    spi,
    rotation=90,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE
)

if disp.rotation % 180 == 90:
    height = disp.width
    width = disp.height
else:
    width = disp.width
    height = disp.height

image = Image.new("RGB", (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((BORDER-10, BORDER-10, width-BORDER+10, height-BORDER+10), outline=BLACK, fill=BLACK)

font = ImageFont.truetype("/user/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", FONTSIZE)

while True:
    result = dht.read()
    moved = GPIO.input(pir)
    if moved == 1:
        time.sleep(0.2)
        print("PIR Motion detected", moved)
        text0 = "Motion detected"
        (font_width, font_height) = font.getsize(text0)
        draw.text(
        (width // 5 - font_width // 6, height // 1.1 - font_height // 2),
         text0,
         font=font,
         fill=WHITE,
        )
        disp.image(image)
    if result.is_valid():
        draw.rectangle((BORDER-10, BORDER-10, width-BORDER+10, height-BORDER+10), outline=BLACK, fill=BLACK)
        draw.line((200, 90, -200, 90), fill=WHITE)
        draw.line((200, 65, -200, 65), fill=WHITE)
        draw.line((200, 40, -200, 40), fill=WHITE)
        draw.line((200, 15, -200, 15), fill=WHITE)
        print(time.strftime('%d/%m/%y')+" "+time.strftime('%H:%M'))
        print(f"Room Temperature:{result.temperature}C ,{str(round(result.temperature *1.8000+32,1))}F")
        print("Room Humidity: %d %%" % result.humidity)
        text1 = time.strftime('%d/%m/%y')+" "+time.strftime('%H:%M')
        (font_width, font_height) = font.getsize(text1)
        draw.text(
        (width // 8 - font_width // 6, height // 9 - font_height // 1),
         text1,
         font=font,
         fill=WHITE,
        )
        text2 = f"Temperature:{result.temperature}C {str(round(result.temperature *1.8000+32,1))}F"
        (font_width, font_height) = font.getsize(text2)
        draw.text(
        (width // 4.5 - font_width // 6, height // 3.5 - font_height // 1),
         text2,
         font=font,
         fill=WHITE,
        )
        if result.temperature < 20:
            text3 = "Room status:Cold"
            (font_width, font_height) = font.getsize(text3)
            draw.text(
            (width // 5.1 - font_width // 6, height // 2.2 - font_height // 1),
             text3,
             font=font,
             fill=BLUE,
            )
        elif result.temperature <= 29:
            text3 = "Room status:Normal"
            (font_width, font_height) = font.getsize(text3)
            draw.text(
            (width // 5.1 - font_width // 6, height // 2.2 - font_height // 1),
             text3,
             font=font,
             fill=WHITE,
            )
        elif result.temperature > 29:
            text3 = "Room status: Hot"
            (font_width, font_height) = font.getsize(text3)
            draw.text(
            (width // 5.1 - font_width // 6, height // 2.2 - font_height // 1),
             text3,
             font=font,
             fill=RED,
            )
        text4 = "Room Humidity: %d %%" % result.humidity
        (font_width, font_height) = font.getsize(text4)
        draw.text(
        (width // 5.2 - font_width // 6, height // 1.5 - font_height // 1),
         text4,
         font=font,
         fill=WHITE,
        )
        text5 = "PIR sensor:"
        (font_width, font_height) = font.getsize(text5)
        draw.text(
        (width // 6 - font_width // 6, height // 1.2 - font_height // 1),
         text5,
         font=font,
         fill=WHITE,
        )
        time.sleep(0.2)
        disp.image(image)

