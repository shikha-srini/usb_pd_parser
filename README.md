# USB PD Specification Parser 🚀

> **Intelligent PDF parsing system for USB Power Delivery specifications**

## 🎯 **Quick Start**

```bash
# Run the interactive parser
python usb_pd_parser.py

# Or use command-line mode
python usb_pd_parser.py -i "your_spec.pdf" -o "output/"
```

## 📁 **Project Structure**

```
usb_parser/
├── 📁 src/                    # Source code
│   ├── 📁 core/              # Core parsing logic
│   ├── 📁 schemas/           # Data validation
│   └── 📁 config/            # Configuration
├── 📁 tests/                 # Test suite
├── 📁 examples/              # Demo scripts
├── 📁 docs/                  # Documentation
└── usb_pd_parser.py         # Main entry point
```

## ✨ **Features**

- 🔍 **Interactive PDF Upload** - Easy-to-use interface
- 📑 **Automatic ToC Extraction** - Smart table of contents detection
- 🏗️ **Hierarchical Structure** - Parent-child section relationships
- 📊 **Content Analysis** - Tables, figures, and metadata detection
- 💾 **Multiple Outputs** - JSONL files and Excel validation reports
- ✅ **Schema Validation** - Data integrity assurance

## 📚 **Documentation**

- **[📖 Full Documentation](docs/README.md)** - Complete usage guide
- **[🏗️ Project Structure](docs/PROJECT_STRUCTURE.md)** - Code organization
- **[📋 Project Summary](docs/PROJECT_SUMMARY.md)** - Overview and features

## 🧪 **Testing & Examples**

```bash
# Run tests
python tests/test_parser.py

# Run demos
python examples/demo.py
python examples/demo_interactive.py
python examples/quick_start.py
```

## 🔧 **Installation**

```bash
pip install -r requirements.txt
```

## 📊 **Output Files**

- `usb_pd_toc.jsonl` - Table of Contents
- `usb_pd_spec.jsonl` - Document Sections  
- `usb_pd_metadata.jsonl` - Document Metadata
- `validation_report.xlsx` - Validation Report

## 🚀 **Ready to Parse?**

Just run `python usb_pd_parser.py` and follow the interactive prompts!

---

**📁 [View Full Documentation](docs/README.md) | 🧪 [Run Tests](tests/) | 💡 [Examples](examples/)**
