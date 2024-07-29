import json
import os
import argparse

def convert_coco_to_panoptic(coco_json):
    res = dict()
    res['info'] = coco_json.get('info', [])
    res['licenses'] = coco_json.get('licenses', [])
    res['categories'] = coco_json['categories']
    res['images'] = coco_json['images']

    panoptic_annotations = []
    for image_info in coco_json['images']:
        panoptic_annotation = {
            'id': image_info['id'],
            "file_name": image_info['file_name'],
            "image_id": image_info['id'],
            "segments_info": []
        }
        for annotation in coco_json['annotations']:
            if annotation['image_id'] == image_info['id']:
                segment_info = {
                    "id": annotation['id'],
                    "category_id": annotation['category_id'],
                    "iscrowd": annotation['iscrowd'],
                    "bbox": annotation['bbox'],
                    "segmentation": annotation['segmentation'],
                    "area": annotation['area']
                }
                panoptic_annotation["segments_info"].append(segment_info)
        panoptic_annotations.append(panoptic_annotation)

    res['annotations'] = panoptic_annotations
    return res

def main():
    parser = argparse.ArgumentParser(description='Convert COCO annotations to panoptic format.')
    parser.add_argument('--dataset_type', type=str, required=True, help='Type of dataset')
    parser.add_argument('--key_paths', type=str, nargs='+', required=True, help='List of key paths')
    parser.add_argument('--base_url', type=str, required=True, help='Base URL for the dataset')

    args = parser.parse_args()

    key_paths = args.key_paths
    base_url = args.base_url
    dataset_type = args.dataset_type

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}")

    for t in key_paths:    
        anno_file = os.path.join(base_url, t, "_annotations.coco.json")
        print(f"Processing file: {anno_file}")
        
        with open(anno_file, 'r') as f:
            coco_json = json.load(f)
        
        panoptic_json = convert_coco_to_panoptic(coco_json)

        out_file = os.path.join(base_url, t, "_panoptic_annotations.coco.json")
        with open(out_file, 'w') as f:
            json.dump(panoptic_json, f, indent=2)
        print(f"Saved panoptic annotations to {out_file}")

if __name__ == "__main__":
    main()
