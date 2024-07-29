import os
import cv2
import numpy as np
import json
import argparse
from panopticapi.utils import id2rgb
from utils import print_


def load_annotations(annotations_path):
    # Load the annotations file in COCO format
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)
    return annotations

def generate_segmentation_masks(annotations, image_shape, image_info):
    # Initialize an empty array to store the segmentation masks
    segmentation_masks = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint8)

    # Iterate through the annotations to generate masks for each category
    for annotation in annotations['annotations']:
        if annotation['image_id'] == image_info['id']:
            segmentation_mask = np.zeros((image_shape[0], image_shape[1], 3), dtype=np.uint8)
            segmentations = annotation['segmentation']

            for segmentation in segmentations:
                pts = np.array(segmentation).reshape((-1, 1, 2)).astype(np.int32)
                color = id2rgb(annotation['id'])
                cv2.fillPoly(segmentation_mask, [pts], color)
            # Add the mask to the overall segmentation masks
            segmentation_masks = np.maximum(segmentation_masks, segmentation_mask)

    return segmentation_masks

def save_panoptic_segmentation(segmentation_masks, output_path):
    cv2.imwrite(output_path, segmentation_masks)
 
def main():
    parser = argparse.ArgumentParser(description='Generate and save panoptic segmentation masks.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--key_paths', type=str, nargs='+', required=True, help='List of key paths')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')
    parser.add_argument('--not_add_log', action="store_true", help='Add job log in the output or not')

    args = parser.parse_args()

    dataset_type = args.dataset_type
    key_paths = args.key_paths
    base_url = args.base_url

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}")

    for key_path in key_paths:   
        print(f"Processing key path: {key_path}")
        image_dir = os.path.join(base_url, key_path)
        print(f"Image directory: {image_dir}")

        # Path to the annotations file
        annotations_path = '_annotations.coco.json'

        # Output directory for panoptic segmentation masks
        output_dir = os.path.join(base_url, "panoptic_masks", key_path)
        os.makedirs(output_dir, exist_ok=True)

        # Load the annotations
        annotations = load_annotations(os.path.join(image_dir, annotations_path))

        # Process each image in the directory
        for image_info in annotations['images']:
            filename = image_info['file_name']
            image_path = os.path.join(image_dir, filename)
            output_path = os.path.join(output_dir, filename[:-4] + ".png")

            # Load the image
            image = cv2.imread(image_path)

            # Generate segmentation masks
            segmentation_masks = generate_segmentation_masks(annotations, image.shape, image_info)

            segmentation_masks = cv2.cvtColor(segmentation_masks, cv2.COLOR_BGR2RGB)

            # Save the panoptic segmentation mask
            save_panoptic_segmentation(segmentation_masks, output_path)

if __name__ == "__main__":
    main()
