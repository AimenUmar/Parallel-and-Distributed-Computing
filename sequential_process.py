import os
import time
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "images_dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_seq")
IMAGE_SIZE = (128, 128)
WATERMARK_TEXT = "Image"


def add_watermark(image, text):
    watermark = image.copy()
    draw = ImageDraw.Draw(watermark)
    font = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(text, font)

    x = watermark.width - text_width - 10
    y = watermark.height - text_height - 10

    draw.text((x, y), text, font=font, fill=(255, 0, 255, 180))
    return watermark



def process_images_sequentially():
    start_time = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    processed_count = 0

    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.jfif', '.webp')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, INPUT_DIR)
                output_folder = os.path.join(OUTPUT_DIR, relative_path)
                os.makedirs(output_folder, exist_ok=True)
                output_path = os.path.join(output_folder, file)

                try:
                    img = Image.open(input_path).convert("RGB")
                    img = img.resize(IMAGE_SIZE)
                    watermarked = add_watermark(img, WATERMARK_TEXT)
                    watermarked.save(output_path)
                    processed_count += 1
                except Exception as e:
                    print(f"Error processing {input_path}: {e}")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Processed {processed_count} images.")
    print(f"Sequential Processing Time: {total_time:.2f} seconds")


if __name__ == "__main__":
    process_images_sequentially()
