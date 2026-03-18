# Changelog

All notable changes to the ZLC Euroscope Profile will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Initial Release Features
- Complete position definitions for ZLC ARTCC
  - 34 center positions
  - 22 TRACON positions across 8 facilities
  - 30 tower positions across 10 facilities
- Basic sector file structure (ZLC.sct)
- Extended sector extension with all positions (ZLC.ese)
- Default profile settings (ZLC.prf)
- 19 radar display files (ASR/)
  - 1 center display
  - 8 TRACON displays
  - 10 tower displays
- Automation tools
  - json_to_sct.py - Sector file generator
  - json_to_ese.py - Position file generator
  - generate_asr.py - ASR file generator
  - validate.py - File format validator
- Documentation
  - Installation guide
  - Position reference
  - Update procedures

### Known Limitations
- Navigation aids (VORs, NDBs) not yet included
- Fixes and waypoints not yet included
- Airways not yet defined
- SID/STAR procedures not yet included
- Airspace boundaries need refinement
- Geographic features limited

### Planned Improvements
- Add complete navigation database
- Add airways from FAA database
- Add SID/STAR procedures
- Define detailed sector boundaries
- Add geographic features
- Implement AIRAC cycle automation

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
