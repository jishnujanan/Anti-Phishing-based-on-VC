import random
import string,os
from captcha.image import ImageCaptcha
from . import captcha_generation

def generate_captcha(username,captcha_array):
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    username_chars = list(username)
    random.shuffle(username_chars)
    username_dearranged = ''.join(username_chars[:4])
    captcha_text = username_dearranged + chars
    captcha_array.append(captcha_text)
    captcha_generation.draw_captcha(captcha_text,f'static/media/captcha/{username}.png')
    return "Success"