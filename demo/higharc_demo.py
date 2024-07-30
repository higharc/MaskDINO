# Copyright (c) Facebook, Inc. and its affiliates.
# Modified by Bowen Cheng from: https://github.com/facebookresearch/detectron2/blob/master/demo/demo.py
import argparse
import glob
import multiprocessing as mp
import json
import os
# fmt: off
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# fmt: on
from PIL import Image
import tempfile
import time
import warnings

import cv2
import numpy as np
import tqdm

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.projects.deeplab import add_deeplab_config
from detectron2.utils.logger import setup_logger

from maskdino import add_maskdino_config
from predictor import VisualizationDemo



coco_json = {
    "info": {
        "description": "Panoptic segmentation dataset",
        "version": "1.0",
        "year": 2024,
        "contributor": "Your Name",
        "date_created": "2024-06-07"
    },
    "licenses": [],
    "images": [],
    "annotations": [],
    "categories":  [
        {
            "id": 0,
            "name": "roomTypes",
            "supercategory": "none",
            "isthing": 1
        },
        {
            "id": 1,
            "name": "BALCONY",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 2,
            "name": "BASEMENT",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 3,
            "name": "BATHFULL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 4,
            "name": "BATHHALF",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 5,
            "name": "BATH_HALL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 6,
            "name": "BAY_WINDOW",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 7,
            "name": "BEDROOM",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 8,
            "name": "BED_CLOSET",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 9,
            "name": "CABINETS",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 10,
            "name": "CAFE",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 11,
            "name": "CHASE",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 12,
            "name": "CLOSET",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 13,
            "name": "COAT_CLOSET",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 14,
            "name": "DECK",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 15,
            "name": "DINING",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 16,
            "name": "DINING_NOOK",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 17,
            "name": "ENTRY",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 18,
            "name": "FLEX",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 19,
            "name": "FOYER",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 20,
            "name": "FRONT_PORCH",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 21,
            "name": "GARAGE",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 22,
            "name": "GARAGE_DETACH",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 23,
            "name": "GENERAL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 24,
            "name": "HALL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 25,
            "name": "KITCHEN",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 26,
            "name": "KITCHEN_HALL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 27,
            "name": "LAUNDRY",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 28,
            "name": "LIBRARY",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 29,
            "name": "LIVING",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 30,
            "name": "LIVING_HALL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 31,
            "name": "LOFT",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 32,
            "name": "MASTER_BATH",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 33,
            "name": "MASTER_BED",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 34,
            "name": "MASTER_HALL",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 35,
            "name": "MASTER_VESTIBULE",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 36,
            "name": "MECH",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 37,
            "name": "MUDROOM",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 38,
            "name": "NOOK",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 39,
            "name": "OFFICE",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 40,
            "name": "OPEN TO BELOW",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 41,
            "name": "PANTRY",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 42,
            "name": "PATIO",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 43,
            "name": "PORCH",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 44,
            "name": "POWDER",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 45,
            "name": "PR",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 46,
            "name": "REAR_PORCH",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 47,
            "name": "SHOWER",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 48,
            "name": "STAIRS",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 49,
            "name": "WALK_IN_CLOSET",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 50,
            "name": "WATER_CLOSET",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 51,
            "name": "bathtub",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 52,
            "name": "fireplace",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 53,
            "name": "master_vanity",
            "supercategory": "roomTypes",
            "isthing": 1
        },
        {
            "id": 54,
            "name": "workshop",
            "supercategory": "roomTypes",
            "isthing": 0
        }
    ]
}


def read_image(path, format="BGR"):
    img = Image.open(path)
    
    # Check if either width or height is greater than 2000
    while img.width > 2000 or img.height > 2000:
        # Resize both width and height by dividing by 2
        new_width = img.width // 2
        new_height = img.height // 2
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Check if the image has an alpha channel (transparency)
    if img.mode == "RGBA":
        # Create a white background image
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        
        # Paste the original image onto the white background
        white_bg.paste(img, (0, 0), img)
        
        img = white_bg
    
    # Convert to the desired format
    if format == "BGR":
        img = img.convert("RGB")
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    return img

def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    add_deeplab_config(cfg)
    add_maskdino_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="maskdino demo for builtin configs")
    parser.add_argument(
        "--config-file",
        default="configs/coco/instance-segmentation/maskdino_R50_bs16_50ep_3s.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


def test_opencv_video_format(codec, file_ext):
    with tempfile.TemporaryDirectory(prefix="video_format_test") as dir:
        filename = os.path.join(dir, "test_file" + file_ext)
        writer = cv2.VideoWriter(
            filename=filename,
            fourcc=cv2.VideoWriter_fourcc(*codec),
            fps=float(30),
            frameSize=(10, 10),
            isColor=True,
        )
        [writer.write(np.zeros((10, 10, 3), np.uint8)) for _ in range(30)]
        writer.release()
        if os.path.isfile(filename):
            return True
        return False


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))

    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)
    annotation_id = 0
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    if args.input:
        print(args.input[0])
        input_path = os.path.expanduser(args.input[0])
       
        if os.path.isdir(input_path):
            args.input = glob.glob(os.path.join(input_path, "*"))
        else:
            args.input = glob.glob(input_path)
        assert args.input, "The input path(s) was not found"
        idx = 0
        for path in tqdm.tqdm(args.input, disable=not args.output):
            if path[-4:] == "json" or path[-4:] == '.svg' or path[-4:] == '.pdf' or path[-4:] == '.jpg':
                continue
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            height, width = img.shape[:2]
            start_time = time.time()
            predictions, visualized_output = demo.run_on_image(img)
            panoptic_seg, segments_info = predictions['panoptic_seg']
            panoptic_seg = panoptic_seg.cpu().detach().numpy()
            
            image_info = {
                "file_name": os.path.basename(path),
                "height": height,
                "width": width,
                "id": idx
            }
            idx += 1
            coco_json['images'].append(image_info)
            annotations_info = []
            unique_ids = np.unique(panoptic_seg)
            for segment_id in unique_ids:
                if segment_id == 0:
                    continue  # Skip the 'nothing' category

                mask = (panoptic_seg == segment_id).astype(np.uint8)
                iscrowd = 0  # or 1, based on your context
                area = int(np.sum(mask))

                # Bounding box
                y_indices, x_indices = np.where(mask)
                bbox = [int(np.min(x_indices)), int(np.min(y_indices)), int(np.max(x_indices) - np.min(x_indices)), int(np.max(y_indices) - np.min(y_indices))]

                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                segmentation = []
                for contour in contours:
                    contour = contour.flatten().tolist()
                    segmentation.append(contour)
                    
                annotation_info = {
                    "id": annotation_id,
                    'image_id': image_info['id'],
                    "category_id": int(segment_id),
                    "area": area,
                    "bbox": bbox,
                    "segmentation": segmentation,
                    "iscrowd": iscrowd
                }
                annotations_info.append(annotation_info)
                annotation_id += 1
            coco_json['annotations'].extend(annotations_info)
            
            logger.info(
                "{}: {} in {:.2f}s".format(
                    path,
                    "detected {} instances".format(len(predictions["instances"]))
                    if "instances" in predictions
                    else "finished",
                    time.time() - start_time,
                )
            )

            if os.path.isdir(args.output):
                out_filename = os.path.join(args.output, os.path.basename(path))
            else:
                assert len(args.input) == 1, "Please specify a directory with args.output"
                out_filename = args.output
            visualized_output.save(out_filename)

    with open(args.output + "/_annotation_file.json", 'w') as f:
        json.dump(coco_json, f, indent=4)