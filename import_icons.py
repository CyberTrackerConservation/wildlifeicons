#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Icons Script

This script scans the icons directory recursively and creates a JSON file
containing an array of objects with filename information.
"""

import os
import json
import re
import yaml
from pathlib import Path

SCIENTIFIC_NAMES = 'scientific_names.txt'

def load_scientific_names():
    with open(SCIENTIFIC_NAMES, 'r', encoding='utf-8') as f:
        return {line.strip().split(';')[0]: line.strip().split(';')[1] for line in f.readlines()}

def normalize_filename(filename):
    """
    Normalize filename to create a key:
    - Remove file extension
    - Replace spaces with underscores
    - Remove "icon" suffix (case insensitive)
    - Remove "glyph" suffix (case insensitive)
    - Remove "line" suffix (case insensitive)
    - Remove "color" suffix (case insensitive)
    - Remove "black" suffix (case insensitive)
    - Remove "rep" suffix (case insensitive)
    - Remove "ns" suffix (case insensitive)
    - Remove "_1" and "_2" suffixes
    - Remove apostrophes and parentheses
    - Convert to lowercase
    
    Args:
        filename (str): The filename to normalize
        
    Returns:
        str: Normalized key
    """
    # Remove file extension
    name_without_ext = os.path.splitext(filename)[0]
    
    # Replace spaces with underscores
    normalized = name_without_ext.replace(' ', '_')
    
    # Remove "icon" suffix (case insensitive)
    normalized = re.sub(r'_icon$', '', normalized, flags=re.IGNORECASE)
    
    # Remove "glyph" suffix (case insensitive)
    normalized = re.sub(r'_glyph$', '', normalized, flags=re.IGNORECASE)
    
    # Remove "line" suffix (case insensitive)
    normalized = re.sub(r'_line$', '', normalized, flags=re.IGNORECASE)
    
    # Remove "color" suffix (case insensitive)
    normalized = re.sub(r'_color$', '', normalized, flags=re.IGNORECASE)

    # Remove "black" suffix (case insensitive)
    normalized = re.sub(r'_black$', '', normalized, flags=re.IGNORECASE)

    # Remove "rep" suffix (case insensitive)
    normalized = re.sub(r'_rep$', '', normalized, flags=re.IGNORECASE)

    # Remove "rep" suffix (case insensitive)
    normalized = re.sub(r'_ns$', '', normalized, flags=re.IGNORECASE)

    # Remove "_1" suffix
    normalized = re.sub(r'_1$', '', normalized)
    
    # Remove "_2" suffix
    normalized = re.sub(r'_2$', '', normalized)
    
    # Remove apostrophes and parentheses
    normalized = normalized.replace("'", "").replace("(", "").replace(")", "")
    
    # Convert to lowercase
    normalized = normalized.lower()
    
    return normalized

def extract_source_from_filename(filename):
    """
    Extract source from filename path prefix.
    Source is the first directory in the path.
    
    Args:
        filename (str): The filename path
        
    Returns:
        str: Source string
    """
    # Split the path by slashes
    path_parts = filename.split('/')
    
    # If there's only one part (no directory), return empty string
    if len(path_parts) <= 1:
        return ""
    
    # Get the first directory (top-level folder)
    source = path_parts[0]
    
    return source

def extract_tags_from_filename(filename):
    """
    Extract tags from filename path.
    Tags are the subfolders below the first subfolder of icons.
    
    Args:
        filename (str): The filename path
        
    Returns:
        list: List of tag strings
    """
    # Split the path by slashes
    path_parts = filename.split('/')
    
    # If there are less than 2 parts, no subfolders to extract
    if len(path_parts) < 2:
        return []
    
    # Get all parts except the first one (source) and the filename
    # This gives us the subfolder structure
    tags = path_parts[1:-1] if len(path_parts) > 2 else []
    
    return tags

def load_existing_icons():
    """
    Load existing icons from icons.json if it exists.
    
    Returns:
        dict: Dictionary mapping filename to icon object for existing icons
    """
    existing_icons = {}
    
    if os.path.exists('icons.json'):
        try:
            with open('icons.json', 'r', encoding='utf-8') as f:
                icons_data = json.load(f)
                
            # Handle both array format and object with icons property
            icons_list = icons_data if isinstance(icons_data, list) else icons_data.get('icons', [])
            
            for icon in icons_list:
                existing_icons[icon['filename']] = icon
                
            print(f"Loaded {len(existing_icons)} existing icons from icons.json")
            
        except Exception as e:
            print(f"Warning: Could not load existing icons.json: {e}")
    
    return existing_icons

def rename_dot_files(icons_dir='icons'):
    """
    Rename all dot files in the icons directory to make them compatible with GitHub Pages.
    This should be done before scanning the directory.
    
    Args:
        icons_dir (str): Path to the icons directory
        
    Returns:
        int: Number of files renamed
    """
    renamed_count = 0
    
    if not os.path.exists(icons_dir):
        print(f"Error: Directory '{icons_dir}' not found.")
        return renamed_count
    
    # Walk through the icons directory recursively
    for root, dirs, files in os.walk(icons_dir):
        for file in files:
            # Only process SVG files
            if not file.lower().endswith('.svg'):
                continue
                
            # Check if the file starts with a dot
            if file.startswith('.'):
                # Get the full path to the original file
                original_path = os.path.join(root, file)
                
                # Create the new filename without the leading dot
                new_file = file[1:]  # Remove the leading dot
                new_path = os.path.join(root, new_file)
                
                # Check if the new filename already exists
                if os.path.exists(new_path):
                    print(f"Warning: Cannot rename '{file}' to '{new_file}' - file already exists")
                    continue
                
                try:
                    # Actually rename the file on disk
                    os.rename(original_path, new_path)
                    print(f"Renamed: '{file}' -> '{new_file}' in {root}")
                    renamed_count += 1
                except Exception as e:
                    print(f"Error renaming file '{file}': {e}")
    
    if renamed_count > 0:
        print(f"Renamed {renamed_count} dot files for GitHub Pages compatibility")
    else:
        print("No dot files found to rename")
    
    return renamed_count

def scan_icons_directory(icons_dir='icons', lookup_table=None):
    """
    Scan the icons directory recursively and return a list of file objects.
    Preserves existing readonly entries from icons.json.
    
    Args:
        icons_dir (str): Path to the icons directory
        lookup_table (dict): Dictionary mapping keys to names
        
    Returns:
        list: List of dictionaries containing file information
    """
    icons = []
    
    # Load existing icons from icons.json
    existing_icons = load_existing_icons()
    
    # Check if icons directory exists
    if not os.path.exists(icons_dir):
        print(f"Error: Directory '{icons_dir}' not found.")
        return icons
    
    # Walk through the icons directory recursively
    for root, dirs, files in os.walk(icons_dir):
        for file in files:
            # Only process SVG files
            if not file.lower().endswith('.svg'):
                continue
                
            # Get the full path of the file
            full_path = os.path.join(root, file)
            
            # Get the relative path from the icons directory
            relative_path = os.path.relpath(full_path, icons_dir)
            
            # Convert Windows backslashes to forward slashes for consistency
            filename = relative_path.replace("\\", "/")
            
            # Skip dot files (they should have been renamed already)
            if file.startswith('.'):
                print(f"Skipping dot file: {filename}")
                continue
            
            # Check if this icon already exists and is readonly
            if filename in existing_icons and existing_icons[filename].get('readonly', False):
                # Use the existing readonly entry
                icons.append(existing_icons[filename])
                print(f"Preserved readonly icon: {filename}")
                continue
            
            # Create normalized key from filename
            key = normalize_filename(file)
            
            # Extract source from filename path
            source = extract_source_from_filename(filename)
            
            # Extract tags from filename path
            tags = extract_tags_from_filename(filename)
            
            # Look up name from the lookup table
            name = lookup_table.get(key, "") if lookup_table else ""
            
            # If no name found, convert key to title case
            if not name:
                name = key.replace('_', ' ').title()
            
            # Create object with filename, key, source, name, and tags
            # Note: readonly is not set here - it defaults to false for new entries
            icon_object = {
                "filename": filename,
                "key": key,
                "source": source,
                "name": name,
                "tags": tags
            }
            
            icons.append(icon_object)
    
    return icons

def main():
    """
    Main function to scan icons and create JSON file.
    """
    print("Scanning icons directory...")
    
    # Load the lookup table
    lookup_table = load_scientific_names()
    
    # Rename dot files first
    rename_dot_files()
    
    # Scan the icons directory
    icons = scan_icons_directory(lookup_table=lookup_table)
    
    if not icons:
        print("No icons found.")
        return
    
    # Count readonly icons
    readonly_count = sum(1 for icon in icons if icon.get('readonly', False))
    new_count = len(icons) - readonly_count
    
    # Sort icons by source first, then by key
    icons.sort(key=lambda x: (x['source'], x['key']))
    
    # Write to JSON file
    try:
        with open('icons.json', 'w', encoding='utf-8') as f:
            json.dump(icons, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully created icons.json")
        print(f"Total icons: {len(icons)}")
        print(f"New icons generated: {new_count}")
        print(f"Readonly icons preserved: {readonly_count}")
        
    except Exception as e:
        print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    main() 