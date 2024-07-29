import json
import argparse

def update_file_names(json_file):
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

    print(f"File names have been updated and saved to {json_file}")

def main():
    parser = argparse.ArgumentParser(description='Update file names in COCO JSON annotations.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--files_name', type=str, nargs='+', required=True, help='List of file names')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')

    args = parser.parse_args()

    dataset_type = args.dataset_type
    files_name = args.files_name
    base_url = args.base_url

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, files_name: {files_name}")

    for file_name in files_name:
        path = base_url.format(file_name)
        update_file_names(path)

if __name__ == "__main__":
    main()
