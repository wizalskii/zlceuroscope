#!/usr/bin/env python3
"""
Convert CRC GeoJSON video maps to Euroscope [GEO] format
"""

import json
import glob
from pathlib import Path


def decimal_to_euroscope_coord(lat, lon):
    """
    Convert decimal degrees to Euroscope format
    Input: lat (float), lon (float)
    Output: "N040.47.23.456" "W111.58.41.234"
    """
    # Latitude
    lat_dir = 'N' if lat >= 0 else 'S'
    lat = abs(lat)
    lat_deg = int(lat)
    lat_min_decimal = (lat - lat_deg) * 60
    lat_min = int(lat_min_decimal)
    lat_sec_decimal = (lat_min_decimal - lat_min) * 60
    lat_sec = int(lat_sec_decimal)
    lat_subsec = int((lat_sec_decimal - lat_sec) * 1000)
    lat_str = f"{lat_dir}{lat_deg:03d}.{lat_min:02d}.{lat_sec:02d}.{lat_subsec:03d}"

    # Longitude
    lon_dir = 'E' if lon >= 0 else 'W'
    lon = abs(lon)
    lon_deg = int(lon)
    lon_min_decimal = (lon - lon_deg) * 60
    lon_min = int(lon_min_decimal)
    lon_sec_decimal = (lon_min_decimal - lon_min) * 60
    lon_sec = int(lon_sec_decimal)
    lon_subsec = int((lon_sec_decimal - lon_sec) * 1000)
    lon_str = f"{lon_dir}{lon_deg:03d}.{lon_min:02d}.{lon_sec:02d}.{lon_subsec:03d}"

    return lat_str, lon_str


def convert_geojson_to_geo(geojson_file, output_file, append=False):
    """
    Convert a single GeoJSON file to Euroscope GEO format
    """
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name = data.get('name', Path(geojson_file).stem)
    features = data.get('features', [])

    mode = 'a' if append else 'w'
    with open(output_file, mode, encoding='latin-1') as out:
        # Write section header if not appending
        if not append:
            out.write("[GEO]\n")

        # Write video map name comment
        out.write(f";\n; {name}\n;\n")

        for feature in features:
            geometry = feature.get('geometry', {})
            properties = feature.get('properties', {})
            geom_type = geometry.get('type')
            coordinates = geometry.get('coordinates', [])

            # Determine color/style from properties
            color = properties.get('color', '#FFFFFF').upper()
            # Map color to style keyword
            style = "VIDEO-MAP"

            if geom_type == 'Polygon':
                # Polygon has one ring (first element is outer ring)
                for ring in coordinates:
                    # Ring is list of [lon, lat] pairs
                    for i in range(len(ring) - 1):
                        lon1, lat1 = ring[i][0], ring[i][1]
                        lon2, lat2 = ring[i + 1][0], ring[i + 1][1]

                        lat1_str, lon1_str = decimal_to_euroscope_coord(lat1, lon1)
                        lat2_str, lon2_str = decimal_to_euroscope_coord(lat2, lon2)

                        out.write(f"{lat1_str} {lon1_str} {lat2_str} {lon2_str} {style}\n")

            elif geom_type == 'MultiPolygon':
                # MultiPolygon has multiple polygons
                for polygon in coordinates:
                    for ring in polygon:
                        for i in range(len(ring) - 1):
                            lon1, lat1 = ring[i][0], ring[i][1]
                            lon2, lat2 = ring[i + 1][0], ring[i + 1][1]

                            lat1_str, lon1_str = decimal_to_euroscope_coord(lat1, lon1)
                            lat2_str, lon2_str = decimal_to_euroscope_coord(lat2, lon2)

                            out.write(f"{lat1_str} {lon1_str} {lat2_str} {lon2_str} {style}\n")

            elif geom_type == 'LineString':
                # LineString is a series of connected points
                for i in range(len(coordinates) - 1):
                    lon1, lat1 = coordinates[i][0], coordinates[i][1]
                    lon2, lat2 = coordinates[i + 1][0], coordinates[i + 1][1]

                    lat1_str, lon1_str = decimal_to_euroscope_coord(lat1, lon1)
                    lat2_str, lon2_str = decimal_to_euroscope_coord(lat2, lon2)

                    out.write(f"{lat1_str} {lon1_str} {lat2_str} {lon2_str} {style}\n")

            elif geom_type == 'MultiLineString':
                # MultiLineString has multiple lines
                for line in coordinates:
                    for i in range(len(line) - 1):
                        lon1, lat1 = line[i][0], line[i][1]
                        lon2, lat2 = line[i + 1][0], line[i + 1][1]

                        lat1_str, lon1_str = decimal_to_euroscope_coord(lat1, lon1)
                        lat2_str, lon2_str = decimal_to_euroscope_coord(lat2, lon2)

                        out.write(f"{lat1_str} {lon1_str} {lat2_str} {lon2_str} {style}\n")


def main():
    geojson_dir = Path("C:/Users/danie/AppData/Local/CRC/VideoMaps/ZLC")
    output_dir = Path("Z:/claude/zlceuroscope/VideoMaps")

    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("Converting CRC GeoJSON Video Maps to Euroscope Format")
    print("=" * 60)
    print()

    if not geojson_dir.exists():
        print(f"Error: {geojson_dir} not found")
        return

    # Get all GeoJSON files
    geojson_files = list(geojson_dir.glob("*.geojson"))
    print(f"Found {len(geojson_files)} GeoJSON files")
    print()

    # Priority files to convert first
    priority_maps = [
        "ERAM_FILTER 01_ZLC SECTOR BOUNDARIES",
        "ERAM_FILTER_04_APPROACH_CONTROL_BOUNDARIES",
        "ERAM_FILTER 02_SECTOR INFO",
    ]

    # Convert priority maps first
    print("Converting priority video maps...")
    for priority in priority_maps:
        for geojson_file in geojson_files:
            with open(geojson_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    name = data.get('name', '')
                    if name == priority:
                        output_file = output_dir / f"{name.replace('/', '_').replace(' ', '_')}.txt"
                        print(f"  {name} -> {output_file.name}")
                        convert_geojson_to_geo(geojson_file, output_file, append=False)
                except Exception as e:
                    print(f"    Error: {e}")

    # Convert CAB (Class B/C/D airspace) maps
    print("\nConverting CAB airspace maps...")
    cab_output = output_dir / "ZLC_CAB_Airspace.txt"
    first = True
    for geojson_file in sorted(geojson_files):
        with open(geojson_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                name = data.get('name', '')
                if 'CAB' in name.upper() or 'Cab' in name:
                    print(f"  {name}")
                    convert_geojson_to_geo(geojson_file, cab_output, append=not first)
                    first = False
            except Exception as e:
                print(f"    Error: {e}")

    # Convert MVA maps
    print("\nConverting MVA (Minimum Vectoring Altitude) maps...")
    mva_output = output_dir / "ZLC_MVA.txt"
    first = True
    for geojson_file in sorted(geojson_files):
        with open(geojson_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                name = data.get('name', '')
                if 'MVA' in name.upper():
                    print(f"  {name}")
                    convert_geojson_to_geo(geojson_file, mva_output, append=not first)
                    first = False
            except Exception as e:
                print(f"    Error: {e}")

    # Convert airport-specific maps (approaches, procedures)
    print("\nConverting airport procedure maps...")
    airports = ['KSLC', 'KBOI', 'KJAC', 'KIDA', 'KMSO', 'KBIL', 'KHLN', 'KGTF',
                'KOGD', 'KPVU', 'KHIF', 'KPIH', 'KTWF', 'KSUN', 'KGPI', 'KBZN']

    for airport in airports:
        airport_code = airport[1:]  # Remove 'K' prefix
        airport_output = output_dir / f"{airport}_Procedures.txt"
        first = True
        count = 0

        for geojson_file in sorted(geojson_files):
            with open(geojson_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    name = data.get('name', '')
                    # Match if airport code is in the name
                    if airport_code in name.upper() or airport in name.upper():
                        if 'SECTOR' not in name.upper() and 'BOUNDARIES' not in name.upper():
                            convert_geojson_to_geo(geojson_file, airport_output, append=not first)
                            first = False
                            count += 1
                except Exception as e:
                    pass

        if count > 0:
            print(f"  {airport}: {count} procedure maps")

    print("\n" + "=" * 60)
    print("Conversion Complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
