#!/bin/bash
# conda activate maskdino

# rem Set common parameters
DATASET_TYPE="brochure_construction_v2"
KEY_PATHS=("test train")
BASE_URL="/home/ubuntu/dataset/brochure_construction_v2"

# rem Run job 1: Update COCO JSON file names
echo Running job 1: Update COCO JSON file names
echo ---- 
python 1-adding_isthing_to_file_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 1 failed!"
    exit 1
fi
echo Job 1 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------


# rem Run job 2: Generate Panoptic based on COCO
echo Running job 2: Generate Panoptic based on COCO
echo ---- 
python 2-create_panoptic_annotations_file_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 2 failed!"
    exit 1
fi
echo Job 2 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------

# rem Run job 3: Changes image names with png from jpg
echo Running job 3: Changes image names with png from jpg
echo ---- 
python 3-change_json_image_names_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 3 failed!"
    exit 1
fi
echo Job 3 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------

# rem Run job 4: Generate png files from jpg
echo Running job 4: Generate png files from jpg
echo ---- 
python 4-convertor_jpg_to_png_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 4 failed!"
    exit 1
fi
echo Job 4 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------

# rem Run job 5: Generate panoptic segmentation masks
echo Running job 5: Generate panoptic segmentation masks
echo ---- 
python 5-create_panoptic_masks_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 5 failed!"
    exit 1
fi
echo Job 5 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------

# rem Run job 6: Generate semantic segmentation masks
echo Running job 6: Generate semantic segmentation masks
echo ---- 
python 6-create_separate_semantic_with_arg.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 6 failed!"
    exit 1
fi
echo Job 6 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------


# rem Run job 7: Separate Coco Semantic From Panoptic
echo Running job 7: Separate Coco Semantic From Panoptic
echo ---- 
python 7-prepare_higharc_semantic_annos_from_panoptic_annos.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 7 failed!"
    exit 1
fi
echo Job 7 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------

# rem Run job 8: Prepare category for the main code
echo Running job 8: Prepare category for the main code
echo ---- 
python 8-prepare-categories.py --dataset_type $DATASET_TYPE --key_paths $KEY_PATHS --base_url $BASE_URL --not_add_log
if [ $? -ne 0 ]; then
    echo "Job 8 failed!"
    exit 1
fi
echo Job 8 completed successfully!
echo -------------------------------------------------------------------------------------------------------------------


echo All jobs completed successfully!
# endlocal
# pause
