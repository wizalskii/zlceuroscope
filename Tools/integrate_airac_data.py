#!/usr/bin/env python3
"""
Integrate extracted AIRAC data into ZLC.sct file
"""

from pathlib import Path


def read_section(file_path):
    """Read a section file and return lines (skip header)"""
    lines = []
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in f:
            # Skip section headers
            if line.startswith('['):
                continue
            if line.strip():
                lines.append(line)
    return lines


def build_complete_sct():
    """Build complete ZLC.sct with AIRAC data"""

    repo_root = Path(__file__).parent.parent
    airac_dir = repo_root / 'AIRAC_Data'
    output_file = repo_root / 'ZLC.sct'

    print("=" * 60)
    print("Integrating AIRAC Data into ZLC.sct")
    print("=" * 60)

    with open(output_file, 'w', encoding='latin-1') as f:
        # Header
        f.write("; ZLC ARTCC - Sector File\n")
        f.write("; Salt Lake City Air Route Traffic Control Center\n")
        f.write("; Generated with AIRAC data from FE-BUDDY\n")
        f.write(";\n")
        f.write("; AIRAC Cycle: Current\n")
        f.write("; Last Updated: 2026-03-18\n")
        f.write(";\n\n")

        # [INFO] section
        f.write("[INFO]\n")
        f.write("ZLC\n")
        f.write("N040.47.23.456\n")
        f.write("W111.58.41.234\n")
        f.write("60\n")
        f.write(".sct\n")
        f.write("KSLC\n")
        f.write("N\n")
        f.write("W\n")
        f.write("\n")

        # [VOR] section
        print("Adding VORs...")
        f.write("[VOR]\n")
        f.write("; ID:Freq:Lat:Lon:Description\n")
        vor_lines = read_section(airac_dir / 'ZLC_VOR.sct2')
        for line in vor_lines:
            f.write(line)
        print(f"  Added {len(vor_lines)} VORs")
        f.write("\n")

        # [NDB] section
        print("Adding NDBs...")
        f.write("[NDB]\n")
        f.write("; ID:Freq:Lat:Lon:Description\n")
        ndb_lines = read_section(airac_dir / 'ZLC_NDB.sct2')
        for line in ndb_lines:
            f.write(line)
        print(f"  Added {len(ndb_lines)} NDBs")
        f.write("\n")

        # [FIXES] section
        print("Adding Fixes...")
        f.write("[FIXES]\n")
        f.write("; Name:Lat:Lon:Description\n")
        fix_lines = read_section(airac_dir / 'ZLC_FIXES.sct2')
        for line in fix_lines:
            f.write(line)
        print(f"  Added {len(fix_lines)} Fixes")
        f.write("\n")

        # [AIRPORT] section
        print("Adding Airports...")
        f.write("[AIRPORT]\n")
        f.write("; ICAO:Freq:Lat:Lon:Name\n")
        airport_lines = read_section(airac_dir / 'ZLC_AIRPORT.sct2')
        for line in airport_lines:
            f.write(line)
        print(f"  Added {len(airport_lines)} Airports")
        f.write("\n")

        # [RUNWAY] section
        print("Adding Runways...")
        f.write("[RUNWAY]\n")
        f.write("; RwyNum:Heading:Lat1:Lon1:Lat2:Lon2:Airport\n")
        runway_lines = read_section(airac_dir / 'ZLC_RUNWAY.sct2')
        for line in runway_lines:
            f.write(line)
        print(f"  Added {len(runway_lines)} Runways")
        f.write("\n")

        # [LOW AIRWAY] section
        print("Adding Low Airways...")
        f.write("[LOW AIRWAY]\n")
        f.write("; Airway:Start_Lat:Start_Lon:End_Lat:End_Lon:Start_Fix:End_Fix\n")
        low_airway_lines = read_section(airac_dir / 'ZLC_LOW_AIRWAY.sct2')
        for line in low_airway_lines:
            f.write(line)
        print(f"  Added {len(low_airway_lines)} Low Airway segments")
        f.write("\n")

        # [HIGH AIRWAY] section
        print("Adding High Airways...")
        f.write("[HIGH AIRWAY]\n")
        f.write("; Airway:Start_Lat:Start_Lon:End_Lat:End_Lon:Start_Fix:End_Fix\n")
        high_airway_lines = read_section(airac_dir / 'ZLC_HIGH_AIRWAY.sct2')
        for line in high_airway_lines:
            f.write(line)
        print(f"  Added {len(high_airway_lines)} High Airway segments")
        f.write("\n")

        # [ARTCC] section - ZLC Boundary
        f.write("[ARTCC]\n")
        f.write("; ZLC ARTCC Boundary\n")
        print("Adding ARTCC Boundaries...")

        vrc_boundaries = repo_root / 'VRC_Data' / 'ZLC_ARTCC_Boundaries.txt'
        if vrc_boundaries.exists():
            with open(vrc_boundaries, 'r', encoding='latin-1') as vrc:
                for line in vrc:
                    if not line.startswith('[ARTCC]'):  # Skip section header
                        f.write(line)

        f.write("\n")

        # [ARTCC HIGH] section
        f.write("[ARTCC HIGH]\n")
        f.write("; ZLC High Altitude Boundary\n")
        f.write("; TODO: Add high altitude sector boundaries\n")
        f.write("\n")

        # [ARTCC LOW] section - TRACON Boundaries
        f.write("[ARTCC LOW]\n")
        f.write("; ZLC Low Altitude Boundaries\n")
        f.write(";\n")

        # Add TRACON boundaries (selectable)
        video_maps_dir = repo_root / 'VideoMaps'
        tracon_regions = video_maps_dir / 'ZLC_TRACON_Regions.txt'
        if tracon_regions.exists():
            print("Adding TRACON Boundaries (selectable)...")
            with open(tracon_regions, 'r', encoding='latin-1') as tracons:
                for line in tracons:
                    if not line.startswith('[ARTCC LOW]'):  # Skip section header
                        f.write(line)

        f.write("\n")

        # [SID] section
        f.write("[SID]\n")
        f.write("; Standard Instrument Departures\n")
        f.write("; TODO: Add SID routes from extracted procedures\n")
        f.write("\n")

        # [STAR] section
        f.write("[STAR]\n")
        f.write("; Standard Terminal Arrival Routes\n")
        f.write("; TODO: Add STAR routes from extracted procedures\n")
        f.write("\n")

        # [GEO] section - Video Maps
        f.write("[GEO]\n")
        f.write("; Geographic features and Video Maps\n")
        f.write(";\n")

        # Add sector boundaries
        video_maps_dir = repo_root / 'VideoMaps'
        sector_boundaries = video_maps_dir / 'ERAM_FILTER_01_ZLC_SECTOR_BOUNDARIES.txt'
        if sector_boundaries.exists():
            print("Adding ZLC Sector Boundaries...")
            with open(sector_boundaries, 'r', encoding='latin-1') as vmap:
                for line in vmap:
                    if not line.startswith('[GEO]'):  # Skip section header
                        f.write(line)

        # Add TRACON boundaries
        tracon_boundaries = video_maps_dir / 'ERAM_FILTER_04_APPROACH_CONTROL_BOUNDARIES.txt'
        if tracon_boundaries.exists():
            print("Adding TRACON Boundaries...")
            with open(tracon_boundaries, 'r', encoding='latin-1') as vmap:
                for line in vmap:
                    if not line.startswith('[GEO]'):
                        f.write(line)

        # Add CAB airspace
        cab_airspace = video_maps_dir / 'ZLC_CAB_Airspace.txt'
        if cab_airspace.exists():
            print("Adding CAB Airspace...")
            with open(cab_airspace, 'r', encoding='latin-1') as vmap:
                for line in vmap:
                    if not line.startswith('[GEO]'):
                        f.write(line)

        # Add airport diagrams
        airport_diagrams = repo_root / 'VRC_Data' / 'ZLC_Airport_Diagrams.txt'
        if airport_diagrams.exists():
            print("Adding Airport Diagrams...")
            with open(airport_diagrams, 'r', encoding='latin-1') as diagrams:
                for line in diagrams:
                    if not line.startswith('[GEO]'):
                        f.write(line)

        f.write("\n")

        # [REGIONS] section
        f.write("[REGIONS]\n")
        f.write("; Airspace regions\n")
        f.write("; TRACON and special use airspace boundaries\n")
        f.write("\n")

    print("\n" + "=" * 60)
    print(f"Complete! ZLC.sct updated with AIRAC data")
    print(f"Output: {output_file}")
    print("=" * 60)

    # Print file size
    size_mb = output_file.stat().st_size / (1024 * 1024)
    print(f"File size: {size_mb:.2f} MB")


def main():
    build_complete_sct()


if __name__ == '__main__':
    main()
