# Wildlife Icons Repository

A searchable repository of wildlife icons.

## Features

- Search icons by name or keywords
- Filter by source (SMART, EarthRanger, Aerial, etc)
- Download selected icons as ZIP files

## Project Structure

- `icons/` - Contains all icon files organized by source
- `icons.json` - Metadata file containing icon information
- `import_icons.py` - Script to automatically generate icons.json from the icons directory
- `scientific_names.txt` - Lookup table for scientific names to common names

## Adding New Icons

### Automatic Method (Recommended)

1. Add your icon files to the appropriate subdirectory in the `icons/` folder
2. Run the import script:
   ```bash
   python import_icons.py
   ```
3. The script will automatically generate entries in `icons.json` for all new icons

**Note**: Files that start with a dot (`.`) will be automatically renamed by removing the leading dot to ensure compatibility with GitHub Pages.

### Manual Method

1. Add your icon file to the `icons` directory
2. Manually update the `icons.json` file with the icon's metadata:
   ```json
   {
       "filename": "path/to/icon.svg",
       "key": "normalized_key",
       "source": "SMART",
       "name": "Icon Name",
       "tags": ["tag1", "tag2"]
   }
   ```

## Readonly Property

The `readonly` property allows you to preserve manually edited icon entries when running the import script.

### How it works:

- **`readonly: true`** - The import script will preserve this entry exactly as it is, even if the file changes
- **`readonly: false` or not specified** - The import script will regenerate this entry based on the current file

### Usage:

1. Run the import script to generate initial entries
2. Manually edit specific entries in `icons.json` (e.g., improve names, add custom tags)
3. Add `"readonly": true` to entries you want to preserve:
   ```json
   {
       "filename": "SMART/color/elephant.svg",
       "key": "elephant",
       "source": "SMART",
       "name": "Custom Name",
       "tags": ["color", "custom_tag"],
       "readonly": true
   }
   ```
4. Run the import script again - readonly entries will be preserved, others will be regenerated

## Development

This is a static website that can be served directly from GitHub Pages. No build process is required.

### Local Development

1. Clone the repository
2. Run a local web server:
   ```bash
   python -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser

## Acknowledgements

This repository includes icons from several conservation technology platforms and organizations:

- **[SMART](https://smartconservationtools.org)** - Spatial Monitoring and Reporting Tool for conservation management
- **[EarthRanger](https://www.earthranger.com/)** - Real-time conservation software for protected area management
- **[WCS](https://wcs.org)** - Wildlife Conservation Society

We thank these organizations for their contributions to conservation technology and for making their icon libraries available to the broader conservation community.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
