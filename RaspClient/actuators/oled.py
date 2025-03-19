import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Configuracion de la pantalla OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Funcion para mostrar datos en la pantalla OLED
def display_data(temperature, humidity):
    oled.fill(0)
    oled.show()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    draw.text((0, 0), "Temperatura:", font=font, fill=255)
    draw.text((0, 16), f"-> {temperature:.2f} C", font=font, fill=255)
    draw.text((0, 32), "Humedad:", font=font, fill=255)
    draw.text((0, 48), f"-> {humidity:.2f} %", font=font, fill=255)
    oled.image(image)
    oled.show()

# Funcion para mostrar mensajes en la pantalla OLED
def display_message(message):
    oled.fill(0)
    oled.show()
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    max_width = oled.width - 4  # Margen de 2 pixeles a cada lado
    lines = []
    words = message.split(' ')
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    
    y = (oled.height - len(lines) * draw.textbbox((0, 0), lines[0], font=font)[3]) // 2
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
        x = (oled.width - text_width) // 2
        draw.text((x, y), line, font=font, fill=255)
        y += text_height

    oled.image(image)
    oled.show()
