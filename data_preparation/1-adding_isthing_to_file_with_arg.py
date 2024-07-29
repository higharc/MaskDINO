import json
import os
import argparse

def add_isthing_to_categories(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        
    if 'categories' in data:
        for category in data['categories']:
            if category['id'] != len(data['categories']) -1:
                category['isthing'] = 1
            else:
                category['isthing'] = 0
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

def process_json_files_in_directory(json_file):
    add_isthing_to_categories(json_file)
    print(f"Added 'isthing' to categories in {json_file}")

def main():
    parser = argparse.ArgumentParser(description='Process some JSON files.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--key_paths', type=str, nargs='+', required=True, help='List of key paths')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')

    args = parser.parse_args()

    key_paths = args.key_paths
    base_url = args.base_url
    dataset_type = args.dataset_type

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}")

    for key_path in key_paths:
        json_file_path = os.path.join(base_url, key_path, '_annotations.coco.json')
        process_json_files_in_directory(json_file_path)

if __name__ == "__main__":
    main()
