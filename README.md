# ZLC ARTCC Euroscope Profile

Euroscope profile for Salt Lake City Air Route Traffic Control Center (ZLC ARTCC) on VATSIM.

## Overview

This profile provides comprehensive controller position definitions and radar displays for all ZLC ARTCC facilities:

- **Center**: 34 en route positions (ZLC sectors)
- **TRACON**: 8 approach control facilities (22 positions)
- **Tower**: 10 tower facilities (30 positions)

**Total: 86 controller positions**

## Facilities Included

### Center (ZLC)
Salt Lake City Air Route Traffic Control Center - 34 high altitude sectors

### TRACON Facilities
- **S56** - Salt Lake TRACON
- **BIL** - Billings TRACON
- **BOI** - Boise TRACON
- **BZN** - Bozeman TRACON
- **GTF** - Great Falls TRACON
- **TWF** - Twin Falls TRACON
- **MUO** - Mountain Home TRACON
- **MSO** - Missoula TRACON

### Tower Facilities
- **KSLC** - Salt Lake City International
- **KOGD** - Ogden-Hinckley
- **KPVU** - Provo Municipal
- **KHIF** - Hill Air Force Base
- **KHLN** - Helena Regional
- **KIDA** - Idaho Falls Regional
- **KJAC** - Jackson Hole
- **KPIH** - Pocatello Regional
- **KSUN** - Friedman Memorial (Sun Valley)
- **KGPI** - Glacier Park International (Kalispell)

## Installation

1. Download the latest release from the [Releases](https://github.com/wizalskii/zlceuroscope/releases) page
2. Extract all files to your Euroscope directory
3. Open Euroscope and load the `ZLC.prf` profile
4. Select your desired position from the Controller menu

For detailed installation instructions, see [Docs/installation.md](Docs/installation.md)

## File Structure

```
ZLC.sct          - Main sector file with complete AIRAC data (4.0 MB)
  - 215 VORs
  - 26 NDBs
  - 13,546 Fixes
  - 2,554 Airports
  - 892 Runways
  - 3,695 Low Airway segments
  - 1,162 High Airway segments
  - 129 ARTCC boundary segments
  - ZLC Sector boundaries (video maps)
  - 457 TRACON boundary segments (selectable)
    - BIL, BOI, BZN, GTF, MSO, MUO, S56, TWF
  - CAB airspace
  - Airport diagrams (16 airports)
ZLC.ese          - Extended sector extension (86 positions)
ZLC.prf          - Default profile settings
ASR/             - Radar display files (19 files)
  ZLC_CTR.asr    - Center radar display
  *_APP.asr      - TRACON radar displays
  *_TWR.asr      - Tower radar displays
AIRAC_Data/      - Extracted ZLC-specific AIRAC data
VideoMaps/       - Converted video maps from CRC GeoJSON
  - Sector boundaries
  - TRACON boundaries
  - CAB airspace
  - MVA charts
  - Airport procedures
VRC_Data/        - Extracted data from VRC sector files
  - ARTCC boundaries
  - Airport diagrams
Data/            - Source data
  ZLC.json       - Facility data from CRC
Tools/           - Automation scripts
  json_to_sct.py           - Generate .sct from JSON
  json_to_ese.py           - Generate .ese from JSON
  generate_asr.py          - Generate ASR files
  extract_zlc_data.py      - Extract AIRAC data from FE-BUDDY
  convert_geojson_to_geo.py - Convert CRC GeoJSON to Euroscope
  extract_vrc_data.py      - Extract data from VRC files
  integrate_airac_data.py  - Integrate all data into .sct
  validate.py              - Validate file formats
```

## Usage

### Selecting a Position

1. Open Euroscope
2. Load the ZLC.prf profile
3. Go to Other SET > Controller Info
4. Enter your callsign (e.g., SLC_04_CTR, BIL_APP, KSLC_TWR)
5. Enter the corresponding frequency

### Position Reference

See [Docs/positions.md](Docs/positions.md) for a complete list of all positions with callsigns and frequencies.

### Displaying Boundaries

In Euroscope, you can toggle different boundary types:

1. **ARTCC Boundary**: Go to Setup > Sector File > ARTCC
2. **TRACON Boundaries**: Go to Setup > Sector File > ARTCC Low
   - Each TRACON can be toggled individually:
   - BIL_TRACON, BOI_TRACON, BZN_TRACON, GTF_TRACON
   - MSO_TRACON, MUO_TRACON, S56_TRACON, TWF_TRACON
3. **Sector Boundaries**: Displayed in the main radar view as video maps

## Requirements

- Euroscope 3.2 or higher
- VATSIM account and client authorization
- Current AIRAC cycle data

## Important Notes

### Navigation Data

The sector file now includes **complete AIRAC navigation data** extracted from FE-BUDDY:

✅ **Included:**
- 215 VOR stations
- 26 NDB stations
- 13,546 navigation fixes
- 2,554 airports
- 892 runway definitions
- 3,695 low altitude airway segments (Victor routes)
- 1,162 high altitude airway segments (Jet routes)

⚠️ **Not Yet Included:**
- SID/STAR procedures (planned for future release)
- Detailed ARTCC sector boundaries
- TRACON airspace boundaries
- Special use airspace
- Geographic features (state lines, terrain)

The AIRAC data is extracted and filtered specifically for ZLC airspace boundaries.

### File Encoding

All Euroscope files (.sct, .ese, .prf, .asr) use **ANSI/Latin-1 encoding**, not UTF-8. If you edit these files, ensure your editor preserves the correct encoding.

### AIRAC Cycles

Aeronautical data is updated every 28 days. Check for profile updates at the beginning of each AIRAC cycle. See [Docs/updates.md](Docs/updates.md) for update procedures.

## Development

### Generating Files

The profile can be regenerated from the source data:

```bash
# Extract ZLC-specific AIRAC data from FE-BUDDY output
python3 Tools/extract_zlc_data.py

# Integrate AIRAC data into sector file
python3 Tools/integrate_airac_data.py

# Generate position definitions
python3 Tools/json_to_ese.py

# Generate radar display files
python3 Tools/generate_asr.py

# Validate all files
python3 Tools/validate.py
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation: `python3 Tools/validate.py`
5. Submit a pull request

## Resources

- [ZLC ARTCC Website](https://zlcartcc.org/)
- [VATSIM](https://www.vatsim.net/)
- [Euroscope](https://www.euroscope.hu/)
- [vNAS Navigation Data](https://vnas.vatsim.net/)

## License

See [LICENSE](LICENSE) file for details.

## Credits

Generated from ZLC facility data. For use on the VATSIM network.

Built with Claude Code.
