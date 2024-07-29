#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates.

import functools
import json
import multiprocessing as mp
import numpy as np
import os
import time
from fvcore.common.download import download
from panopticapi.utils import rgb2id
from PIL import Image

from detectron2.data.datasets.builtin_meta import COCO_CATEGORIES


def _process_panoptic_to_semantic(input_panoptic, output_semantic, segments, id_map):
    panoptic = np.asarray(Image.open(input_panoptic), dtype=np.uint32)
    panoptic = rgb2id(panoptic)
    output = np.zeros_like(panoptic, dtype=np.uint8) + 255
    for seg in segments:
        cat_id = seg["category_id"]
        # if cat_id > 45:
        #     cat_id = 45
        new_cat_id = id_map[cat_id]
        output[panoptic == seg["id"]] = new_cat_id
    Image.fromarray(output).save(output_semantic)


def separate_coco_semantic_from_panoptic(panoptic_json, panoptic_root, sem_seg_root, categories):
    """
    Create semantic segmentation annotations from panoptic segmentation
    annotations, to be used by PanopticFPN.
    It maps all thing categories to class 0, and maps all unlabeled pixels to class 255.
    It maps all stuff categories to contiguous ids starting from 1.
    Args:
        panoptic_json (str): path to the panoptic json file, in COCO's format.
        panoptic_root (str): a directory with panoptic annotation files, in COCO's format.
        sem_seg_root (str): a directory to output semantic annotation files
        categories (list[dict]): category metadata. Each dict needs to have:
            "id": corresponds to the "category_id" in the json annotations
            "isthing": 0 or 1
    """
    os.makedirs(sem_seg_root, exist_ok=True)

    id_map = {}  # map from category id to id in the output semantic annotation
    assert len(categories) <= 60
    for i, k in enumerate(categories):
        id_map[k] = i
    # what is id = 0?
    # id_map[0] = 255
    print(id_map)

    with open(panoptic_json) as f:
        obj = json.load(f)

    pool = mp.Pool(processes=max(mp.cpu_count() // 2, 4))

    def iter_annotations():
        for anno in obj["annotations"]:
            file_name = anno["file_name"]
            segments = anno["segments_info"]
            input = os.path.join(panoptic_root, file_name.replace(".jpg", ".png"))
            output = os.path.join(sem_seg_root, file_name)
            yield input, output, segments

    print("Start writing to {} ...".format(sem_seg_root))
    start = time.time()
    pool.starmap(
        functools.partial(_process_panoptic_to_semantic, id_map=id_map),
        iter_annotations(),
        chunksize=100,
    )
    print("Finished. time: {:.2f}s".format(time.time() - start))



mscoco_category2name = {
    0: "architectural-plans-LGP8",
    1: "BALCONY",
    2: "BASEMENT",
    3: "BATHFULL",
    4: "BATHHALF",
    5: "BATH_HALL",
    6: "BAY_WINDOW",
    7: "BEDROOM",
    8: "BED_CLOSET",
    9: "CABINETS",
    10: "CAFE",
    11: "CHASE",
    12: "CLOSET",
    13: "COAT_CLOSET",
    14: "DECK",
    15: "DINING",
    16: "DINING_NOOK",
    17: "ENTRY",
    18: "FLEX",
    19: "FOYER",
    20: "FRONT_PORCH",
    21: "GARAGE",
    22: "GARAGE_DETACH",
    23: "GENERAL",
    24: "HALL",
    25: "KITCHEN",
    26: "KITCHEN_HALL",
    27: "LAUNDRY",
    28: "LIBRARY",
    29: "LIVING",
    30: "LIVING_HALL",
    31: "LOFT",
    32: "MASTER_BATH",
    33: "MASTER_BED",
    34: "MASTER_HALL",
    35: "MASTER_VESTIBULE",
    36: "MECH",
    37: "MUDROOM",
    38: "NOOK",
    39: "OFFICE",
    40: "OPEN TO BELOW",
    41: "PANTRY",
    42: "PATIO",
    43: "PORCH",
    44: "POWDER",
    45: "PR",
    46: "REAR_PORCH",
    47: "SHOWER",
    48: "STAIRS",
    49: "WALK_IN_CLOSET",
    50: "WATER_CLOSET"
}





if __name__ == "__main__":
    
    dataset_type = "expriment_three"
    key_paths = []
    base_url = ""
    if dataset_type == "construction":
        key_paths = ["valid", "test", "train"]
        # base_url = "/Users/amin/Desktop/higharc/Datasets/Laleled-2024-05-29/auto_translate_v4.v3i.coco-segmentation"
        base_url = "../../dataset/seg_object_detection/auto_translate_v4-3"
        
    elif dataset_type == 'pulte_unlabel':
        key_paths = ['floorplans']
        base_url = "../../dataset/data_pulte/pulte"

    elif dataset_type == 'pulte_lable_81':
        key_paths = ["valid", "train"]
        base_url = "../../dataset/experiment_two"
        
    elif dataset_type == 'pseudo':
        key_paths = ["train"]
        base_url = "/home/ubuntu/code/MaskDINO/output_experiment_two/output/pseudo"
    
    elif dataset_type == 'expriment_three':
        key_paths = ["test", "train"]
        base_url = "../../dataset/expriment_three_1"
    

    for key_path in key_paths: 
        separate_coco_semantic_from_panoptic(
            os.path.join(base_url, "{}/_panoptic_annotations.coco.json".format(key_path)),
            # os.path.join(base_url, "{}/_panoptic_annotation_pulte_maskdino_augmented_file.json".format(key_path)),
            os.path.join(base_url, "panoptic_masks/{}".format(key_path)),
            # os.path.join(base_url, "panoptic_masks_maskdino_augmented/{}".format(key_path)),
            os.path.join(base_url, "panoptic_semseg_{}".format(key_path)),
            # os.path.join(base_url, "panoptic_semseg_maskdino_augmented_{}".format(key_path)),
            mscoco_category2name,
        )