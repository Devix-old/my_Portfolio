steps = [
    {
        "number": 1,
        "step": "Take a large bowl mix in the ginger and garlic paste, yogurt, red chilly powder, turmeric powder, and salt.",
        "ingredients": [
            {
                "id": 2043,
                "name": "turmeric",
                "localizedName": "turmeric",
                "image": "turmeric.jpg"
            },
            {
                "id": 2009,
                "name": "chili powder",
                "localizedName": "chili powder",
                "image": "chili-powder.jpg"
            },
            {
                "id": 10111215,
                "name": "garlic paste",
                "localizedName": "garlic paste",
                "image": "garlic-paste.png"
            },
            {
                "id": 11216,
                "name": "ginger",
                "localizedName": "ginger",
                "image": "ginger.png"
            },
            {
                "id": 1116,
                "name": "yogurt",
                "localizedName": "yogurt",
                "image": "plain-yogurt.jpg"
            },
            {
                "id": 2047,
                "name": "salt",
                "localizedName": "salt",
                "image": "salt.jpg"
            }
        ],
        "equipment": []
    },
    {
        "number": 2,
        "step": "Add the chicken pieces to this mix and leave it for 2 hours to marinate.",
        "ingredients": [
            {
                "id": 5006,
                "name": "chicken",
                "localizedName": "chicken",
                "image": "whole-chicken.jpg"
            }
        ],
        "equipment": []
    },
    {
        "number": 3,
        "step": "Heat oil in a frying pan and fry the chicken pieces until they are cooked.",
        "ingredients": [
            {
                "id": 4582,
                "name": "cooking oil",
                "localizedName": "cooking oil",
                "image": "vegetable-oil.jpg"
            }
        ],
        "equipment": [
            {
                "id": 404727,
                "name": "frying pan",
                "localizedName": "frying pan",
                "image": "pan.png"
            }
        ]
    }
]

for step in steps:
    for ingredient in step.ingredients:
        print(ingredient.name)
        
