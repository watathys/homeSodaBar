#!/usr/bin/env python3
"""Generate all recipe pages with video-first layout and VideoObject schema for SEO."""

import os

RECIPES = [
    "Golden Hour", "Raspberry Dream", "The Utah Doc", "Islander Doctor", "Southern Gentleman",
    "Black Forest", "Chocolate Covered Strawberry", "The Founder", "The Millionaire",
    "Just Peachy Coke", "Pineapple Express", "The Loaded Diet", "Vanilla Coke Remix",
    "Raspberry Royale", "Blackberry Lime", "Baja Gold", "Tiger's Stripe", "Peaches & Cream",
    "Key Lime Pie", "Fruit Punch", "Raspberry Dew", "Paradise City", "Pink Lagoon",
    "Hula Girl", "Strawberry Shortcake", "White Wash", "Limeade Crunch", "Peachy Keen",
    "Mojito Mock", "Berry Lemonade", "Tropical Storm", "Wizard Brew", "The Brown Cow",
    "Toasted Root Beer", "The Garden Spritz", "The Amalfi Splash", "The Napa Soda",
    "Summer House", "Island Sparkler", "The Bramble Patch", "The Pink Slush",
    "The Hawaiian High", "Dreamy Orange", "Cosmic Colada", "The Starlet", "The Bullrider",
    "Electric Peach", "Skinny Kicker", "The Midnight Sky", "The Tropic Thunder",
    "The White Flight", "Neon Nectar",
]

# Recipes that have YouTube Shorts (video ID)
VIDEO_IDS = {
    "toasted-root-beer": "lppOTR_XrEM",
    "the-millionaire": "0tHoHN6SriQ",
    "the-starlet": "OMCVoaObY_c",
    "the-amalfi-splash": "_V4JG55Fr4k",
    "raspberry-royale": "Q22QLiromgk",
    "wizard-brew": "BqtkkwNE-4E",
    "strawberry-shortcake": "CgJ-5k5CAOA",
    "islander-doctor": "6a0vX-cSXxY",
    "just-peachy-coke": "rboeu9tXWEU",
    "hula-girl": "_xoKVQWsJBU",
    "southern-gentleman": "hyw5_dh33tY",
}

VIDEO_PLACEHOLDER = """                <div class="video-placeholder">
                    Instructional video still being created, check back soon
                </div>"""


def slug(recipe: str) -> str:
    return recipe.lower().replace(" ", "-").replace("&", "and").replace("'", "").replace("'", "")


def video_object_schema(recipe_name: str, video_id: str) -> str:
    return f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "VideoObject",
      "name": "How to Make {recipe_name} | Kazzi Soda Recipe",
      "description": "Learn how to make {recipe_name} dirty soda at home with this recipe from KazziSoda.",
      "thumbnailUrl": "https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
      "embedUrl": "https://www.youtube.com/embed/{video_id}",
      "contentUrl": "https://www.youtube.com/watch?v={video_id}"
    }}
    </script>
'''


def video_embed(video_id: str) -> str:
    return f'<iframe width="100%" height="100%" src="https://www.youtube-nocookie.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin" title="YouTube video player"></iframe>'


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base, "recipe-template.html")
    recipes_dir = os.path.join(base, "recipes")

    with open(template_path, "r") as f:
        template = f.read()

    for recipe in RECIPES:
        s = slug(recipe)
        filepath = os.path.join(recipes_dir, f"{s}.html")

        if s in VIDEO_IDS:
            video_id = VIDEO_IDS[s]
            video_embed_html = video_embed(video_id)
            video_schema = video_object_schema(recipe, video_id)
        else:
            video_embed_html = VIDEO_PLACEHOLDER
            video_schema = ""

        content = (
            template.replace("{{RECIPE_NAME}}", recipe)
            .replace("{{VIDEO_EMBED}}", video_embed_html)
            .replace("{{VIDEO_SCHEMA}}", video_schema)
        )

        with open(filepath, "w") as f:
            f.write(content)
        print(f"Generated: {filepath}")

    print(f"\nDone. Generated {len(RECIPES)} recipe pages.")
    print(f"  - {len(VIDEO_IDS)} with VideoObject schema + embedded video")
    print(f"  - {len(RECIPES) - len(VIDEO_IDS)} with placeholder")


if __name__ == "__main__":
    main()
