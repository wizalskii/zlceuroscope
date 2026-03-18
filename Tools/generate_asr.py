#!/usr/bin/env python3
"""
Generate ASR (radar display) files for different position types
"""

import json
from pathlib import Path


def generate_center_asr(output_path):
    """Generate center radar display file"""
    with open(output_path, 'w', encoding='latin-1') as f:
        f.write("; ZLC Center Radar Display\n")
        f.write("; High altitude view for center positions\n\n")
        f.write("[DISPLAY]\n")
        f.write("DisplayTypeName:Standard ES radar screen\n")
        f.write("DisplayTypeGeoReferenced:1\n")
        f.write("Free Text:ZLC Center|N040.47.23.456:W111.58.41.234|255:255:255\n")
        f.write("View Cursor:N040.47.23.456:W111.58.41.234\n")
        f.write("Zoom:0.5\n\n")
        f.write("[SYMBOLSIZE]\n")
        f.write("AC Symbol:1\n")
        f.write("AC Symbol Heading:1\n\n")
        f.write("[FILTERS]\n")
        f.write("Altitude Filter:1:0:99999\n")
        f.write("Show All Aircraft:1\n\n")
        f.write("[COLOR DEFINITION]\n")
        f.write("Color_1:255:0:0\n")
        f.write("Color_2:0:255:0\n")
        f.write("Color_3:0:0:255\n")
        f.write("Color_4:255:255:0\n")
        f.write("Color_5:255:0:255\n")
        f.write("Color_6:0:255:255\n")
        f.write("Color_7:192:192:192\n")
        f.write("Color_8:128:128:128\n\n")


def generate_tracon_asr(facility_id, output_path, center_lat="N040.00.00.000", center_lon="W110.00.00.000"):
    """Generate TRACON radar display file"""
    with open(output_path, 'w', encoding='latin-1') as f:
        f.write(f"; {facility_id} TRACON Radar Display\n")
        f.write("; Terminal area view\n\n")
        f.write("[DISPLAY]\n")
        f.write("DisplayTypeName:Standard ES radar screen\n")
        f.write("DisplayTypeGeoReferenced:1\n")
        f.write(f"Free Text:{facility_id} Approach|{center_lat}:{center_lon}|255:255:255\n")
        f.write(f"View Cursor:{center_lat}:{center_lon}\n")
        f.write("Zoom:2.0\n\n")
        f.write("[SYMBOLSIZE]\n")
        f.write("AC Symbol:1\n")
        f.write("AC Symbol Heading:1\n\n")
        f.write("[FILTERS]\n")
        f.write("Altitude Filter:1:0:18000\n")
        f.write("Show All Aircraft:1\n\n")
        f.write("[COLOR DEFINITION]\n")
        f.write("Color_1:255:0:0\n")
        f.write("Color_2:0:255:0\n")
        f.write("Color_3:0:0:255\n")
        f.write("Color_4:255:255:0\n\n")


def generate_tower_asr(airport_id, output_path, center_lat="N040.00.00.000", center_lon="W110.00.00.000"):
    """Generate tower radar display file"""
    with open(output_path, 'w', encoding='latin-1') as f:
        f.write(f"; {airport_id} Tower Radar Display\n")
        f.write("; Airport surface and local area view\n\n")
        f.write("[DISPLAY]\n")
        f.write("DisplayTypeName:Standard ES radar screen\n")
        f.write("DisplayTypeGeoReferenced:1\n")
        f.write(f"Free Text:{airport_id} Tower|{center_lat}:{center_lon}|255:255:255\n")
        f.write(f"View Cursor:{center_lat}:{center_lon}\n")
        f.write("Zoom:5.0\n\n")
        f.write("[SYMBOLSIZE]\n")
        f.write("AC Symbol:1\n")
        f.write("AC Symbol Heading:1\n\n")
        f.write("[FILTERS]\n")
        f.write("Altitude Filter:1:0:5000\n")
        f.write("Show All Aircraft:1\n\n")
        f.write("[COLOR DEFINITION]\n")
        f.write("Color_1:255:0:0\n")
        f.write("Color_2:0:255:0\n")
        f.write("Color_3:0:0:255\n\n")


def main():
    repo_root = Path(__file__).parent.parent
    asr_dir = repo_root / 'ASR'

    # Approximate coordinates for facilities (these should be refined)
    facility_coords = {
        'S56': ('N040.47.14.000', 'W111.58.44.000'),  # Salt Lake TRACON
        'BIL': ('N045.48.22.000', 'W108.32.34.000'),  # Billings
        'BOI': ('N043.33.49.000', 'W116.13.23.000'),  # Boise
        'BZN': ('N045.46.41.000', 'W111.09.09.000'),  # Bozeman
        'GTF': ('N047.28.55.000', 'W111.22.17.000'),  # Great Falls
        'TWF': ('N042.28.56.000', 'W114.29.16.000'),  # Twin Falls
        'MUO': ('N043.24.00.000', 'W112.42.00.000'),  # Mountain Home (approx)
        'MSO': ('N046.54.57.000', 'W114.05.28.000'),  # Missoula
        'KSLC': ('N040.47.14.000', 'W111.58.44.000'), # Salt Lake City
        'KOGD': ('N041.11.45.000', 'W112.00.43.000'), # Ogden
        'KPVU': ('N040.13.16.000', 'W111.43.23.000'), # Provo
        'KHIF': ('N041.07.20.000', 'W112.02.02.000'), # Hill AFB (approx)
        'KHLN': ('N046.36.28.000', 'W111.59.02.000'), # Helena
        'KIDA': ('N043.30.51.000', 'W112.04.10.000'), # Idaho Falls
        'KJAC': ('N043.36.20.000', 'W110.44.16.000'), # Jackson Hole
        'KPIH': ('N042.54.37.000', 'W112.35.43.000'), # Pocatello
        'KSUN': ('N043.30.16.000', 'W114.17.50.000'), # Sun Valley
        'KGPI': ('N048.18.32.000', 'W114.15.22.000'), # Kalispell
    }

    # Generate center ASR
    print("Generating ZLC_CTR.asr...")
    generate_center_asr(asr_dir / 'ZLC_CTR.asr')

    # Generate TRACON ASRs
    tracons = ['S56', 'BIL', 'BOI', 'BZN', 'GTF', 'TWF', 'MUO', 'MSO']
    for tracon in tracons:
        print(f"Generating {tracon}_APP.asr...")
        coords = facility_coords.get(tracon, ('N040.00.00.000', 'W110.00.00.000'))
        generate_tracon_asr(tracon, asr_dir / f'{tracon}_APP.asr', coords[0], coords[1])

    # Generate Tower ASRs
    towers = ['KSLC', 'KOGD', 'KPVU', 'KHIF', 'KHLN', 'KIDA', 'KJAC', 'KPIH', 'KSUN', 'KGPI']
    for tower in towers:
        print(f"Generating {tower[1:]}_TWR.asr...")
        coords = facility_coords.get(tower, ('N040.00.00.000', 'W110.00.00.000'))
        generate_tower_asr(tower[1:], asr_dir / f'{tower[1:]}_TWR.asr', coords[0], coords[1])

    print(f"\nGenerated {1 + len(tracons) + len(towers)} ASR files")


if __name__ == '__main__':
    main()
