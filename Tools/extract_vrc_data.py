#!/usr/bin/env python3
"""
Extract ZLC boundaries and airport diagrams from PilotEdge VRC sector file
"""

from pathlib import Path
import re


# ZLC airports to extract diagrams for
ZLC_AIRPORTS = [
    'KSLC', 'KBOI', 'KJAC', 'KIDA', 'KMSO', 'KBIL', 'KHLN', 'KGTF',
    'KOGD', 'KPVU', 'KHIF', 'KPIH', 'KTWF', 'KSUN', 'KGPI', 'KBZN'
]


def extract_artcc_boundaries(input_file, output_file):
    """Extract ZLC ARTCC boundaries from [ARTCC] section"""

    in_artcc_section = False
    zlc_boundaries = []

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('[ARTCC]'):
                in_artcc_section = True
                continue
            elif line.startswith('[ARTCC LOW]') or line.startswith('[ARTCC HIGH]'):
                in_artcc_section = False
                break

            if in_artcc_section and ';ZLC' in line:
                zlc_boundaries.append(line)

    # Write boundaries
    with open(output_file, 'w', encoding='latin-1') as f:
        f.write("[ARTCC]\n")
        f.write("; ZLC ARTCC Boundary\n")
        for boundary in zlc_boundaries:
            f.write(boundary)
        f.write("\n")

    return len(zlc_boundaries)


def extract_airport_diagrams(input_file, output_file, airports):
    """Extract airport diagrams (GEO sections) for ZLC airports"""

    current_airport = None
    in_geo = False
    airport_diagrams = {}
    current_lines = []

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Check for airport marker comment
            if line.strip().startswith(';K'):
                airport_code = line.strip().replace(';', '').strip()
                if airport_code in airports:
                    current_airport = airport_code
                    continue

            # Check for GEO section start
            if line.startswith('[GEO]'):
                in_geo = True
                if current_airport:
                    current_lines = []
                continue

            # Check for next section (end of GEO)
            if line.startswith('[') and not line.startswith('[GEO]'):
                if current_airport and current_lines:
                    airport_diagrams[current_airport] = current_lines.copy()
                in_geo = False
                current_airport = None
                current_lines = []
                continue

            # Collect GEO lines for current airport
            if in_geo and current_airport and line.strip():
                current_lines.append(line)

    # Write airport diagrams
    with open(output_file, 'w', encoding='latin-1') as f:
        f.write("[GEO]\n")
        f.write("; ZLC Airport Diagrams\n")
        f.write(";\n")

        for airport in sorted(airport_diagrams.keys()):
            f.write(f";\n")
            f.write(f"; {airport} Airport Diagram\n")
            f.write(f";\n")
            for line in airport_diagrams[airport]:
                f.write(line)

        f.write("\n")

    return len(airport_diagrams)


def extract_regions(input_file, output_file):
    """Extract REGIONS section for airspace boundaries"""

    in_regions = False
    zlc_regions = []

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith('[REGIONS]'):
                in_regions = True
                continue
            elif line.startswith('[') and in_regions:
                break

            if in_regions and line.strip():
                # Include lines that might be ZLC-related
                if 'ZLC' in line or any(apt in line for apt in ZLC_AIRPORTS):
                    zlc_regions.append(line)

    if zlc_regions:
        with open(output_file, 'w', encoding='latin-1') as f:
            f.write("[REGIONS]\n")
            f.write("; ZLC Airspace Regions\n")
            for line in zlc_regions:
                f.write(line)
            f.write("\n")

    return len(zlc_regions)


def main():
    vrc_file = Path("C:/Users/danie/Documents/VRC/PilotEdge_WUS_Sector.sct2")
    output_dir = Path("Z:/claude/zlceuroscope/VRC_Data")

    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Extracting ZLC Data from PilotEdge VRC Sector File")
    print("=" * 60)
    print()

    if not vrc_file.exists():
        print(f"Error: {vrc_file} not found")
        return

    # Extract ARTCC boundaries
    print("Extracting ZLC ARTCC boundaries...")
    count = extract_artcc_boundaries(vrc_file, output_dir / 'ZLC_ARTCC_Boundaries.txt')
    print(f"  Found {count} boundary segments")

    # Extract airport diagrams
    print("\nExtracting airport diagrams...")
    count = extract_airport_diagrams(vrc_file, output_dir / 'ZLC_Airport_Diagrams.txt', ZLC_AIRPORTS)
    print(f"  Found diagrams for {count} airports:")
    print(f"    {', '.join(sorted([apt for apt in ZLC_AIRPORTS if count > 0]))}")

    # Extract regions
    print("\nExtracting airspace regions...")
    count = extract_regions(vrc_file, output_dir / 'ZLC_Regions.txt')
    print(f"  Found {count} region definitions")

    print("\n" + "=" * 60)
    print(f"Extraction complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
