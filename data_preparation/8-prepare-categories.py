import functools
import json
import multiprocessing as mp
import numpy as np
import os
import time
import argparse
from utils import print_

def modify_categories(input_filename, output_filename, add_log):
    # Read the JSON data from the input file
    with open(input_filename, 'r') as file:
        data = json.load(file)
    
    # Write the modified data to the output file
    with open(output_filename, 'w') as file:
        json.dump(data['categories'], file, indent=4)
    
    print_(f"the model is saved in {output_filename}", add_log)


def main():
    parser = argparse.ArgumentParser(description='Generate and save semantic segmentation masks from panoptic annotations.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--key_paths', type=str, nargs='+', required=True, help='List of key paths')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')
    parser.add_argument('--not_add_log', action="store_true", help='Add job log in the output or not')
    
    args = parser.parse_args()

    dataset_type = args.dataset_type
    key_paths = args.key_paths
    base_url = args.base_url
    add_log = not args.not_add_log
    
    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}, add_log: {add_log}")
    
    annotations_path = os.path.join(base_url, key_paths[0], '_annotations.coco.json')
    modify_categories(annotations_path, 'output.json', add_log)
    

if __name__ == "__main__":
    main()
    