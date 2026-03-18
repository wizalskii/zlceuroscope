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
ZLC.sct          - Main sector file
ZLC.ese          - Extended sector extension (positions)
ZLC.prf          - Default profile settings
ASR/             - Radar display files (19 files)
  ZLC_CTR.asr    - Center radar display
  *_APP.asr      - TRACON radar displays
  *_TWR.asr      - Tower radar displays
Data/            - Source data
  ZLC.json       - Facility data from CRC
Tools/           - Automation scripts
  json_to_sct.py - Generate .sct from JSON
  json_to_ese.py - Generate .ese from JSON
  generate_asr.py - Generate ASR files
  validate.py    - Validate file formats
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

## Requirements

- Euroscope 3.2 or higher
- VATSIM account and client authorization
- Current AIRAC cycle data

## Important Notes

### Navigation Data

The current sector file includes basic airport and airspace structure. For complete functionality, you should supplement with:

- VOR/NDB navigation aids from FAA database
- Fixes and waypoints from navigation database
- Airways (Victor routes and Jet routes)
- SID/STAR procedures from approach plates
- Detailed airspace boundaries

These can be sourced from:
- [vNAS](https://vnas.vatsim.net/) - VATSIM's navigation database
- [FAA NASR](https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/) - Official FAA data
- Existing VATSIM sector files

### File Encoding

All Euroscope files (.sct, .ese, .prf, .asr) use **ANSI/Latin-1 encoding**, not UTF-8. If you edit these files, ensure your editor preserves the correct encoding.

### AIRAC Cycles

Aeronautical data is updated every 28 days. Check for profile updates at the beginning of each AIRAC cycle. See [Docs/updates.md](Docs/updates.md) for update procedures.

## Development

### Generating Files

The profile can be regenerated from the source data:

```bash
# Generate position definitions
python3 Tools/json_to_ese.py

# Generate sector file structure
python3 Tools/json_to_sct.py

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
