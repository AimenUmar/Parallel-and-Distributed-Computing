import os
import time
from multiprocessing import Process, Manager
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "images_dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_distributed")
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


def node_process(node_id, image_subset, return_dict):
    start_time = time.time()
    processed_count = 0

    for input_path, relative_path, file in image_subset:
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
            print(f"[Node {node_id}] Error processing {input_path}: {e}")

    end_time = time.time()
    total_time = end_time - start_time
    return_dict[node_id] = (processed_count, total_time)


def simulate_distributed_processing():
    image_files = []
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.jfif', '.webp')):
                relative_path = os.path.relpath(root, INPUT_DIR)
                image_files.append((os.path.join(root, file), relative_path, file))

    if not image_files:
        print("No images found in images_dataset/. Please check folder paths.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_images = len(image_files)
    half = total_images // 2
    node1_images = image_files[:half]
    node2_images = image_files[half:]
    
    print(f"Total images: {total_images} (Node 1: {len(node1_images)}, Node 2: {len(node2_images)})\n")

    manager = Manager()
    return_dict = manager.dict()

    overall_start = time.time()

    node1 = Process(target=node_process, args=(1, node1_images, return_dict))
    node2 = Process(target=node_process, args=(2, node2_images, return_dict))

    node1.start()
    node2.start()

    node1.join()
    node2.join()


    overall_end = time.time()
    total_time = overall_end - overall_start

    node1_count, node1_time = return_dict[1]
    node2_count, node2_time = return_dict[2]

    print(f"Node 1 processed {node1_count} images in {node1_time:.2f}s")
    print(f"Node 2 processed {node2_count} images in {node2_time:.2f}s")
    print(f"Total distributed time: {total_time:.2f}s")

    sequential_time = 0.71  
    efficiency = sequential_time / total_time if total_time > 0 else 0
    print(f"Efficiency: {efficiency:.2f}x over sequential")


if __name__ == "__main__":
    simulate_distributed_processing()
