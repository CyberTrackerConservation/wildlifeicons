#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Icons Script

This script scans the icons directory recursively and creates a JSON file
containing an array of objects with filename information.
"""

import os
import json
from pathlib import Path

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
            
            # Create object with filename
            icon_object = {
                "filename": filename
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