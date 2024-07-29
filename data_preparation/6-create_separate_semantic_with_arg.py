import os
import cv2
import numpy as np
import json
import argparse
from panopticapi.utils import rgb2id
from PIL import Image
import multiprocessing as mp
import time
import functools
import random
from utils import print_


# Function to generate a random color
def generate_random_color():
    return [random.randint(0, 255) for _ in range(3)]


def load_annotations(annotations_path):
    # Load the annotations file in COCO format
    with open(annotations_path, 'r') as f:
        annotations = json.load(f)
    return annotations

def _process_panoptic_to_semantic(input_panoptic, output_semantic, segments, id_map):
    panoptic = np.asarray(Image.open(input_panoptic), dtype=np.uint32)
    panoptic = rgb2id(panoptic)
    output = np.zeros_like(panoptic, dtype=np.uint8) + 255
    for seg in segments:
        cat_id = seg["category_id"]
        new_cat_id = id_map[cat_id]
        output[panoptic == seg["id"]] = new_cat_id
    Image.fromarray(output).save(output_semantic)

def separate_coco_semantic_from_panoptic(panoptic_json, panoptic_root, sem_seg_root, categories, add_log):
    os.makedirs(sem_seg_root, exist_ok=True)

    stuff_ids = [k["id"] for k in categories if k["isthing"] == 0]
    thing_ids = [k["id"] for k in categories if k["isthing"] == 1]
    id_map = {}  # map from category id to id in the output semantic annotation
    assert len(stuff_ids) <= 254
    for i, stuff_id in enumerate(stuff_ids):
        id_map[stuff_id] = i + 1
    for thing_id in thing_ids:
        id_map[thing_id] = 0
    id_map[0] = 255

    with open(panoptic_json) as f:
        obj = json.load(f)

    pool = mp.Pool(processes=max(mp.cpu_count() // 2, 4))

    def iter_annotations():
        for anno in obj["annotations"]:
            file_name = anno["file_name"]
            segments = anno["segments_info"]
            input = os.path.join(panoptic_root, file_name)
            output = os.path.join(sem_seg_root, file_name)
            yield input, output, segments

    print_("Start writing to {} ...".format(sem_seg_root), add_log)
    start = time.time()
    pool.starmap(
        functools.partial(_process_panoptic_to_semantic, id_map=id_map),
        iter_annotations(),
        chunksize=100,
    )
    print_("Finished. time: {:.2f}s".format(time.time() - start), add_log)

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

    annotations_path = os.path.join(base_url, key_paths[0], '_annotations.coco.json')

    with open(annotations_path, 'r') as f:
        info = json.load(f)
        
    categories = info['categories']
        
    HIGHARC_CATEGORIES = [
        {'color': generate_random_color(), 'isthing': 1, 'id': cat['id'], 'name': cat['name']} for cat in categories
    ]

    print(f"Processing dataset_type: {dataset_type}, base_url: {base_url}, key_paths: {key_paths}, add_log: {add_log}")

    for key_path in key_paths:   
        separate_coco_semantic_from_panoptic(
            os.path.join(base_url, "{}/_panoptic_annotations.coco.json".format(key_path)),
            os.path.join(base_url, "panoptic_masks/{}".format(key_path)),
            os.path.join(base_url, "panoptic_stuff/{}".format(key_path)),
            HIGHARC_CATEGORIES,
            add_log
        )

if __name__ == "__main__":
    main()