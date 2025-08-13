# USB Power Delivery (USB PD) Specification Parsing System

## Overview
This system intelligently parses USB PD specification PDF documents and converts them into structured, machine-readable JSONL formats. It extracts the Table of Contents (ToC) hierarchy, document sections, and generates validation reports.

## ✨ Features
- **Interactive PDF Upload**: Easy-to-use interface for uploading and parsing PDFs
- **Automatic ToC Detection**: Intelligently identifies and extracts table of contents
- **Hierarchical Structure**: Builds parent-child relationships between sections
- **Content Analysis**: Detects tables, figures, and analyzes section content
- **Multiple Output Formats**: Generates JSONL files and Excel validation reports
- **Schema Validation**: Ensures data integrity using JSON schemas
- **Flexible Usage**: Both interactive and command-line modes available

## 📊 Output Files
The system generates the following structured outputs:

### 1. `usb_pd_toc.jsonl` - Table of Contents
```json
{
  "doc_title": "USB Power Delivery Specification Rev X",
  "section_id": "2.1.2",
  "title": "Power Delivery Contract Negotiation",
  "page": 53,
  "level": 3,
  "parent_id": "2.1",
  "full_path": "2.1.2 Power Delivery Contract Negotiation",
  "tags": ["contracts", "negotiation"]
}
```

### 2. `usb_pd_spec.jsonl` - Document Sections
```json
{
  "doc_title": "USB Power Delivery Specification Rev X",
  "section_id": "2.1.2",
  "title": "Power Delivery Contract Negotiation",
  "page": 53,
  "level": 3,
  "parent_id": "2.1",
  "content_preview": "This section describes...",
  "word_count": 1250,
  "has_tables": true,
  "has_figures": false,
  "tags": ["contracts", "negotiation"]
}
```

### 3. `usb_pd_metadata.jsonl` - Document Metadata
```json
{
  "doc_title": "USB Power Delivery Specification Rev X",
  "total_pages": 450,
  "total_sections": 156,
  "total_tables": 23,
  "total_figures": 45,
  "parsing_timestamp": "2024-01-15T10:30:00Z",
  "file_size_bytes": 5242880,
  "parser_version": "1.0.0"
}
```

### 4. `validation_report.xlsx` - Validation Report
Excel file with multiple sheets comparing ToC vs parsed sections, identifying mismatches, order errors, and gaps.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Required packages (see `requirements.txt`)

### Installation
```bash
# Clone or download the project
cd usb_parser

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Interactive Mode (Recommended)
Simply run the script without arguments for an interactive experience:

```bash
python usb_pd_parser.py
```

The script will:
1. Ask for your PDF file path
2. Ask for output directory
3. Confirm parsing parameters
4. Process the PDF and generate outputs
5. Optionally open the output directory

### Command-Line Mode
For automated or scripted usage:

```bash
# Basic usage
python usb_pd_parser.py -i "path/to/spec.pdf" -o "output/"

# With verbose logging
python usb_pd_parser.py -i "spec.pdf" -o "output/" --verbose

# Generate sample files
python usb_pd_parser.py --generate_samples

# Validate existing outputs
python usb_pd_parser.py --validate_only
```

### Command-Line Options
- `-i, --input`: Path to input PDF file
- `-o, --output_dir`: Output directory (default: output/)
- `-v, --verbose`: Enable verbose logging
- `-s, --generate_samples`: Generate sample output files
- `--validate_only`: Only validate existing output files

## 🏗️ Architecture

### Core Components
- **`pdf_parser.py`**: Main PDF parsing logic and text extraction
- **`output_generator.py`**: Output file generation and validation reporting
- **`schemas.py`**: JSON schema definitions for data validation
- **`config.py`**: Configuration settings and patterns
- **`usb_pd_parser.py`**: Main orchestration script

### Key Classes
- **`USBPDParser`**: Handles PDF opening, ToC extraction, and section parsing
- **`OutputGenerator`**: Manages output file creation and validation reports
- **`JSONSchemaValidator`**: Ensures output data integrity

## 🔧 Configuration

The system is highly configurable through `config.py`:

- **PDF Parsing Settings**: Page limits, margin tolerances
- **Section Patterns**: Regex patterns for identifying sections
- **ToC Indicators**: Keywords that suggest table of contents pages
- **USB PD Terms**: Domain-specific terminology for tagging
- **Output Settings**: File encodings, Excel engines, validation options

## 📋 Requirements Compliance

### Assignment Requirements Met
✅ **Python Scripts**: Complete parsing system implemented  
✅ **ToC Extraction**: Automatic table of contents identification  
✅ **JSON Schema**: Comprehensive schema definitions  
✅ **JSONL Output**: Structured data in required format  
✅ **Validation Reports**: Excel-based comparison reports  
✅ **Sample Files**: Complete sample output generation  
✅ **Documentation**: Comprehensive README and code comments  

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_parser.py
```

## 📝 Logging

The system provides comprehensive logging:
- File logging: `usb_pd_parser.log`
- Console output with progress indicators
- Detailed error reporting and debugging information

## 🚨 Error Handling

- **PDF Issues**: Corrupted files, password protection, format problems
- **Parsing Errors**: Missing ToC, unrecognized section formats
- **Output Errors**: File permission issues, disk space problems
- **Validation Errors**: Schema violations, data inconsistencies

## 🔮 Future Enhancements

- **Batch Processing**: Multiple PDF processing
- **Advanced Content Analysis**: Table and figure extraction
- **Export Formats**: Additional output formats (XML, CSV)
- **Web Interface**: REST API for integration
- **Machine Learning**: Improved pattern recognition

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.

---

**Note**: This system is designed specifically for USB Power Delivery specification documents but can be adapted for other technical PDFs with similar structure.
