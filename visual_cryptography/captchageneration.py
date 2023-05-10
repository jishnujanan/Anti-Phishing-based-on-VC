import random
import string,os
from captcha.image import ImageCaptcha

def generate_captcha(username,captcha_array,i):
    size = (200, 100)
    bg_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_size = 40
    #font = ImageFont.truetype('arial.ttf', font_size)
    chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    username_chars = list(username)
    random.shuffle(username_chars)
    username_dearranged = ''.join(username_chars[:4])
    captcha_text = username_dearranged + chars
    captcha_array.append(captcha_text)
    size = (200, 100)
    font_path = 'arial.ttf'
    image = ImageCaptcha(width=size[0], height=size[1])
    image.write(captcha_text,f'static/media/captcha/{username}/captcha_{i-1}.png')
    return "Success"
