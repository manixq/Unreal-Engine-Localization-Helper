# Unreal Engine Localization Helper

A Python utility for managing Unreal Engine 5.x localization files. This tool helps you convert between PO (gettext) and CSV formats, making it easier to work with translations in spreadsheet applications.

## Features

- **po2csv**: Convert PO files to CSV format (with or without duplicates)
- **csv2po**: Convert CSV files back to PO format
- **fill2po**: Fill empty translations in existing PO files from CSV data

## Installation

### Requirements

- Python 2.7 or Python 3.x
- Required packages:
  - `polib`
  - `unicodecsv`

### Install Dependencies

```bash
pip install polib unicodecsv
```

## Usage

### 1. Convert PO to CSV

Convert a PO file to CSV format. You can choose to include or exclude duplicate entries.

```bash
# With duplicates
python main.py po2csv <po_file> True

# Without duplicates (creates a no_dupes_ prefixed file and dupes.txt)
python main.py po2csv <po_file> False
```

**Example:**
```bash
python main.py po2csv Game.po True
```

This creates a CSV file with columns: `comment`, `msgctxt`, `Raw`, `English`

### 2. Convert CSV to PO

Convert a CSV file to PO format. Specify which column contains the translations.

```bash
python main.py csv2po <csv_file> <csv_column>
```

**Example:**
```bash
python main.py csv2po translations.csv 3
```

The column index is 0-based (0 = first column, 1 = second column, etc.)

### 3. Fill Empty Translations in PO File

Update an existing PO file with translations from a CSV file. Only fills entries where `msgstr` is empty.

```bash
python main.py fill2po <csv_file> <csv_column> <po_file>
```

**Example:**
```bash
python main.py fill2po translations.csv 3 Game.po
```

This command:
- Matches entries by `msgctxt` (context) first, then by `msgid` (source text)
- Only updates entries with empty translations
- Reports how many rows were filled and how many were not found

## Manifest Files

This repository includes two important manifest files that need to be copied to your Unreal Engine installation directories:

### Copy these files:

```
Engine.manifest → UE_5.6\Engine\Content\Localization\Engine\
Editor.manifest → UE_5.6\Engine\Content\Localization\Editor\
```

**Note:** Replace `UE_5.6` with your actual Unreal Engine version directory (e.g., `UE_5.5`, `UE_5.4`, etc.)

These manifest files are essential for Unreal Engine's localization system to properly recognize and process translations.

## CSV Format

When working with CSV files, the expected format is:

| Column 0 | Column 1 | Column 2 | Column 3+ |
|----------|----------|----------|-----------|
| msgctxt  | msgid    | Raw      | Translation(s) |

- **msgctxt**: Context identifier for the translation
- **msgid**: Source text (original language)
- **Raw**: Raw text field
- **Translation columns**: One or more columns with translations in different languages

## License

Please refer to the repository license for terms of use.
