
import random


def generate_random_color():
    return [random.randint(0, 255) for _ in range(3)]

categories = [
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


HIGHARC_CATEGORIES = [
    {'color': generate_random_color(), 'isthing': 1 if i < len(categories) - 1 else 0, 'id': cat['id'], 'name': cat['name']} for i, cat in enumerate(categories)
]