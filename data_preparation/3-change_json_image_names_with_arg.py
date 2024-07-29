import json
import argparse
import os
from utils import print_


def update_file_names(json_file, add_log):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Change file names from .jpg to .png in the "images" section
    for image in data.get('images', []):
        if image.get('file_name'):
            image['file_name'] = image['file_name'][:-4] + ".png"
            
    # Update file names from .jpg to .png in the "annotations" section
    for annotation in data.get('annotations', []):
        if annotation.get('file_name'):
            annotation['file_name'] = annotation['file_name'].replace('.jpg', '.png')

    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print_(f"File names have been updated and saved to {json_file}", add_log)

def main():
    parser = argparse.ArgumentParser(description='Update file names in COCO JSON annotations.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--key_paths', type=str, nargs='+', required=True, help='List of file names')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')
    parser.add_argument('--not_add_log', action="store_true", help='Add job log in the output or not')

    args = parser.parse_args()

    dataset_type = args.dataset_type
    key_paths = args.key_paths
    base_url = args.base_url
    add_log = not args.not_add_log

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}, add_log: {add_log}")

    for key_path in key_paths:
        for t in ["_panoptic_annotations.coco.json", "_annotations.coco.json"]:
            path = os.path.join(base_url, key_path, t)
            update_file_names(path, add_log)

if __name__ == "__main__":
    main()
