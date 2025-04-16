"""Module to parse PDF files into markdown using docling."""

from pathlib import Path

import fitz  # type: ignore[import-untyped]
from docling.document_converter import DocumentConverter

# Define the directory containing the recipes
recipes_dir = "scratch"

# Get all recipe PDFs in the directory
recipes = Path(recipes_dir).glob("*.pdf")
recipe_list = list(recipes)

print(f"Found {len(recipe_list)} recipe PDFs to process:")

# Process each recipe
for i, recipe in enumerate(recipe_list, 1):
    print(f"\n[{i}/{len(recipe_list)}] Processing {recipe.name}...")

    # Create folders
    recipe_name = recipe.stem
    recipe_folder = Path(recipes_dir) / recipe_name
    images_folder = recipe_folder / "images"
    images_folder.mkdir(parents=True, exist_ok=True)

    # First extract images using PyMuPDF
    print("  Extracting images...")
    image_count = 0

    # Open the PDF
    pdf_document = fitz.open(recipe)

    # Iterate through pages
    for page_num, page in enumerate(pdf_document):
        # Get images from the page
        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]  # Get the XREF of the image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Generate image file name
            image_filename = f"image_p{page_num + 1}_{img_index + 1}.{image_ext}"
            image_path = images_folder / image_filename

            # Save the image
            with Path.open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            image_count += 1
            print(f"    Extracted image: {image_filename}")

    pdf_document.close()

    # Convert PDF to markdown using docling

    # Import the document converter
    converter = DocumentConverter()

    print("  Converting PDF to markdown...")
    result = converter.convert(recipe)

    # Get the markdown content
    print("  Processing markdown content...")
    recipe_md = result.document.export_to_markdown()

    # Save markdown file
    markdown_path = recipe_folder / f"{recipe_name}.md"
    with Path.open(markdown_path, "w") as f:
        f.write(recipe_md)
    print(f"  Completed: Extracted {image_count} images and saved markdown.")

print("\nAll recipes processed successfully!")
