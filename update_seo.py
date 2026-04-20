import os
import glob
import re
import json

recipe_files = glob.glob('recipes/*.html')

for filepath in recipe_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract name from title
    title_match = re.search(r'<title>(.*?)\s*\|', content)
    if not title_match:
        continue
    recipe_name = title_match.group(1).strip()

    # Update Title
    new_title = f"<title>{recipe_name} | Best Dirty Soda Recipe | KazziSoda</title>"
    content = re.sub(r'<title>.*?</title>', new_title, content)

    # Update H1
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    if h1_match:
        h1_text = h1_match.group(1)
        if 'Dirty Soda' not in h1_text:
            content = re.sub(r'<h1>(.*?)</h1>', r'<h1>\1 Dirty Soda Recipe</h1>', content)

    # Add Meta Description if missing
    if '<meta name="description"' not in content:
        desc = f'<meta name="description" content="Learn how to make the {recipe_name} dirty soda recipe at home. Get the exact syrup ratios, ingredients, and step-by-step instructions for this viral drink.">'
        content = re.sub(r'(<meta name="viewport".*?>)', r'\1\n    ' + desc, content)

    # Add Recipe Schema
    if '"@type": "Recipe"' not in content:
        schema = {
            "@context": "https://schema.org/",
            "@type": "Recipe",
            "name": f"{recipe_name} Dirty Soda",
            "description": f"How to make the perfect {recipe_name} dirty soda at home with exact syrup ratios and ingredients.",
            "recipeCategory": "Drink",
            "keywords": "dirty soda, dirty soda recipe, soda shop recipe, mocktail"
        }
        schema_str = json.dumps(schema, indent=4)
        # Indent the schema properly
        schema_str = '\n'.join(['    ' + line for line in schema_str.split('\n')])
        schema_html = f'\n    <!-- Recipe Schema for SEO -->\n    <script type="application/ld+json">\n{schema_str}\n    </script>'
        content = content.replace('</head>', schema_html + '\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(recipe_files)} recipe files for SEO.")
