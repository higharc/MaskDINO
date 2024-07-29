import os
from PIL import Image
import argparse
from utils import print_


def convert_images(folder_path, add_log):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Iterate through each file
    for file in files:
        # Check if it's a JPG file
        if file.endswith(".jpg"):
            # Open the image
            img_path = os.path.join(folder_path, file)
            img = Image.open(img_path)
            
            # Convert to PNG
            png_path = img_path[:-4] + ".png"
            img.save(png_path, "PNG")
            
            print_(f"Converted {file} to PNG", add_log)

def main():
    parser = argparse.ArgumentParser(description='Convert JPG images to PNG in specified folders.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--key_paths', type=str, nargs='+', required=True, help='List of key_paths')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')
    parser.add_argument('--not_add_log', action="store_true", help='Add job log in the output or not')

    args = parser.parse_args()

    dataset_type = args.dataset_type
    key_paths = args.key_paths
    base_url = args.base_url
    add_log = not args.not_add_log

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}, add_log: {add_log}")

    # Iterate through each folder and convert images
    for key_path in key_paths:
        folder_path = os.path.join(base_url, key_path)
        if os.path.isdir(folder_path):
            convert_images(folder_path, add_log)
        else:
            print_(f"{key_path} is not a valid directory.", add_log)

if __name__ == "__main__":
    main()
