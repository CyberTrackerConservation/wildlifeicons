import os
import json
import re

ICONS_DIR = 'icons'
OUTPUT_JSON = 'icons.json'
SUPPORTED_EXTENSIONS = {'.svg', '.png', '.jpg', '.jpeg', '.webp'}

def determine_style(keywords):
    if not keywords:
        return ""
    if keywords[0].lower() == "aerial":
        return "aerial"
    if keywords[0] == "SMART":
        if len(keywords) > 1:
            if keywords[1].lower() == "mono":
                return "monochrome"
            return keywords[1]
        return ""
    if keywords[0] == "EarthRanger":
        return "compact"
    return keywords[0]

def scan_icons():
    icons = []
    for root, dirs, files in os.walk(ICONS_DIR):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                rel_dir = os.path.relpath(root, ICONS_DIR)
                keywords = [k for k in rel_dir.split(os.sep) if k != '.'] if rel_dir != '.' else []
                icon_path = os.path.join(root, file)
                icon_path = icon_path.replace("\\", "/")  # For Windows compatibility
                icon_name = os.path.splitext(file)[0]
                raw_name = icon_name.replace('_', ' ').title()
                # Remove trailing "Icon"
                clean_name = re.sub(r'\s*Icon$', '', raw_name, flags=re.IGNORECASE)
                # Remove whole words "glyph" or "color" (case-insensitive)
                clean_name = re.sub(r'\b(glyph|color)\b', '', clean_name, flags=re.IGNORECASE)
                # Remove extra spaces
                clean_name = clean_name.strip()
                icons.append({
                    "name": clean_name,
                    "filename": os.path.relpath(icon_path, ICONS_DIR).replace("\\", "/"),
                    "description": "",
                    "keywords": keywords,
                    "style": determine_style(keywords)
                })
    return icons

def main():
    icons = scan_icons()
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({"icons": icons}, f, indent=2, ensure_ascii=False)
    print(f"Written {len(icons)} icons to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()