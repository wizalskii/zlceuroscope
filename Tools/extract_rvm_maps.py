#!/usr/bin/env python3
"""
Extract Radar Vector Maps (RVM) from CRC GeoJSON files
"""

import json
import glob
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent))
from convert_geojson_to_geo import convert_geojson_to_geo


def main():
    geojson_dir = Path("C:/Users/danie/AppData/Local/CRC/VideoMaps/ZLC")
    output_dir = Path("Z:/claude/zlceuroscope/VideoMaps")

    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Extracting Radar Vector Maps (RVM)")
    print("=" * 60)
    print()

    if not geojson_dir.exists():
        print(f"Error: {geojson_dir} not found")
        return

    # Get all GeoJSON files
    geojson_files = list(geojson_dir.glob("*.geojson"))

    # RVM categories
    rvm_categories = {
        'RVM_STD': [],  # Standard RVMs
        'RVM_ALT': [],  # Alternate RVMs
        'RVM_OTHER': []  # Other RVMs
    }

    # Find all RVM files
    for geojson_file in geojson_files:
        try:
            with open(geojson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                name = data.get('name', '')

                if 'RVM STD' in name:
                    rvm_categories['RVM_STD'].append((geojson_file, name))
                elif 'RVM ALT' in name:
                    rvm_categories['RVM_ALT'].append((geojson_file, name))
                elif 'RVM' in name.upper() or 'VECTOR' in name.upper():
                    rvm_categories['RVM_OTHER'].append((geojson_file, name))
        except:
            pass

    # Convert Standard RVMs
    print("Converting Standard RVMs...")
    std_output = output_dir / "ZLC_RVM_Standard.txt"
    first = True
    for geojson_file, name in sorted(rvm_categories['RVM_STD']):
        print(f"  {name}")
        convert_geojson_to_geo(geojson_file, std_output, append=not first)
        first = False

    # Convert Alternate RVMs
    print("\nConverting Alternate RVMs...")
    alt_output = output_dir / "ZLC_RVM_Alternate.txt"
    first = True
    for geojson_file, name in sorted(rvm_categories['RVM_ALT']):
        print(f"  {name}")
        convert_geojson_to_geo(geojson_file, alt_output, append=not first)
        first = False

    # Convert Other RVMs
    if rvm_categories['RVM_OTHER']:
        print("\nConverting Other RVMs...")
        other_output = output_dir / "ZLC_RVM_Other.txt"
        first = True
        for geojson_file, name in sorted(rvm_categories['RVM_OTHER']):
            print(f"  {name}")
            convert_geojson_to_geo(geojson_file, other_output, append=not first)
            first = False

    print("\n" + "=" * 60)
    print("RVM Extraction Complete!")
    print(f"  Standard RVMs: {len(rvm_categories['RVM_STD'])} files")
    print(f"  Alternate RVMs: {len(rvm_categories['RVM_ALT'])} files")
    print(f"  Other RVMs: {len(rvm_categories['RVM_OTHER'])} files")
    print(f"\nOutput directory: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
