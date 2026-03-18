# Update Procedures

## AIRAC Cycles

Aeronautical information is updated every 28 days according to the AIRAC (Aeronautical Information Regulation And Control) cycle. This profile should be updated at the beginning of each cycle to ensure accuracy.

### AIRAC Schedule

AIRAC cycles run on a fixed international schedule. Check the current cycle at:
- [VATSIM vNAS](https://vnas.vatsim.net/)
- [FAA NASR](https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/)

### When to Update

Update your ZLC Euroscope profile:
1. At the start of each AIRAC cycle (every 28 days)
2. When navigation procedures change (new SIDs/STARs)
3. When airspace changes are published
4. When new positions are added or frequencies change

## Update Methods

### Method 1: Download Latest Release (Recommended)

1. **Check for Updates**
   - Visit [Releases](https://github.com/wizalskii/zlceuroscope/releases)
   - Look for releases tagged with the current AIRAC cycle

2. **Download New Version**
   - Download the latest release ZIP
   - Extract to a temporary folder

3. **Backup Current Settings**
   - Copy your custom .prf files to a safe location
   - Note any custom modifications you've made

4. **Install Update**
   - Replace ZLC.sct, ZLC.ese, and ASR files
   - Keep your custom .prf files
   - Reload in Euroscope

5. **Verify**
   - Load the updated sector file
   - Check that all positions load correctly
   - Verify frequencies are correct

### Method 2: Regenerate from Source

If you have the source data:

1. **Update Source Data**
   ```bash
   # Update ZLC.json from CRC or other source
   cp /path/to/new/ZLC.json Data/ZLC.json
   ```

2. **Regenerate Files**
   ```bash
   # Generate updated position definitions
   python3 Tools/json_to_ese.py

   # Generate updated sector file
   python3 Tools/json_to_sct.py

   # Regenerate ASR files if needed
   python3 Tools/generate_asr.py
   ```

3. **Validate**
   ```bash
   python3 Tools/validate.py
   ```

4. **Test in Euroscope**
   - Load updated files
   - Verify all positions work
   - Check for any errors

### Method 3: Git Pull

If you cloned the repository:

1. **Pull Latest Changes**
   ```bash
   cd zlceuroscope
   git pull origin main
   ```

2. **Copy Updated Files**
   ```bash
   # Copy to your Euroscope directory
   copy ZLC.* ..\
   xcopy /E ASR ..\ASR\
   ```

3. **Reload in Euroscope**

## Adding Navigation Data

The basic profile includes airport and position data but lacks detailed navigation information. To add:

### VORs, NDBs, and Fixes

1. **Download vNAS Data**
   - Visit [vNAS](https://vnas.vatsim.net/)
   - Download the US sector file package
   - Extract navigation data

2. **Extract Navigation Aids**
   - Open the vNAS .sct file
   - Copy [VOR], [NDB], and [FIXES] sections
   - Paste into ZLC.sct

3. **Filter for ZLC Airspace**
   - Remove navigation aids outside ZLC airspace
   - Keep major facilities even if slightly outside
   - Maintain aids used in published procedures

### Airways

1. **Source Airway Data**
   - Use vNAS or FAA database
   - Focus on airways within ZLC airspace

2. **Add to Sector File**
   - Copy [LOW AIRWAY] and [HIGH AIRWAY] sections
   - Ensure all referenced fixes exist in [FIXES]

### SIDs and STARs

1. **Obtain Current Procedures**
   - Download approach plates from FAA
   - Check [FAA d-TPP](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dtpp/)

2. **Add to Sector File**
   - Define procedure routes in [SID] and [STAR] sections
   - Ensure all waypoints exist in [FIXES]
   - Test in Euroscope for accuracy

## Frequency Changes

If controller frequencies change:

1. **Update ZLC.json** (source data)
2. **Regenerate ZLC.ese**
   ```bash
   python3 Tools/json_to_ese.py
   ```
3. **Validate**
   ```bash
   python3 Tools/validate.py
   ```
4. **Test in Euroscope**

## Position Changes

When positions are added, removed, or renamed:

1. **Update source data** (ZLC.json)
2. **Regenerate files**
   ```bash
   python3 Tools/json_to_ese.py
   python3 Tools/json_to_sct.py
   ```
3. **Update ASR files** if new position types added
4. **Update documentation**
   - Regenerate positions.md
   - Update README.md if major changes

## Airspace Boundary Changes

When sector boundaries change:

1. **Obtain new boundary definitions**
   - From ZLC SOPs
   - From official facility documentation

2. **Update ZLC.sct**
   - Modify [ARTCC], [ARTCC HIGH], [ARTCC LOW] sections
   - Update [REGIONS] for TRACON boundaries

3. **Update ASR files**
   - Adjust display ranges if needed
   - Update sector boundary displays

## Testing Updates

After any update:

1. **File Validation**
   ```bash
   python3 Tools/validate.py
   ```

2. **Load in Euroscope**
   - Open ZLC.sct
   - Check for errors in loading

3. **Position Check**
   - Try loading different positions
   - Verify frequencies are correct
   - Check callsigns match

4. **Display Check**
   - Load different ASR files
   - Verify displays are appropriate
   - Check zoom and centering

5. **Network Test (Optional)**
   - Connect to Sweatbox
   - Test actual controller functions
   - Verify all features work

## Rollback Procedure

If an update causes problems:

1. **Close Euroscope**
2. **Restore from Backup**
   - Replace updated files with backup copies
   - Restore previous .sct, .ese, ASR files
3. **Reload Previous Version**
4. **Report Issue**
   - Create issue at [GitHub](https://github.com/wizalskii/zlceuroscope/issues)
   - Include error details and steps to reproduce

## Staying Informed

To stay updated on changes:

1. **Watch the Repository**
   - Click "Watch" on [GitHub](https://github.com/wizalskii/zlceuroscope)
   - Get notifications of new releases

2. **Check ZLC ARTCC**
   - Visit [zlcartcc.org](https://zlcartcc.org/)
   - Review controller bulletin board
   - Check for facility updates

3. **VATSIM Updates**
   - Monitor VATSIM news for network-wide changes
   - Check for Euroscope version updates

## Contributing Updates

If you make improvements:

1. **Fork the Repository**
2. **Make Your Changes**
3. **Test Thoroughly**
   ```bash
   python3 Tools/validate.py
   ```
4. **Submit Pull Request**
   - Describe your changes
   - Include testing results
   - Reference any related issues

## Automation

For facility staff maintaining the profile:

1. **Create Update Script**
   - Automate file generation
   - Schedule for AIRAC cycles
   - Include validation

2. **Version Control**
   - Tag releases with AIRAC cycle
   - Maintain changelog
   - Document changes

3. **Distribution**
   - Create release packages
   - Upload to GitHub releases
   - Notify controllers

## Support

For update-related questions:
- Check [installation.md](installation.md) for basic troubleshooting
- Visit [zlcartcc.org](https://zlcartcc.org/) for facility guidance
- Submit issues at [GitHub](https://github.com/wizalskii/zlceuroscope/issues)
