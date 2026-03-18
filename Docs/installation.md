# Installation Guide

## Prerequisites

1. **Euroscope 3.2 or higher**
   - Download from [euroscope.hu](https://www.euroscope.hu/)
   - Install and complete initial setup

2. **VATSIM Account**
   - Register at [vatsim.net](https://www.vatsim.net/)
   - Complete required controller training for your rating

3. **Current AIRAC Data**
   - Ensure you have current navigation data
   - Download from [vNAS](https://vnas.vatsim.net/) if needed

## Installation Steps

### Option 1: Release Download (Recommended)

1. **Download the latest release**
   - Go to [Releases](https://github.com/wizalskii/zlceuroscope/releases)
   - Download the latest `zlc-euroscope-vX.X.X.zip`

2. **Extract files**
   - Extract the ZIP file to a temporary location
   - Locate your Euroscope directory (usually `C:\Program Files\EuroScope`)

3. **Copy files**
   ```
   Copy to your Euroscope directory:
   - ZLC.sct
   - ZLC.ese
   - ZLC.prf
   - ASR/ folder (all contents)
   ```

4. **Verify installation**
   - Open Euroscope
   - Go to `Open SCT` and select `ZLC.sct`
   - If it loads without errors, installation was successful

### Option 2: Clone Repository

1. **Clone the repository**
   ```bash
   cd /path/to/euroscope/directory
   git clone https://github.com/wizalskii/zlceuroscope.git
   cd zlceuroscope
   ```

2. **Copy files to Euroscope directory**
   ```bash
   # On Windows
   copy ZLC.sct ..\
   copy ZLC.ese ..\
   copy ZLC.prf ..\
   xcopy /E ASR ..\ASR\
   ```

3. **Verify installation**
   - Open Euroscope
   - Load ZLC.sct

## First Time Setup

### 1. Load the Profile

1. Open Euroscope
2. Click `Open SCT`
3. Navigate to and select `ZLC.sct`
4. The sector file should load successfully

### 2. Set Your Position

1. Click `Other SET` → `Controller Info`
2. Enter your details:
   - **Callsign**: Choose from the position list (see [positions.md](positions.md))
   - **Real Name**: Your full name
   - **Certificate**: Your VATSIM rating
   - **Frequency**: The frequency for your chosen position

### 3. Load Radar Display

1. Right-click on the radar screen
2. Select `Open ASR`
3. Navigate to the `ASR/` folder
4. Choose the appropriate display:
   - Center positions: `ZLC_CTR.asr`
   - TRACON positions: `[FACILITY]_APP.asr` (e.g., `S56_APP.asr`)
   - Tower positions: `[AIRPORT]_TWR.asr` (e.g., `SLC_TWR.asr`)

### 4. Save Your Profile

1. Click `Other SET` → `Save Profile`
2. Save as `ZLC_[YourCallsign].prf` (e.g., `ZLC_SLC_04_CTR.prf`)
3. This preserves your personal settings

## Position-Specific Setup

### Center Positions

1. Load `ASR/ZLC_CTR.asr`
2. Adjust zoom to see your entire sector
3. Enable high altitude filters (FL180+)

### TRACON Positions

1. Load the appropriate APP ASR (e.g., `S56_APP.asr`)
2. Adjust range to 40-60 nm
3. Set altitude filter to 0-18000 ft

### Tower Positions

1. Load the appropriate TWR ASR (e.g., `SLC_TWR.asr`)
2. Zoom in to see airport surface
3. Set altitude filter to 0-5000 ft
4. Enable ground radar if available

## Troubleshooting

### Sector File Won't Load

**Problem**: Error message when loading ZLC.sct

**Solutions**:
- Ensure file encoding is ANSI/Latin-1 (not UTF-8)
- Check that all referenced files exist
- Verify Euroscope version is 3.2+

### Missing Positions

**Problem**: Position doesn't appear in list

**Solutions**:
- Verify ZLC.ese is in the same directory as ZLC.sct
- Check that ZLC.ese uses correct encoding (ANSI)
- Ensure frequency format is correct (5 decimal places)

### ASR File Won't Load

**Problem**: Radar display file fails to open

**Solutions**:
- Check that ASR/ folder is in Euroscope directory
- Verify file encoding is ANSI/Latin-1
- Try the default ZLC_CTR.asr first

### Navigation Aids Not Showing

**Problem**: VORs, fixes not displayed

**Solutions**:
- Basic sector file doesn't include full navigation database
- Download and integrate vNAS data
- See [updates.md](updates.md) for adding navigation data

## Network Connection

### Connecting to VATSIM

1. Ensure you have the latest position data
2. Open your profile in Euroscope
3. Set your position and frequency
4. Connect to VATSIM:
   - Click `Connect`
   - Enter VATSIM credentials
   - Select appropriate server
   - Click `Connect`

### Before Your First Session

1. **Review ZLC SOPs**
   - Visit [zlcartcc.org](https://zlcartcc.org/)
   - Read Standard Operating Procedures
   - Familiarize yourself with local procedures

2. **Complete Training**
   - Ensure you have appropriate rating
   - Complete required training
   - Get mentor approval if required

3. **Test Your Setup**
   - Connect to VATSIM Sweatbox for testing
   - Verify all features work correctly
   - Practice with mentor if available

## Updates

To update to a new version:

1. Download the latest release
2. Back up your custom settings
3. Replace ZLC.sct, ZLC.ese, and ASR files
4. Reload in Euroscope
5. Restore your custom settings

See [updates.md](updates.md) for AIRAC cycle update procedures.

## Support

For help:
- Check [zlcartcc.org](https://zlcartcc.org/) for facility-specific guidance
- Visit VATSIM forums for Euroscope support
- Submit issues at [GitHub](https://github.com/wizalskii/zlceuroscope/issues)
