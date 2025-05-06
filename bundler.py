import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)) 

def create_black_image(width, height):
    return Image.new('RGB', (width, height), 'black')

def resize_image(image, height):
    aspect_ratio = image.width / image.height
    new_width = int(height * aspect_ratio)
    return image.resize((new_width, height), Image.LANCZOS)

def add_text_to_image(image, text, position, font_path, font_size, color):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=color)
    return image

def paste_image_onto_black(black_image, pasted_image):
    bg_width, bg_height = black_image.size
    img_width, img_height = pasted_image.size
    position = ((bg_width - img_width) // 2, (bg_height - img_height) // 2 - 50)

    black_image.paste(pasted_image, position)
    return black_image

def save_image(image, output_path):
    image.save(output_path)

image_url = 'http://www.kaywalkingstick.com/art/canvas_wood/fullsize/Our_Land.jpg'
output_path = '_site/assets/Our_Land.jpg'
footer_text = "Your Footer Text Here"

downloaded_image = download_image(image_url)
resized_image = resize_image(downloaded_image, 864)
black_image = create_black_image(1920, 1080)
final_image = paste_image_onto_black(black_image, resized_image)
final_image_with_text = add_text_to_image(final_image, footer_text, (50, 1020), "arial.ttf", 40, "white")
save_image(final_image, output_path)
print(f"Image saved to {output_path}")
