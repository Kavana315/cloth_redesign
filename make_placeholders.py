from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("assets", exist_ok=True)

ideas = [
    ("Tshirt", "tote_bag", (60, 120, 200)),
    ("Tshirt", "cushion_cover", (60, 120, 200)),
    ("Tshirt", "cleaning_cloths", (60, 120, 200)),
    ("Shirt", "apron", (200, 200, 60)),
    ("Shirt", "pillow_cover", (200, 200, 60)),
    ("Shirt", "patchwork_quilt", (200, 200, 60)),
    ("Jeans", "denim_tote_bag", (30, 60, 130)),
    ("Jeans", "denim_shorts", (30, 60, 130)),
    ("Jeans", "pouch_or_pencil_case", (30, 60, 130)),
    ("Dress", "skirt", (200, 80, 140)),
    ("Dress", "scarf", (200, 80, 140)),
    ("Dress", "fabric_coasters", (200, 80, 140)),
    ("Jacket", "backpack", (80, 80, 80)),
    ("Jacket", "laptop_sleeve", (80, 80, 80)),
    ("Jacket", "vest", (80, 80, 80)),
]

for cls, name, color in ideas:
    img = Image.new("RGB", (400, 400), color)
    draw = ImageDraw.Draw(img)
    text = f"{cls}\n\n{name.replace('_', ' ').title()}"
    draw.multiline_text((30, 160), text, fill="white", spacing=8)
    img.save(f"assets/{cls}_{name}.jpg")

print("✅ Created 15 placeholder images in assets/")