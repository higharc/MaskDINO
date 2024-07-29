#!/bin/bash

# rem Set common parameters
DATASET_TYPE="brochure_construction"
KEY_PATHS=("test train")
BASE_URL="/home/ubuntu/dataset/brochure_construction"
CATEGORIES="/home/ubuntu/dataset/brochure_construction/train/_annotations.coco.json"

# rem Run job 1: Update COCO JSON file names
echo Running job 1: Update COCO JSON file names
python 1-adding_isthing_to_file_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL
if [ $? -ne 0 ]; then
    echo "Job 1 failed!"
    exit 1
fi
echo Job 1 completed successfully!

# rem Run job 2: Generate Panoptic based on COCO
echo Running job 2: Generate Panoptic based on COCO
python 2-create_panoptic_annotations_file_with_arg.py --dataset_type %DATASET_TYPE% --key_paths %KEY_PATHS% --base_url "%BASE_URL%"
if [ $? -ne 0 ]; then
    echo "Job 2 failed!"
    exit 1
fi
echo Job 2 completed successfully!

# rem Run job 3: Changes image names with png from jpg
echo Running job 3: Changes image names with png from jpg
python 3-change_json_image_names_with_arg.py --dataset_type %DATASET_TYPE% --key_paths %KEY_PATHS% --base_url "%BASE_URL%"
if [ $? -ne 0 ]; then
    echo "Job 3 failed!"
    exit 1
fi
echo Job 3 completed successfully!

# rem Run job 4: Generate png files from jpg
echo Running job 4: Generate png files from jpg
python 4-convertor_jpg_to_png_with_arg.py --dataset_type %DATASET_TYPE% --key_paths %KEY_PATHS% --base_url "%BASE_URL%" --categories %CATEGORIES%
if [ $? -ne 0 ]; then
    echo "Job 4 failed!"
    exit 1
fi
echo Job 4 completed successfully!

# rem Run job 5: Generate panoptic segmentation masks
echo Running job 5: Generate panoptic segmentation masks
python 5-create_panoptic_masks_with_arg.py --dataset_type %DATASET_TYPE% --key_paths %KEY_PATHS% --base_url "%BASE_URL%/{}/_annotations.coco.json"
if [ $? -ne 0 ]; then
    echo "Job 5 failed!"
    exit 1
fi
echo Job 5 completed successfully!

# rem Run job 6: Generate semantic segmentation masks
echo Running job 6: Generate semantic segmentation masks
python convert_coco.py --dataset_type %DATASET_TYPE% --key_paths %KEY_PATHS% --base_url "%BASE_URL%"
if [ $? -ne 0 ]; then
    echo "Job 6 failed!"
    exit 1
fi
echo Job 6 completed successfully!

echo All jobs completed successfully!
# endlocal
# pause
