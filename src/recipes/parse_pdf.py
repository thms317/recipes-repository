"""Module to parse PDF files into markdown using docling."""

import os
import shutil
from pathlib import Path

from docling.document_converter import DocumentConverter

converter = DocumentConverter()

recipes_dir = "scratch"
recipes = Path(recipes_dir).glob("*.pdf")
recipe_list = list(recipes)

print(f"Found {len(recipe_list)} recipe PDFs to process:")

for i, recipe in enumerate(recipe_list, 1):
    print(f"\n[{i}/{len(recipe_list)}] Processing {recipe.name}...")

    # Create a folder for this recipe's images
    recipe_name = recipe.stem
    recipe_folder = Path(recipes_dir) / recipe_name
    images_folder = recipe_folder / "images"

    # Create folders if they don't exist
    os.makedirs(images_folder, exist_ok=True)

    print("  Converting PDF to markdown...")
    result = converter.convert(recipe)

    # Extract images if available
    print("  Extracting images...")
    image_count = 0
    if hasattr(result, "images") and result.images:
        for i, img in enumerate(result.images):
            image_path = images_folder / f"image_{i + 1}.png"
            with open(image_path, "wb") as img_file:
                img_file.write(img)
            image_count += 1

    # Process markdown to replace image placeholders
    print("  Processing markdown content...")
    recipe_md = result.document.export_to_markdown()

    # Replace image placeholders with actual image references
    if image_count > 0:
        lines = recipe_md.split("\n")
        for i in range(len(lines)):
            if "<!-- image -->" in lines[i]:
                img_num = lines[i].count("<!-- image -->")
                for j in range(img_num):
                    img_idx = j + 1
                    img_path = f"images/image_{img_idx}.png"
                    lines[i] = lines[i].replace(
                        "<!-- image -->",
                        f"![Image {img_idx}]({img_path})",
                        1,
                    )
        recipe_md = "\n".join(lines)

    # Save markdown file
    markdown_path = recipe_folder / f"{recipe_name}.md"
    print(f"  Saving markdown to {markdown_path}")
    with open(markdown_path, "w") as f:
        f.write(recipe_md)

    # Also save a copy at the original location for backward compatibility
    with open(recipe.with_suffix(".md"), "w") as f:
        f.write(recipe_md)

    print(f"  Completed: Extracted {image_count} images and saved markdown.")

print("\nAll recipes processed successfully!")
