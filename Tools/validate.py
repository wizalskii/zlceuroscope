#!/usr/bin/env python3
"""
Validate ZLC Euroscope files for correct formatting
"""

import sys
from pathlib import Path


def validate_ese_file(file_path):
    """Validate .ese file format"""
    errors = []
    warnings = []

    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
            lines = content.splitlines()

        # Check encoding
        try:
            content.encode('latin-1')
        except UnicodeEncodeError as e:
            errors.append(f"File contains non-latin-1 characters: {e}")

        # Check for required sections
        required_sections = ['[POSITIONS]']
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Validate [POSITIONS] section
        in_positions = False
        position_count = 0
        for i, line in enumerate(lines, 1):
            line = line.strip()

            if line == '[POSITIONS]':
                in_positions = True
                continue
            elif line.startswith('['):
                in_positions = False

            if in_positions and line and not line.startswith(';'):
                # Check position format
                parts = line.split(':')
                if len(parts) < 9:
                    errors.append(f"Line {i}: Invalid position format (need 9 fields): {line}")
                else:
                    position_count += 1
                    # Validate frequency format (should have 5 decimal places)
                    try:
                        freq = float(parts[1])
                        freq_str = parts[1]
                        if '.' in freq_str:
                            decimals = len(freq_str.split('.')[1])
                            if decimals != 5:
                                warnings.append(f"Line {i}: Frequency should have 5 decimal places: {freq_str}")
                    except ValueError:
                        errors.append(f"Line {i}: Invalid frequency: {parts[1]}")

        if position_count == 0:
            warnings.append("No positions found in [POSITIONS] section")

        return errors, warnings, position_count

    except Exception as e:
        return [f"Error reading file: {e}"], [], 0


def validate_sct_file(file_path):
    """Validate .sct file format"""
    errors = []
    warnings = []

    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()

        # Check encoding
        try:
            content.encode('latin-1')
        except UnicodeEncodeError as e:
            errors.append(f"File contains non-latin-1 characters: {e}")

        # Check for required sections
        required_sections = ['[INFO]']
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Check for recommended sections
        recommended_sections = ['[VOR]', '[NDB]', '[FIXES]', '[AIRPORT]']
        for section in recommended_sections:
            if section not in content:
                warnings.append(f"Missing recommended section: {section}")

        return errors, warnings

    except Exception as e:
        return [f"Error reading file: {e}"], []


def main():
    repo_root = Path(__file__).parent.parent

    print("=" * 60)
    print("ZLC Euroscope File Validation")
    print("=" * 60)

    total_errors = 0
    total_warnings = 0

    # Validate .ese file
    ese_path = repo_root / 'ZLC.ese'
    print(f"\nValidating {ese_path}...")

    if ese_path.exists():
        errors, warnings, position_count = validate_ese_file(ese_path)

        if errors:
            print(f"\n  ERRORS ({len(errors)}):")
            for err in errors:
                print(f"    - {err}")
            total_errors += len(errors)

        if warnings:
            print(f"\n  WARNINGS ({len(warnings)}):")
            for warn in warnings:
                print(f"    - {warn}")
            total_warnings += len(warnings)

        if not errors and not warnings:
            print(f"  OK - {position_count} positions defined")
        elif not errors:
            print(f"  OK (with warnings) - {position_count} positions defined")
    else:
        print(f"  ERROR: File not found")
        total_errors += 1

    # Validate .sct file
    sct_path = repo_root / 'ZLC.sct'
    print(f"\nValidating {sct_path}...")

    if sct_path.exists():
        errors, warnings = validate_sct_file(sct_path)

        if errors:
            print(f"\n  ERRORS ({len(errors)}):")
            for err in errors:
                print(f"    - {err}")
            total_errors += len(errors)

        if warnings:
            print(f"\n  WARNINGS ({len(warnings)}):")
            for warn in warnings:
                print(f"    - {warn}")
            total_warnings += len(warnings)

        if not errors and not warnings:
            print(f"  OK")
        elif not errors:
            print(f"  OK (with warnings)")
    else:
        print(f"  ERROR: File not found")
        total_errors += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Validation Summary: {total_errors} errors, {total_warnings} warnings")
    print("=" * 60)

    if total_errors > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
