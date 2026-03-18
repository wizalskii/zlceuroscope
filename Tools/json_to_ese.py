#!/usr/bin/env python3
"""
Generate ZLC.ese (Extended Sector Extension) file from ZLC.json
"""

import json
import sys
from pathlib import Path


def freq_hz_to_euroscope(freq_hz):
    """Convert frequency from Hz to Euroscope format (5 decimal places)"""
    freq_mhz = freq_hz / 1000000
    return f"{freq_mhz:.5f}"


def extract_positions(json_data):
    """Extract all positions from ZLC.json"""
    positions = []

    # Get main facility (ZLC center)
    facility = json_data.get('facility', {})
    facility_id = facility.get('id', 'ZLC')

    # Extract center positions
    for pos in facility.get('positions', []):
        callsign = pos.get('callsign', '')
        freq_hz = pos.get('frequency', 0)
        name = pos.get('name', '')

        # Parse callsign to get identifier (e.g., SLC_04_CTR -> 04)
        parts = callsign.split('_')
        if len(parts) >= 2:
            identifier = parts[1]
        else:
            identifier = callsign

        positions.append({
            'callsign': callsign,
            'frequency': freq_hz_to_euroscope(freq_hz),
            'identifier': identifier,
            'name': name,
            'facility': facility_id,
            'type': 'CTR'  # Center
        })

    # Extract child facility positions (TRACONs and Towers)
    for child in facility.get('childFacilities', []):
        child_id = child.get('id', '')
        child_type = child.get('type', '')

        for pos in child.get('positions', []):
            callsign = pos.get('callsign', '')
            freq_hz = pos.get('frequency', 0)
            name = pos.get('name', '')

            # Determine position type
            if '_TWR' in callsign or '_GND' in callsign or '_DEL' in callsign:
                pos_type = 'TWR'
            elif '_APP' in callsign or '_DEP' in callsign:
                pos_type = 'APP'
            else:
                pos_type = 'OBS'

            # Parse identifier
            parts = callsign.split('_')
            if len(parts) >= 2:
                identifier = parts[1] if len(parts) > 2 else parts[0]
            else:
                identifier = callsign

            positions.append({
                'callsign': callsign,
                'frequency': freq_hz_to_euroscope(freq_hz),
                'identifier': identifier,
                'name': name,
                'facility': child_id,
                'type': pos_type
            })

    return positions


def generate_ese_file(json_data, output_path):
    """Generate ZLC.ese file"""

    positions = extract_positions(json_data)

    with open(output_path, 'w', encoding='latin-1') as f:
        # Header
        f.write("; ZLC ARTCC - Extended Sector Extension File\n")
        f.write("; Generated from ZLC.json\n")
        f.write("; Salt Lake City Air Route Traffic Control Center\n")
        f.write(";\n\n")

        # [POSITIONS] section
        f.write("[POSITIONS]\n")
        f.write("; Callsign:Frequency:Identifier:MiddleLetter:Prefix:Suffix:NotUsed:StartOfRange:EndOfRange\n")

        for pos in positions:
            # Format: CALLSIGN:FREQ:ID:MIDDLE:PREFIX:SUFFIX:NOTUSED:START:END
            # For now, using basic format - can be enhanced with proper ranges
            line = f"{pos['callsign']}:{pos['frequency']}:{pos['identifier']}:::{pos['facility']}::::\n"
            f.write(line)

        f.write("\n")

        # [AIRSPACE] section
        f.write("[AIRSPACE]\n")
        f.write("; Not yet implemented - requires boundary definitions\n")
        f.write("\n")

        # [OWNER] section
        f.write("[OWNER]\n")
        f.write("; Not yet implemented - requires ownership hierarchy\n")
        f.write("\n")

    print(f"Generated {output_path}")
    print(f"Total positions: {len(positions)}")

    # Print summary by type
    ctr_count = sum(1 for p in positions if p['type'] == 'CTR')
    app_count = sum(1 for p in positions if p['type'] == 'APP')
    twr_count = sum(1 for p in positions if p['type'] == 'TWR')

    print(f"  Center: {ctr_count}")
    print(f"  Approach: {app_count}")
    print(f"  Tower: {twr_count}")


def main():
    # Path setup
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    json_path = repo_root / 'Data' / 'ZLC.json'
    output_path = repo_root / 'ZLC.ese'

    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Generate ESE file
    generate_ese_file(data, output_path)


if __name__ == '__main__':
    main()
