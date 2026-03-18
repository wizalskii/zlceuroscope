#!/usr/bin/env python3
"""
Create TRACON boundary regions from video map data for [REGIONS] section
"""

from pathlib import Path
import re


# TRACON identifiers and their approximate center coordinates
TRACONS = {
    'BIL': {'name': 'Billings TRACON', 'lat': 45.8, 'lon': -108.5},
    'BOI': {'name': 'Boise TRACON', 'lat': 43.6, 'lon': -116.2},
    'BZN': {'name': 'Bozeman TRACON', 'lat': 45.8, 'lon': -111.2},
    'GTF': {'name': 'Great Falls TRACON', 'lat': 47.5, 'lon': -111.4},
    'MSO': {'name': 'Missoula TRACON', 'lat': 46.9, 'lon': -114.1},
    'S56': {'name': 'Salt Lake TRACON', 'lat': 40.8, 'lon': -112.0},
    'TWF': {'name': 'Twin Falls TRACON', 'lat': 42.5, 'lon': -114.5},
    'MUO': {'name': 'Mountain Home TRACON', 'lat': 43.0, 'lon': -115.9},
}


def parse_coord(coord_str):
    """Parse Euroscope coordinate to decimal degrees"""
    coord_str = coord_str.strip()
    direction = coord_str[0]
    parts = coord_str[1:].split('.')

    if len(parts) < 3:
        return None

    try:
        degrees = int(parts[0])
        minutes = int(parts[1])
        seconds = float(f"{parts[2]}.{parts[3]}" if len(parts) > 3 else parts[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        if direction in ['S', 'W']:
            decimal = -decimal

        return decimal
    except:
        return None


def find_closest_tracon(lat, lon):
    """Find which TRACON this coordinate is closest to"""
    min_dist = float('inf')
    closest = None

    for tracon_id, info in TRACONS.items():
        dist = ((lat - info['lat'])**2 + (lon - info['lon'])**2)**0.5
        if dist < min_dist:
            min_dist = dist
            closest = tracon_id

    return closest if min_dist < 3.0 else None  # Within ~3 degrees


def create_tracon_regions(input_file, output_file):
    """Convert TRACON boundaries to REGIONS format"""

    # Read all boundary lines
    tracon_lines = {key: [] for key in TRACONS.keys()}

    with open(input_file, 'r', encoding='latin-1') as f:
        for line in f:
            if line.startswith('[GEO]') or line.startswith(';') or not line.strip():
                continue

            # Parse line: LAT1 LON1 LAT2 LON2 VIDEO-MAP
            parts = line.strip().split()
            if len(parts) >= 4:
                lat1_str, lon1_str, lat2_str, lon2_str = parts[0:4]

                lat1 = parse_coord(lat1_str)
                lon1 = parse_coord(lon1_str)
                lat2 = parse_coord(lat2_str)
                lon2 = parse_coord(lon2_str)

                if lat1 and lon1:
                    # Determine which TRACON this belongs to
                    tracon = find_closest_tracon(lat1, lon1)
                    if tracon:
                        tracon_lines[tracon].append((lat1_str, lon1_str, lat2_str, lon2_str))

    # Write ARTCC LOW format (selectable boundaries)
    with open(output_file, 'w', encoding='latin-1') as out:
        out.write("[ARTCC LOW]\n")
        out.write("; TRACON Boundaries - Selectable\n")
        out.write(";\n")

        for tracon_id in sorted(TRACONS.keys()):
            if tracon_lines[tracon_id]:
                out.write(f";\n; {TRACONS[tracon_id]['name']} ({tracon_id})\n;\n")

                for lat1, lon1, lat2, lon2 in tracon_lines[tracon_id]:
                    # Format: NAME Lat1 Lon1 Lat2 Lon2
                    out.write(f"{tracon_id}_TRACON {lat1} {lon1} {lat2} {lon2}\n")

        out.write("\n")

    # Print summary
    print(f"Created TRACON regions:")
    for tracon_id in sorted(TRACONS.keys()):
        if tracon_lines[tracon_id]:
            print(f"  {tracon_id}: {len(tracon_lines[tracon_id])} boundary segments")

    return sum(len(lines) for lines in tracon_lines.values())


def main():
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / 'VideoMaps' / 'ERAM_FILTER_04_APPROACH_CONTROL_BOUNDARIES.txt'
    output_file = repo_root / 'VideoMaps' / 'ZLC_TRACON_Regions.txt'

    print("=" * 60)
    print("Creating TRACON Boundary Regions")
    print("=" * 60)
    print()

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return

    count = create_tracon_regions(input_file, output_file)

    print(f"\nTotal: {count} boundary segments")
    print(f"Output: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
