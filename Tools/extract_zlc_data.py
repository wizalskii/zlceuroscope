#!/usr/bin/env python3
"""
Extract ZLC-relevant AIRAC data from FE-BUDDY output files
Filters navigation data to ZLC airspace boundaries
"""

import re
from pathlib import Path


# ZLC airspace approximate boundaries (with buffer for transitional areas)
ZLC_BOUNDS = {
    'north': 49.5,   # Canadian border + buffer
    'south': 36.0,   # Southern Utah/Nevada - buffer
    'east': -103.0,  # Eastern Wyoming/Montana + buffer
    'west': -118.0   # Western Idaho/Nevada - buffer
}


def parse_coordinate(coord_str):
    """
    Parse coordinate string to decimal degrees
    Format: N040.47.23.456 or W111.58.41.234
    Returns: float (positive for N/E, negative for S/W)
    """
    coord_str = coord_str.strip()

    # Direction (N/S/E/W)
    direction = coord_str[0]
    coord_str = coord_str[1:]

    # Split by periods
    parts = coord_str.split('.')
    if len(parts) < 3:
        return None

    try:
        degrees = int(parts[0])
        minutes = int(parts[1])
        seconds = float(f"{parts[2]}.{parts[3]}" if len(parts) > 3 else parts[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        # Apply direction
        if direction in ['S', 'W']:
            decimal = -decimal

        return decimal
    except (ValueError, IndexError):
        return None


def is_in_zlc_bounds(lat, lon, buffer=2.0):
    """Check if coordinates are within ZLC bounds (with buffer in degrees)"""
    if lat is None or lon is None:
        return False

    return (ZLC_BOUNDS['south'] - buffer <= lat <= ZLC_BOUNDS['north'] + buffer and
            ZLC_BOUNDS['west'] - buffer <= lon <= ZLC_BOUNDS['east'] + buffer)


def extract_vors(input_file, output_file):
    """Extract VORs within ZLC airspace"""
    count = 0
    with open(input_file, 'r', encoding='utf-8') as inf:
        with open(output_file, 'w', encoding='latin-1') as outf:
            for line in inf:
                if line.startswith('[VOR]') or line.strip() == '':
                    outf.write(line)
                    continue

                # Parse VOR line: ID FREQ LAT LON ;DESCRIPTION
                parts = line.split(';')[0].strip().split()
                if len(parts) >= 4:
                    lat = parse_coordinate(parts[2])
                    lon = parse_coordinate(parts[3])

                    if is_in_zlc_bounds(lat, lon):
                        outf.write(line)
                        count += 1

    return count


def extract_ndbs(input_file, output_file):
    """Extract NDBs within ZLC airspace"""
    count = 0
    with open(input_file, 'r', encoding='utf-8') as inf:
        with open(output_file, 'w', encoding='latin-1') as outf:
            for line in inf:
                if line.startswith('[NDB]') or line.strip() == '':
                    outf.write(line)
                    continue

                # Parse NDB line: ID FREQ LAT LON ;DESCRIPTION
                parts = line.split(';')[0].strip().split()
                if len(parts) >= 4:
                    lat = parse_coordinate(parts[2])
                    lon = parse_coordinate(parts[3])

                    if is_in_zlc_bounds(lat, lon):
                        outf.write(line)
                        count += 1

    return count


def extract_fixes(input_file, output_file):
    """Extract fixes within ZLC airspace"""
    count = 0
    with open(input_file, 'r', encoding='utf-8') as inf:
        with open(output_file, 'w', encoding='latin-1') as outf:
            for line in inf:
                if line.startswith('[FIXES]') or line.strip() == '':
                    outf.write(line)
                    continue

                # Parse FIX line: NAME LAT LON ;DESCRIPTION
                parts = line.split(';')[0].strip().split()
                if len(parts) >= 3:
                    lat = parse_coordinate(parts[1])
                    lon = parse_coordinate(parts[2])

                    if is_in_zlc_bounds(lat, lon, buffer=3.0):  # Larger buffer for fixes
                        outf.write(line)
                        count += 1

    return count


def extract_airports(input_file, output_file):
    """Extract airports within ZLC airspace"""
    count = 0
    with open(input_file, 'r', encoding='utf-8') as inf:
        with open(output_file, 'w', encoding='latin-1') as outf:
            for line in inf:
                if line.startswith('[AIRPORT]') or line.strip() == '':
                    outf.write(line)
                    continue

                # Parse AIRPORT line: ICAO FREQ LAT LON ;NAME
                parts = line.split(';')[0].strip().split()
                if len(parts) >= 4:
                    lat = parse_coordinate(parts[2])
                    lon = parse_coordinate(parts[3])

                    if is_in_zlc_bounds(lat, lon):
                        outf.write(line)
                        count += 1

    return count


def extract_runways(input_file, output_file):
    """Extract runways for ZLC airports"""
    count = 0
    with open(input_file, 'r', encoding='utf-8') as inf:
        with open(output_file, 'w', encoding='latin-1') as outf:
            for line in inf:
                if line.startswith('[RUNWAY]') or line.strip() == '':
                    outf.write(line)
                    continue

                # Parse RUNWAY line: NUM HDG LAT1 LON1 LAT2 LON2 AIRPORT
                parts = line.split(';')[0].strip().split()
                if len(parts) >= 6:
                    lat1 = parse_coordinate(parts[2])
                    lon1 = parse_coordinate(parts[3])
                    lat2 = parse_coordinate(parts[4])
                    lon2 = parse_coordinate(parts[5])

                    # Include if either end is in ZLC
                    if (is_in_zlc_bounds(lat1, lon1) or is_in_zlc_bounds(lat2, lon2)):
                        outf.write(line)
                        count += 1

    return count


def extract_airways(input_file, output_file, airway_type='LOW'):
    """Extract airways that pass through ZLC airspace"""
    count = 0
    current_airway = None
    airway_segments = []

    with open(input_file, 'r', encoding='utf-8') as inf:
        for line in inf:
            if line.startswith(f'[{airway_type} AIRWAY]'):
                continue

            if line.strip() == '':
                continue

            # Parse AIRWAY line: NAME LAT1 LON1 LAT2 LON2 ;START END
            parts = line.split(';')[0].strip().split()
            if len(parts) >= 5:
                airway_name = parts[0]
                lat1 = parse_coordinate(parts[1])
                lon1 = parse_coordinate(parts[2])
                lat2 = parse_coordinate(parts[3])
                lon2 = parse_coordinate(parts[4])

                # Include if either endpoint is in ZLC (larger buffer for airways)
                if (is_in_zlc_bounds(lat1, lon1, buffer=4.0) or
                    is_in_zlc_bounds(lat2, lon2, buffer=4.0)):
                    airway_segments.append(line)
                    count += 1

    # Write all segments
    with open(output_file, 'w', encoding='latin-1') as outf:
        outf.write(f'[{airway_type} AIRWAY]\n')
        for segment in airway_segments:
            outf.write(segment)

    return count


def extract_procedures(input_dir, output_dir, proc_type='SID'):
    """Extract SID/STAR procedures for ZLC airports"""
    input_path = Path(input_dir) / f'[{proc_type}]'
    output_path = Path(output_dir) / proc_type
    output_path.mkdir(exist_ok=True)

    # Read the combined file
    combined_file = input_path / f'000_All_{proc_type if proc_type == "SID" else "STAR"}_Combined.sct2'
    if not combined_file.exists():
        combined_file = input_path / f'000_All_{"DP" if proc_type == "SID" else "STAR"}_Combined.sct2'

    if not combined_file.exists():
        print(f"  Warning: Combined {proc_type} file not found")
        return 0

    count = 0
    zlc_procedures = []

    with open(combined_file, 'r', encoding='utf-8') as inf:
        current_proc = []
        for line in inf:
            if line.startswith('['):
                if current_proc:
                    # Check if procedure has any points in ZLC
                    in_zlc = False
                    for proc_line in current_proc:
                        parts = proc_line.split(';')[0].strip().split()
                        if len(parts) >= 3:
                            lat = parse_coordinate(parts[1])
                            lon = parse_coordinate(parts[2])
                            if is_in_zlc_bounds(lat, lon, buffer=2.0):
                                in_zlc = True
                                break

                    if in_zlc:
                        zlc_procedures.extend(current_proc)
                        count += len(current_proc)

                    current_proc = []

                current_proc.append(line)
            else:
                current_proc.append(line)

        # Handle last procedure
        if current_proc:
            in_zlc = False
            for proc_line in current_proc:
                parts = proc_line.split(';')[0].strip().split()
                if len(parts) >= 3:
                    lat = parse_coordinate(parts[1])
                    lon = parse_coordinate(parts[2])
                    if is_in_zlc_bounds(lat, lon, buffer=2.0):
                        in_zlc = True
                        break

            if in_zlc:
                zlc_procedures.extend(current_proc)
                count += len(current_proc)

    # Write ZLC procedures
    output_file = output_path / f'ZLC_{proc_type}_Combined.sct2'
    with open(output_file, 'w', encoding='latin-1') as outf:
        outf.writelines(zlc_procedures)

    return count


def main():
    # Paths
    febuddy_base = Path('Z:/claude/zlceuroscope/febuddyoutput/FE-BUDDY_Output')
    vrc_dir = febuddy_base / 'VRC'
    output_base = Path('Z:/claude/zlceuroscope/AIRAC_Data')

    output_base.mkdir(exist_ok=True)

    print("=" * 60)
    print("Extracting ZLC AIRAC Data from FE-BUDDY Output")
    print("=" * 60)
    print(f"\nZLC Boundaries:")
    print(f"  North: {ZLC_BOUNDS['north']}°")
    print(f"  South: {ZLC_BOUNDS['south']}°")
    print(f"  East: {ZLC_BOUNDS['east']}°")
    print(f"  West: {ZLC_BOUNDS['west']}°")
    print()

    # Extract VORs
    print("Extracting VORs...")
    count = extract_vors(vrc_dir / '[VOR].sct2', output_base / 'ZLC_VOR.sct2')
    print(f"  Found {count} VORs in ZLC airspace")

    # Extract NDBs
    print("Extracting NDBs...")
    count = extract_ndbs(vrc_dir / '[NDB].sct2', output_base / 'ZLC_NDB.sct2')
    print(f"  Found {count} NDBs in ZLC airspace")

    # Extract Fixes
    print("Extracting Fixes...")
    count = extract_fixes(vrc_dir / '[FIXES].sct2', output_base / 'ZLC_FIXES.sct2')
    print(f"  Found {count} Fixes in ZLC airspace")

    # Extract Airports
    print("Extracting Airports...")
    count = extract_airports(vrc_dir / '[AIRPORT].sct2', output_base / 'ZLC_AIRPORT.sct2')
    print(f"  Found {count} Airports in ZLC airspace")

    # Extract Runways
    print("Extracting Runways...")
    count = extract_runways(vrc_dir / '[RUNWAY].sct2', output_base / 'ZLC_RUNWAY.sct2')
    print(f"  Found {count} Runways in ZLC airspace")

    # Extract Low Airways
    print("Extracting Low Airways...")
    count = extract_airways(vrc_dir / '[LOW AIRWAY].sct2', output_base / 'ZLC_LOW_AIRWAY.sct2', 'LOW')
    print(f"  Found {count} Low Airway segments in ZLC airspace")

    # Extract High Airways
    print("Extracting High Airways...")
    count = extract_airways(vrc_dir / '[HIGH AIRWAY].sct2', output_base / 'ZLC_HIGH_AIRWAY.sct2', 'HIGH')
    print(f"  Found {count} High Airway segments in ZLC airspace")

    # Extract SIDs
    print("Extracting SIDs...")
    count = extract_procedures(vrc_dir, output_base, 'SID')
    print(f"  Found {count} SID waypoints in ZLC airspace")

    # Extract STARs
    print("Extracting STARs...")
    count = extract_procedures(vrc_dir, output_base, 'STAR')
    print(f"  Found {count} STAR waypoints in ZLC airspace")

    print("\n" + "=" * 60)
    print("Extraction Complete!")
    print(f"Output directory: {output_base}")
    print("=" * 60)


if __name__ == '__main__':
    main()
