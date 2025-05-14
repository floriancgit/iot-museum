import requests
# import yaml
import csv
import os
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from slugify import slugify

HEIGHT = 1080
WIDTH = 1920

IMAGE_HEIGHT = 0.88 * HEIGHT
LINE1_Y_POSITION = 0.93 * HEIGHT
LINE2_Y_POSITION = 0.96 * HEIGHT

def download_image(url):
    headers = {
        'User-Agent': 'MyArtworkApp/1.0 (your-email@example.com)'  # Set a custom User-Agent for wikipedia
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)) 

def create_black_image(width, height):
    return Image.new('RGB', (width, height), 'black')

def resize_image(image, height):
    aspect_ratio = image.width / image.height
    new_width = int(height * aspect_ratio)
    height = int(height)
    return image.resize((new_width, height), Image.LANCZOS)

def add_centered_text_to_image(image, text, font_path, font_size, color, y_position):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Font file not found: {font_path}. Using default font.")
        font = ImageFont.load_default()

    # Calculate text width and position
    text_width = draw.textlength(text, font=font)
    image_width = image.width
    x_position = (image_width - text_width) // 2

    draw.text((x_position, y_position), text, font=font, fill=color)

    return image

def paste_image_onto_black(black_image, pasted_image):
    bg_width, bg_height = black_image.size
    img_width, img_height = pasted_image.size
    position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2 - 30)

    black_image.paste(pasted_image, position)
    return black_image

def save_image(image, output_path):
    image.save(output_path)

def process_artwork(artwork, output_dir):
    downloaded_image = download_image(artwork['url'])
    random_number = f"{random.randint(0, 9999):04d}"
    resized_image = resize_image(downloaded_image, IMAGE_HEIGHT)
    black_image = create_black_image(WIDTH, HEIGHT)
    final_image = paste_image_onto_black(black_image, resized_image)
    line1 = f"{artwork['title']}, {artwork['artist']}, {artwork['year']}"
    line2 = f"{artwork.get('description', '')[:150]}"
    final_image_with_text = add_centered_text_to_image(final_image, line1, "/System/Library/Fonts//Helvetica.ttc", 20, "white", LINE1_Y_POSITION)
    final_image_with_text = add_centered_text_to_image(final_image, line2, "/System/Library/Fonts//Helvetica.ttc", 18, "white", LINE2_Y_POSITION)
    filename = f"{random_number}-{slugify(artwork['title'])}.jpg"
    output_path = f"{output_dir}{filename}"
    save_image(final_image_with_text, output_path)
    print(f"Image saved to {output_path}")

with open('_data/museum_v2.csv', mode='r') as file:
    artworks_data = csv.DictReader(file)

    output_directory = '_site/assets/dist/'
    os.makedirs(os.path.dirname(output_directory), exist_ok=True)
    for artwork in artworks_data:
        process_artwork(artwork, output_directory)
        # break

