
from PIL import Image, ImageDraw, ImageFont
import random,string

def draw_captcha(text,outputName):
    width = 200
    height = 100
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('static/fonts/arial.ttf',36)
    
    code_chars = text
    for i, c in enumerate(code_chars):
        x = 10 + i * 25 + random.randint(-5, 5)
        y = 10 + random.randint(-5, 5)
        draw.text((x, y), c, font=font, fill=(random.randint(50, 175),random.randint(50, 175),random.randint(50, 175)))
    
    line_count = random.randint(2,5)
    for i in range(line_count):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0))
    
    dot_count = random.randint(200,400)
    for i in range(dot_count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(0, 0, 0))
    
    image.save(outputName)