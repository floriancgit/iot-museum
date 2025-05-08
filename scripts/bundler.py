import requests
import yaml
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from slugify import slugify

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
    return image.resize((new_width, height), Image.LANCZOS)

def add_centered_text_to_image(image, texts, font_path, font_size, color):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Position the text at the bottom of the image
    y_position = image.height - 80  # Adjust this value to change the vertical position

    for text in texts:
        # Calculate text width and position
        text_width = draw.textlength(text, font=font)
        image_width = image.width
        x_position = (image_width - text_width) // 2

        draw.text((x_position, y_position), text, font=font, fill=color)
        y_position += 40  # Adjust this value to change the spacing between lines

    return image

def paste_image_onto_black(black_image, pasted_image):
    bg_width, bg_height = black_image.size
    img_width, img_height = pasted_image.size
    position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2 - 50)

    black_image.paste(pasted_image, position)
    return black_image

def save_image(image, output_path):
    image.save(output_path)

def process_artwork(artwork, output_dir):
    downloaded_image = download_image(artwork['url'])
    resized_image = resize_image(downloaded_image, 864)
    black_image = create_black_image(1920, 1080)
    final_image = paste_image_onto_black(black_image, resized_image)
    footer_texts = [
        f"{artwork['title']} by {artwork['artist']}",
        f"{artwork['year']}, {artwork.get('description', '')}",
    ]
    final_image_with_text = add_centered_text_to_image(final_image, footer_texts, "arial.ttf", 600, "white")
    filename = f"{slugify(artwork['title'])}.jpg"
    output_path = f"{output_dir}{filename}"
    save_image(final_image_with_text, output_path)
    print(f"Image saved to {output_path}")

with open('_data/museum.yml', 'r') as file:
    artworks_data = yaml.safe_load(file)

output_directory = '_site/assets/dist/'
os.makedirs(os.path.dirname(output_directory), exist_ok=True)
for artwork in artworks_data['artworks']:
    process_artwork(artwork, output_directory)

