#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG to PNG Converter Script

This script scans the icons folder for SVG files and creates corresponding
100x100 pixel PNG files if they don't already exist.
"""

import os
import sys
from pathlib import Path
import subprocess
import shutil

def check_rsvg():
    """Check if rsvg-convert is available."""
    if shutil.which('rsvg-convert'):
        return True
    return False

def convert_svg_to_png(svg_path, png_path, size=100):
    """Convert SVG to PNG using rsvg-convert."""
    try:
        # Convert SVG to PNG with transparent background
        # Use --width to scale proportionally, then pad to square
        cmd = [
            'rsvg-convert',
            '--background-color', 'transparent',
            '--width', str(size),
            '--format', 'png',
            '--output', str(png_path),
            str(svg_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Pad to the target size using PIL
        temp_png = png_path.with_suffix('.temp.png')
        png_path.rename(temp_png)
        
        if pad_image_to_square(temp_png, png_path, size):
            temp_png.unlink()  # Remove temporary file
        else:
            # If padding failed, just rename back
            temp_png.rename(png_path)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {svg_path}: {e}")
        return False

def pad_image_to_square(input_path, output_path, size=100):
    """Pad an image to a square canvas using PIL."""
    try:
        from PIL import Image
        
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a new transparent square image
            square_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            
            # Calculate centering position
            x = (size - img.width) // 2
            y = (size - img.height) // 2
            
            # Paste the image centered on the square canvas
            square_img.paste(img, (x, y), img)
            
            # Save the result
            square_img.save(output_path, 'PNG')
        
        return True
    except ImportError:
        print("PIL/Pillow not available for padding")
        return False
    except Exception as e:
        print(f"Error padding image: {e}")
        return False

def scan_and_convert(icons_dir, size=100):
    """Scan icons directory and convert SVG files to PNG."""
    icons_path = Path(icons_dir)
    
    if not icons_path.exists():
        print(f"Error: Icons directory '{icons_dir}' does not exist.")
        return
    
    # Check for rsvg-convert
    if not check_rsvg():
        print("Error: rsvg-convert not found.")
        print("Please install librsvg:")
        print("  macOS: brew install librsvg")
        return
    
    print("Using rsvg-convert for SVG to PNG conversion")
    
    # Find all SVG files
    svg_files = list(icons_path.rglob("*.svg"))
    print(f"Found {len(svg_files)} SVG files")
    
    converted_count = 0
    skipped_count = 0
    error_count = 0
    
    for svg_file in svg_files:
        # Create PNG path with same name but .png extension
        png_file = svg_file.with_suffix('.png')
        
        # Check if PNG already exists
        if png_file.exists():
            skipped_count += 1
            continue
        
        # Create PNG directory if it doesn't exist
        png_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Converting {svg_file.name} to {png_file.name}")
        
        # Convert SVG to PNG
        if convert_svg_to_png(svg_file, png_file, size):
            converted_count += 1
        else:
            error_count += 1
    
    print(f"\nConversion complete:")
    print(f"  Converted: {converted_count}")
    print(f"  Skipped (already exists): {skipped_count}")
    print(f"  Errors: {error_count}")

def main():
    """Main function."""
    icons_dir = "icons"
    size = 100
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        icons_dir = sys.argv[1]
    
    if len(sys.argv) > 2:
        try:
            size = int(sys.argv[2])
        except ValueError:
            print("Error: Size must be an integer")
            return
    
    print(f"Scanning '{icons_dir}' for SVG files...")
    print(f"Creating {size}x{size} pixel PNG files")
    
    scan_and_convert(icons_dir, size)

if __name__ == "__main__":
    main() 