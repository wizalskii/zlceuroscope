#!/usr/bin/env python3
"""
Generate ZLC.sct (Sector File) from ZLC.json
"""

import json
import sys
from pathlib import Path


def generate_sct_file(json_data, output_path):
    """Generate ZLC.sct file"""

    facility = json_data.get('facility', {})
    facility_id = facility.get('id', 'ZLC')
    facility_name = facility.get('name', 'Salt Lake City ARTCC')

    with open(output_path, 'w', encoding='latin-1') as f:
        # Header comments
        f.write("; ZLC ARTCC - Sector File\n")
        f.write("; Salt Lake City Air Route Traffic Control Center\n")
        f.write("; Generated from ZLC.json\n")
        f.write(";\n")
        f.write("; This is a basic sector file structure.\n")
        f.write("; Navigation aids, airways, and detailed geographic data\n")
        f.write("; should be added from FAA or VATSIM sources.\n")
        f.write(";\n\n")

        # [INFO] section
        f.write("[INFO]\n")
        f.write(f"{facility_id}\n")  # ARTCC identifier
        f.write(f"N040.47.23.456\n")  # Default center point (Salt Lake City area)
        f.write(f"W111.58.41.234\n")  # Default center point
        f.write(f"60\n")               # Default magnetic variation
        f.write(f".sct\n")             # File extension
        f.write(f"KSLC\n")             # Default airport
        f.write(f"N\n")                # North/South indicator
        f.write(f"W\n")                # East/West indicator
        f.write("\n")

        # [VOR] section
        f.write("[VOR]\n")
        f.write("; Name:Freq:Lat:Lon\n")
        f.write("; TODO: Add VOR stations from FAA navigation database\n")
        f.write("; Example: SLC 116.800 N040.46.40.000 W111.57.48.000\n")
        f.write("\n")

        # [NDB] section
        f.write("[NDB]\n")
        f.write("; Name:Freq:Lat:Lon\n")
        f.write("; TODO: Add NDB stations from FAA navigation database\n")
        f.write("\n")

        # [FIXES] section
        f.write("[FIXES]\n")
        f.write("; Name:Lat:Lon\n")
        f.write("; TODO: Add navigation fixes from FAA database\n")
        f.write("; These are critical for airways and procedures\n")
        f.write("\n")

        # [AIRPORT] section
        f.write("[AIRPORT]\n")
        f.write("; ICAO:Freq:Lat:Lon:Name\n")
        f.write("; Major airports in ZLC airspace\n")
        f.write("KSLC 119.400 N040.47.14.000 W111.58.44.000 Salt Lake City Intl\n")
        f.write("KBOI 118.300 N043.33.49.000 W116.13.23.000 Boise Air Terminal\n")
        f.write("KJAC 118.075 N043.36.20.000 W110.44.16.000 Jackson Hole\n")
        f.write("KIDA 118.300 N043.30.51.000 W112.04.10.000 Idaho Falls Regional\n")
        f.write("KBIL 119.500 N045.48.22.000 W108.32.34.000 Billings Logan Intl\n")
        f.write("KMSO 125.300 N046.54.57.000 W114.05.28.000 Missoula Intl\n")
        f.write("KHLN 126.200 N046.36.28.000 W111.59.02.000 Helena Regional\n")
        f.write("KGTF 132.650 N047.28.55.000 W111.22.17.000 Great Falls Intl\n")
        f.write("KOGD 127.800 N041.11.45.000 W112.00.43.000 Ogden-Hinckley\n")
        f.write("KPVU 119.200 N040.13.16.000 W111.43.23.000 Provo Municipal\n")
        f.write("KSUN 125.400 N043.30.16.000 W114.17.50.000 Friedman Memorial\n")
        f.write("KPIH 124.175 N042.54.37.000 W112.35.43.000 Pocatello Regional\n")
        f.write("KTWF 119.500 N042.28.56.000 W114.29.16.000 Twin Falls\n")
        f.write("\n")

        # [RUNWAY] section
        f.write("[RUNWAY]\n")
        f.write("; RwyNum:Heading:Lat1:Lon1:Lat2:Lon2:Airport\n")
        f.write("; TODO: Add runway definitions for all airports\n")
        f.write("; KSLC major runways\n")
        f.write("16L 160 N040.47.56.000 W111.58.16.000 N040.44.44.000 W111.57.56.000 KSLC\n")
        f.write("16R 160 N040.47.56.000 W111.59.12.000 N040.44.44.000 W111.58.52.000 KSLC\n")
        f.write("34L 340 N040.44.44.000 W111.58.52.000 N040.47.56.000 W111.59.12.000 KSLC\n")
        f.write("34R 340 N040.44.44.000 W111.57.56.000 N040.47.56.000 W111.58.16.000 KSLC\n")
        f.write("\n")

        # [LOW AIRWAY] section
        f.write("[LOW AIRWAY]\n")
        f.write("; Name:Start:End\n")
        f.write("; TODO: Add low altitude airways from FAA database\n")
        f.write("; Format: V123 FIX1 FIX2\n")
        f.write("\n")

        # [HIGH AIRWAY] section
        f.write("[HIGH AIRWAY]\n")
        f.write("; Name:Start:End\n")
        f.write("; TODO: Add high altitude airways (Jet routes) from FAA database\n")
        f.write("; Format: J123 FIX1 FIX2\n")
        f.write("\n")

        # [ARTCC] section - Center boundaries
        f.write("[ARTCC]\n")
        f.write("; ZLC ARTCC Boundary\n")
        f.write("; TODO: Add precise boundary coordinates\n")
        f.write("; These define the lateral limits of ZLC airspace\n")
        f.write("\n")

        # [ARTCC HIGH] section
        f.write("[ARTCC HIGH]\n")
        f.write("; ZLC High Altitude Boundary\n")
        f.write("; TODO: Add high altitude sector boundaries\n")
        f.write("\n")

        # [ARTCC LOW] section
        f.write("[ARTCC LOW]\n")
        f.write("; ZLC Low Altitude Boundary\n")
        f.write("; TODO: Add low altitude sector boundaries\n")
        f.write("\n")

        # [SID] section
        f.write("[SID]\n")
        f.write("; Standard Instrument Departures\n")
        f.write("; TODO: Add SID routes from approach plates\n")
        f.write("; Format: SIDNAME FIX1 FIX2\n")
        f.write("\n")

        # [STAR] section
        f.write("[STAR]\n")
        f.write("; Standard Terminal Arrival Routes\n")
        f.write("; TODO: Add STAR routes from approach plates\n")
        f.write("; Format: STARNAME FIX1 FIX2\n")
        f.write("\n")

        # [GEO] section
        f.write("[GEO]\n")
        f.write("; Geographic features and visual references\n")
        f.write("; State boundaries, coastlines, etc.\n")
        f.write("; TODO: Add geographic features\n")
        f.write("\n")

        # [REGIONS] section
        f.write("[REGIONS]\n")
        f.write("; Defined airspace regions\n")
        f.write("; TODO: Add TRACON and Tower airspace boundaries\n")
        f.write("\n")

    print(f"Generated {output_path}")
    print("Note: This is a basic structure. Navigation data (VORs, NDBs, fixes, airways)")
    print("      must be added from FAA or VATSIM sources for full functionality.")


def main():
    # Path setup
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    json_path = repo_root / 'Data' / 'ZLC.json'
    output_path = repo_root / 'ZLC.sct'

    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Generate SCT file
    generate_sct_file(data, output_path)


if __name__ == '__main__':
    main()
