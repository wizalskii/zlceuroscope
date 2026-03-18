# Changelog

All notable changes to the ZLC Euroscope Profile will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Major Features
- **Complete AIRAC Navigation Data** (4.0 MB sector file)
  - 215 VOR stations
  - 26 NDB stations
  - 13,546 navigation fixes
  - 2,554 airports
  - 892 runway definitions
  - 3,695 low altitude airway segments
  - 1,162 high altitude airway segments
- **Sector and Airspace Boundaries**
  - 129 ZLC ARTCC boundary segments
  - ZLC sector boundaries (video maps from CRC)
  - 457 selectable TRACON boundaries (8 facilities)
    - Individual toggle for each TRACON in Euroscope
    - BIL, BOI, BZN, GTF, MSO, MUO, S56, TWF
  - CAB airspace (Class B/C/D)
- **Airport Diagrams**
  - 16 major airports with detailed diagrams
  - Runways, taxiways, and terminal areas
  - Extracted from VRC sector files
- Complete position definitions for ZLC ARTCC (86 total)
  - 34 center positions
  - 22 TRACON positions across 8 facilities
  - 30 tower positions across 10 facilities
- Extended sector extension with all positions (ZLC.ese)
- Default profile settings (ZLC.prf)
- 19 radar display files (ASR/)
  - 1 center display
  - 8 TRACON displays
  - 10 tower displays

### Automation Tools
- json_to_ese.py - Position file generator
- generate_asr.py - ASR file generator
- extract_zlc_data.py - Extract ZLC AIRAC from FE-BUDDY
- convert_geojson_to_geo.py - Convert CRC GeoJSON video maps
- create_tracon_regions.py - Create selectable TRACON boundaries
- extract_vrc_data.py - Extract boundaries and diagrams from VRC
- integrate_airac_data.py - Integrate all data into sector file
- validate.py - File format validator

### Documentation
- Installation guide
- Position reference (86 positions)
- Update procedures
- Complete README

### Known Limitations
- SID/STAR procedures not yet extracted from GeoJSON
- Special use airspace not included
- Geographic features (state lines, terrain) not included
- MVA charts available but not integrated into main sector file

### Planned Improvements
- Extract and add SID/STAR procedures
- Define detailed sector boundaries from facility documentation
- Add TRACON airspace definitions
- Add special use airspace
- Add geographic features
- Implement automated AIRAC cycle updates

## Version History

### [0.1.0] - 2026-03-18

Initial development version

- Created repository structure
- Generated position definitions from ZLC.json
- Created basic sector file framework
- Generated radar display files
- Added automation scripts
- Created documentation

---

For upcoming releases and AIRAC cycle updates, check the [Releases](https://github.com/wizalskii/zlceuroscope/releases) page.
