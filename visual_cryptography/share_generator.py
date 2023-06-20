import os
from PIL import Image
import numpy as np

from PIL import ImageFont
import random
import string,os

def split_image(image_path, k, n, output_dir,username):
    image = Image.open(image_path).convert("1")
    width, height = image.size
    client_share =  Image.new(mode = "1", size = (width * 4, height * 4))
    for x in range(0, width*4,4):
        for y in range(0, height*4,4):
            color=random.randint(0,1)
            client_share.putpixel((x,  y),   1-color)
            client_share.putpixel((x+1,y),   color)
            client_share.putpixel((x+2,  y), 1-color)
            client_share.putpixel((x+3,y), color)
            client_share.putpixel((x,  y+1),   color)
            client_share.putpixel((x+1,y+1),   1-color)
            client_share.putpixel((x+2,  y+1), color)
            client_share.putpixel((x+3,y+1), 1-color)
            client_share.putpixel((x,  y+2),   1-color)
            client_share.putpixel((x+1,y+2),   color)
            client_share.putpixel((x+2,  y+2), 1-color)
            client_share.putpixel((x+3,y+2), color)
            client_share.putpixel((x,  y+3),   color)
            client_share.putpixel((x+1,y+3),   1-color)
            client_share.putpixel((x+2,  y+3), color)
            client_share.putpixel((x+3,y+3), 1-color)
    share_path = os.path.join(output_dir, f"{username}_share_1.png")
    client_share.save(share_path)
    share_image = Image.new(mode = "1", size = (width * 4, height * 4))
    for x in range(0, width*4, 4):
        for y in range(0, height*4, 4):
            secret = client_share.getpixel((x,y))
            message = image.getpixel((x/4,y/4))
            if (message > 0 and secret > 0) or (message == 0 and secret == 0):
                color = 0
            else:
                color = 1
            share_image.putpixel((x,  y),   1-color)
            share_image.putpixel((x+1,y),   color)
            share_image.putpixel((x+2,  y), 1-color)
            share_image.putpixel((x+3,y), color)
            share_image.putpixel((x,  y+1),   color)
            share_image.putpixel((x+1,y+1),   1-color)
            share_image.putpixel((x+2,  y+1), color)
            share_image.putpixel((x+3,y+1), 1-color)
            share_image.putpixel((x,  y+2),   1-color)
            share_image.putpixel((x+1,y+2),   color)
            share_image.putpixel((x+2,  y+2), 1-color)
            share_image.putpixel((x+3,y+2), color)
            share_image.putpixel((x,  y+3),   color)
            share_image.putpixel((x+1,y+3),   1-color)
            share_image.putpixel((x+2,  y+3), color)
            share_image.putpixel((x+3,y+3), 1-color)
    share_path = os.path.join(output_dir, f"{username}_share_2.png")
    share_image.save(share_path)
    share_path = os.path.join(output_dir, f"{username}_share_1.png")
    return share_path

def split_image_new(image_path, k, n, output_dir,username,client_share,num):

    image = Image.open(image_path).convert("1")
    client_share=Image.open(client_share)
    width, height = image.size
    share_image = Image.new(mode = "1", size = (width * 4, height * 4))
    for x in range(0, width*4, 4):
        for y in range(0, height*4, 4):
            secret = client_share.getpixel((x,y))
            message = image.getpixel((x/4,y/4))
            if (message > 0 and secret > 0) or (message == 0 and secret == 0):
                color = 0
            else:
                color = 1
            share_image.putpixel((x,  y),   1-color)
            share_image.putpixel((x+1,y),   color)
            share_image.putpixel((x+2,y), 1-color)
            share_image.putpixel((x+3,y), color)
            share_image.putpixel((x,y+1),   color)
            share_image.putpixel((x+1,y+1),   1-color)
            share_image.putpixel((x+2,y+1), color)
            share_image.putpixel((x+3,y+1), 1-color)
            share_image.putpixel((x,y+2),   1-color)
            share_image.putpixel((x+1,y+2),   color)
            share_image.putpixel((x+2,y+2), 1-color)
            share_image.putpixel((x+3,y+2), color)
            share_image.putpixel((x,y+3),   color)
            share_image.putpixel((x+1,y+3),   1-color)
            share_image.putpixel((x+2,y+3), color)
            share_image.putpixel((x+3,y+3), 1-color)
    share_path = os.path.join(output_dir, f"{username}_share_{num}.png")
    share_image.save(share_path)
    return [os.path.join(output_dir, f"{username}_share_{i+1}.png") for i in range(k)]


def recombine_shares(share_url, client_url):
    # Load the first share image and get its size
    share_image = Image.open(share_url)
    share_width, share_height = share_image.size

    # Initialize an array to hold the recombined image
    recombined_image = np.zeros((share_height, share_width, 3), dtype=np.uint8)

    
    # XOR all the share arrays to obtain the recombined image array
    share_image = Image.open(share_url)
    share_array = np.array(share_image)
    recombined_image = np.bitwise_xor(recombined_image, share_array)
    share_image = Image.open(client_url)
    share_array = np.array(share_image)
    recombined_image = np.bitwise_xor(recombined_image, share_array)

    # Return the path to the recombined image file
    return recombined_image

