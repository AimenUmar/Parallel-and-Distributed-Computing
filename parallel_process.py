import os
import time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "images_dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_parallel")
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


def process_single_image(file_info):
    input_path, relative_path, file = file_info

    output_folder = os.path.join(OUTPUT_DIR, relative_path)
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, file)

    try:
        img = Image.open(input_path).convert("RGB")
        img = img.resize(IMAGE_SIZE)
        watermarked = add_watermark(img, WATERMARK_TEXT)
        watermarked.save(output_path)
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_images_parallel(workers):
    if not os.path.exists(INPUT_DIR):
        print(f"Input folder not found: {INPUT_DIR}")
        return 0, 0

    image_files = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.jfif', '.webp')):
                relative_path = os.path.relpath(root, INPUT_DIR)
                image_files.append((os.path.join(root, file), relative_path, file))

    if not image_files:
        print("No images found in images_dataset/. Please check folder paths.")
        return 0, 0

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    start_time = time.time()
    processed_count = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(process_single_image, image_files))
        processed_count = sum(results)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Workers: {workers} | Time: {total_time:.2f} seconds | Processed: {processed_count} images")

    return processed_count, total_time


if __name__ == "__main__":

    worker_configs = [1, 2, 4, 8]
    times = {}

    for w in worker_configs:
        _, t = process_images_parallel(w)
        times[w] = t

    base_time = times[1] if times[1] > 0 else 1
    print("\nWorkers | Time (s) | Speedup")
    print("-------- | -------- | -------")
    for w in worker_configs:
        speedup = base_time / times[w] if times[w] > 0 else 0
        print(f"{w:<8} | {times[w]:<8.2f} | {speedup:.2f}x")
