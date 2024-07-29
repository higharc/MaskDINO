import os
from PIL import Image
import argparse

def convert_images(folder_path):
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
            
            print(f"Converted {file} to PNG")

def main():
    parser = argparse.ArgumentParser(description='Convert JPG images to PNG in specified folders.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--folders', type=str, nargs='+', required=True, help='List of folders')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')

    args = parser.parse_args()

    dataset_type = args.dataset_type
    folders = args.folders
    base_url = args.base_url

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, folders: {folders}")

    # Iterate through each folder and convert images
    for folder in folders:
        folder_path = os.path.join(base_url, folder)
        if os.path.isdir(folder_path):
            convert_images(folder_path)
        else:
            print(f"{folder} is not a valid directory.")

if __name__ == "__main__":
    main()
