#!/usr/bin/env python3
import csv, json, random, os
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEMPLATE = (BASE_DIR / 'templates' / 'recipe-template.md').read_text()
AFFILIATES_CSV = BASE_DIR / 'data' / 'affiliates.csv'
OUTPUT_DIR = BASE_DIR / 'output'

SEEDS = [
    {'name': 'Spicy Raccoon-Free Tacos', 'base': ['tortillas','beans','onion','garlic','tomato','cumin','chili']},
    {'name': 'Krampus Cocoa Bombs', 'base': ['cocoa','milk','sugar','vanilla','cinnamon']},
    {'name': 'Ambient Focus Smoothie', 'base': ['banana','spinach','almond milk','chia','honey']},
    {'name': 'Dark Fantasy Mushroom Pasta', 'base': ['pasta','mushrooms','garlic','butter','parsley','parmesan']},
]

def read_affiliates():
    links = []
    if AFFILIATES_CSV.exists():
        with open(AFFILIATES_CSV, newline='') as f:
            for row in csv.DictReader(f):
                links.append(f"{row['name']}: {row['affiliate_url']}")
    return links

def to_list_block(items):
    return "\n".join([f"- {i}" for i in items])

def gen_schema(name, ingredients, instructions):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": name,
        "recipeIngredient": ingredients,
        "recipeInstructions": [{"@type":"HowToStep","text": step} for step in instructions],
        "author": {"@type": "Person", "name": "AvaTarArTs"}
    }, indent=2)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    seed = random.choice(SEEDS)
    name = seed['name']
    ingredients = seed['base'] + random.sample(['olive oil','salt','pepper','paprika','lemon','basil','oregano'], k=3)
    instructions = [
        "Prep all ingredients and preheat pan/oven as needed.",
        "Combine base ingredients and season to taste.",
        "Cook until textures/flavors meld; plate and garnish.",
    ]
    content = TEMPLATE
    content = content.replace('{{RECIPE_NAME}}', name)
    content = content.replace('{{PREP_TIME}}', '10m').replace('{{COOK_TIME}}', '20m').replace('{{SERVES}}', '2')
    content = content.replace('{{INGREDIENTS_LIST}}', to_list_block(ingredients))
    content = content.replace('{{INSTRUCTIONS_LIST}}', to_list_block([f"Step {i+1}: {s}" for i,s in enumerate(instructions)]))
    content = content.replace('{{TIP_1}}', 'Taste and adjust spice for audience.')
    content = content.replace('{{TIP_2}}', 'Double batch for meal prep.')
    content = content.replace('{{CALORIES}}', '420').replace('{{PROTEIN}}', '12').replace('{{FAT}}', '14').replace('{{CARBS}}', '60')
    content = content.replace('{{AFFILIATE_LINKS}}', '; '.join(read_affiliates()) or '—')
    content = content.replace('{{RECIPE_SCHEMA}}', gen_schema(name, ingredients, instructions))

    filename = name.lower().replace(' ','-') + '.md'
    out = OUTPUT_DIR / filename
    out.write_text(content)
    print(f"✅ Generated: {out}")

if __name__ == '__main__':
    main()
