from PIL import Image, ImageDraw, ImageFont
import random
import string
from captcha.image import ImageCaptcha

def generate_captcha(username):
    # Define image properties
    size = (200, 100)
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 40
    font = ImageFont.truetype('arial.ttf', font_size)

    # Generate random string of characters
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))

    # Dearrange characters in username
    username_chars = list(username)
    random.shuffle(username_chars)
    username_dearranged = ''.join(username_chars[:4])

    # Combine dearranged username with random characters
    captcha_text = username_dearranged + chars

    size = (200, 100)
    font_path = 'arial.ttf'

    # Create image object
    image = ImageCaptcha(width=size[0], height=size[1], fonts=[font_path])

    # Return captcha image as a PIL image object
    randomNumber = random.random
    path = f'/captcha/{username}.png'
    print(path)
    image.write(captcha_text, path)

    # Return random string of characters
    return path
