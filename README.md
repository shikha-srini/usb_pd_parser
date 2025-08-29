# USB PD Specification Parser 🚀

A clean, object-oriented Python application for parsing USB Power Delivery specification PDFs and generating structured outputs.

## 📋 Overview

This project provides a robust solution for extracting and structuring content from USB PD specification documents. It follows Object-Oriented Programming (OOP) principles with clean separation of concerns, making it maintainable and extensible.

## ✨ Features

- **PDF Parsing**: Extract text and structure from PDF documents
- **Table of Contents Extraction**: Identify and parse document sections
- **Content Analysis**: Analyze sections for tables, figures, and word counts
- **Multiple Output Formats**: Generate JSONL files and Excel validation reports
- **Data Validation**: Comprehensive validation of output integrity
- **Clean OOP Architecture**: Well-structured, maintainable code

## 🏗️ Architecture

The project follows a clean, modular architecture with clear separation of responsibilities:

```
usb_pd_parser/
├── usb_pd_parser.py          # Main application entry point
├── src/                      # Source code modules
│   ├── parser.py            # PDF parsing and content extraction
│   ├── output.py            # Output file generation
│   └── validator.py         # Data validation and integrity checks
├── output/                   # Generated output files
├── tests/                    # Test suite
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Core Classes

1. **`USBPDParserApp`** - Main application orchestrator
2. **`PDFParser`** - Handles PDF loading and content extraction
3. **`OutputManager`** - Manages generation of all output files
4. **`ValidationManager`** - Validates output integrity and schema compliance

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd usb_pd_parser
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample outputs:**
   ```bash
   python usb_pd_parser.py --samples
   ```

### Usage

#### Basic PDF Parsing
```bash
python usb_pd_parser.py -i "your_spec.pdf"
```

#### Custom Output Directory
```bash
python usb_pd_parser.py -i "your_spec.pdf" -o "custom_output/"
```

#### Verbose Logging
```bash
python usb_pd_parser.py -i "your_spec.pdf" --verbose
```

#### Generate Sample Files
```bash
python usb_pd_parser.py --samples
```

## 📁 Output Files

The parser generates the following output files:

### 1. **`usb_pd_toc.jsonl`** - Table of Contents
Contains structured table of contents entries with:
- Section IDs and titles
- Page numbers and hierarchy levels
- Parent-child relationships
- Semantic tags

### 2. **`usb_pd_spec.jsonl`** - Document Sections
Contains detailed section information including:
- Content boundaries (start/end pages)
- Table and figure detection
- Word count estimates
- Hierarchical structure

### 3. **`usb_pd_metadata.jsonl`** - Document Metadata
Contains document-level information:
- Total pages and sections
- Parsing timestamp
- File size and statistics
- Error tracking

### 4. **`validation_report.xlsx`** - Validation Report
Excel file with multiple sheets:
- **Summary**: Overall parsing statistics
- **ToC_vs_Parsed**: Comparison between ToC and parsed content
- **Detailed_Analysis**: Section-by-section analysis
- **Statistics**: Hierarchical breakdown and content analysis

## 🔧 Technical Details

### Dependencies

- **`pdfplumber`** - PDF text extraction and analysis
- **`pandas`** - Data manipulation and Excel generation
- **`openpyxl`** - Excel file creation
- **`jsonschema`** - JSON schema validation

### Code Quality

- **PEP 8 Compliance**: Follows Python style guidelines
- **Type Hints**: Full type annotation support
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging throughout
- **Testing**: Unit test coverage for all modules

### OOP Principles

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Easy to extend without modifying existing code
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Interface Segregation**: Clients only depend on methods they use

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
python -m unittest tests.test_parser -v
```

## 📊 Sample Output

After running `--samples`, you'll get:

```json
// usb_pd_toc.jsonl
{"doc_title": "USB Power Delivery Specification Rev X", "section_id": "2", "title": "Overview", "page": 53, "level": 1, "parent_id": null, "full_path": "2 Overview", "tags": []}

// usb_pd_spec.jsonl  
{"doc_title": "USB Power Delivery Specification Rev X", "section_id": "2", "title": "Overview", "page": 53, "level": 1, "parent_id": null, "full_path": "2 Overview", "tags": [], "content_start": 53, "content_end": 54, "has_tables": false, "has_figures": false, "word_count": 150}
```

## 🔍 How It Works

### 1. **PDF Loading**
- Opens PDF using pdfplumber
- Validates file integrity
- Extracts basic document information

### 2. **Content Extraction**
- Identifies table of contents pages
- Parses section patterns using regex
- Builds hierarchical relationships
- Extracts metadata and statistics

### 3. **Output Generation**
- Creates JSONL files for each data type
- Generates Excel validation report
- Ensures proper formatting and structure

### 4. **Validation**
- Schema validation for all JSONL files
- Data integrity checks between ToC and sections
- Comprehensive error reporting

## 🛠️ Customization

### Adding New Section Patterns

Modify the `section_patterns` in `PDFParser`:

```python
self.section_patterns = [
    r'^(\d+(?:\.\d+)*)\s+([^\n]+?)(?:\s+(\d+))?$',  # "2.1.2 Title [page]"
    r'^(\d+(?:\.\d+)*)\s+([^\n]+?)\s+(\d+)$',       # "2.1.2 Title 53"
    r'^(?:Chapter\s+)?(\d+)\s+([^\n]+?)(?:\s+(\d+))?$'  # "Chapter 2 Title"
]
```

### Custom Output Formats

Extend `OutputManager` to add new output formats:

```python
def generate_custom_format(self, data, filename):
    # Your custom format logic here
    pass
```

## 🐛 Troubleshooting

### Common Issues

1. **PDF Loading Failed**
   - Ensure PDF is not password-protected
   - Check file corruption
   - Verify PDF format compatibility

2. **No Sections Found**
   - Check if PDF has clear table of contents
   - Verify section numbering patterns
   - Review ToC page identification logic

3. **Validation Errors**
   - Check JSONL file format
   - Verify required fields are present
   - Review schema compliance

### Debug Mode

Use verbose logging for detailed information:

```bash
python usb_pd_parser.py -i "spec.pdf" --verbose
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with modern Python best practices
- Inspired by the need for structured document parsing
- Designed for maintainability and extensibility

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the documentation
- Review the test suite for examples

---

**Happy Parsing! 🎉**
