import os
from PIL import Image
import numpy as np

from PIL import ImageFont
import random
import string,os

def generate_shares(image_array, k, n):
    height, width, channels = image_array.shape
    shares = []
    for i in range(k-1):
        random_array = np.random.randint(0, 256, size=(height, width, channels))
        shares.append(random_array)

    last_share = image_array.copy()
    last_share = np.bitwise_xor(last_share, shares[0])
    shares.append(last_share)
    return shares

def split_image(image_path, k, n, output_dir,username):

    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)
    shares = generate_shares(image_array, k, n)

    # Save each share as a separate image file
    for i, share in enumerate(shares):
        share = share.astype('uint8')
        share_image = Image.fromarray(share)
        share_path = os.path.join(output_dir, f"{username}_share_{i+1}.png")
        share_image.save(share_path)

    return shares[0]

def split_image_new(image_path, k, n, output_dir,username,client_share,num):

    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)

    last_share = image_array.copy()
    last_share = np.bitwise_xor(last_share, client_share)

    last_share = last_share.astype('uint8')
    share_image = Image.fromarray(last_share)
    share_path = os.path.join(output_dir, f"{username}_share_{num}.png")
    share_image.save(share_path)

    return [os.path.join(output_dir, f"{username}_share_{i+1}.png") for i in range(k)]


def recombine_shares(share_url, client_url):
    # Load the first share image and get its size
    share_image = Image.open(share_url)
    share_width, share_height = share_image.size

    # Initialize an array to hold the recombined image
    recombined_image = np.zeros((share_height, share_width, 3), dtype=np.uint8)

    directory = r'D:\ANTI PHISHING\Anti-Phishing-based-on-VC'
    os.chdir(directory)
    # XOR all the share arrays to obtain the recombined image array
    share_image = Image.open(share_url)
    share_array = np.array(share_image)
    recombined_image = np.bitwise_xor(recombined_image, share_array)
    share_image = Image.open(client_url)
    share_array = np.array(share_image)
    recombined_image = np.bitwise_xor(recombined_image, share_array)

    # Return the path to the recombined image file
    return recombined_image


