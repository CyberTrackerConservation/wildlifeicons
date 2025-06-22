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
from pathlib import Path

def normalize_filename(filename):
    """
    Normalize filename to create a key:
    - Remove file extension
    - Replace spaces with underscores
    - Remove "icon" suffix (case insensitive)
    - Remove "glyph" suffix (case insensitive)
    - Remove "line" suffix (case insensitive)
    - Remove "color" suffix (case insensitive)
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

def scan_icons_directory(icons_dir='icons'):
    """
    Scan the icons directory recursively and return a list of file objects.
    
    Args:
        icons_dir (str): Path to the icons directory
        
    Returns:
        list: List of dictionaries containing file information
    """
    icons = []
    
    # Check if icons directory exists
    if not os.path.exists(icons_dir):
        print(f"Error: Directory '{icons_dir}' not found.")
        return icons
    
    # Walk through the icons directory recursively
    for root, dirs, files in os.walk(icons_dir):
        for file in files:
            # Get the full path of the file
            full_path = os.path.join(root, file)
            
            # Get the relative path from the icons directory
            relative_path = os.path.relpath(full_path, icons_dir)
            
            # Convert Windows backslashes to forward slashes for consistency
            filename = relative_path.replace("\\", "/")
            
            # Create normalized key from filename
            key = normalize_filename(file)
            
            # Extract source from filename path
            source = extract_source_from_filename(filename)
            
            # Create object with filename, key, and source
            icon_object = {
                "filename": filename,
                "key": key,
                "source": source
            }
            
            icons.append(icon_object)
    
    return icons

def main():
    """
    Main function to scan icons and create JSON file.
    """
    print("Scanning icons directory...")
    
    # Scan the icons directory
    icons = scan_icons_directory()
    
    if not icons:
        print("No files found in the icons directory.")
        return
    
    # Create the JSON file
    output_file = "scan_icons.json"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(icons, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully created {output_file}")
        print(f"Found {len(icons)} files in the icons directory")
        
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    main() 