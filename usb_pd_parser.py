#!/usr/bin/env python3
"""
USB PD Specification Parser
A clean, object-oriented PDF parser for USB Power Delivery specifications.
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from src.parser import PDFParser
from src.output import OutputManager
from src.validator import ValidationManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class USBPDParserApp:
    """Main application class for USB PD parsing."""
    
    def __init__(self, output_dir="output"):
        """Initialize the parser application."""
        self.output_dir = output_dir
        self.parser = PDFParser()
        self.output_manager = OutputManager(output_dir)
        self.validator = ValidationManager()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def parse_pdf(self, pdf_path, verbose=False):
        """Parse a PDF file and generate all outputs."""
        try:
            if verbose:
                logging.getLogger().setLevel(logging.DEBUG)
            
            logger.info("Starting USB PD Specification parsing...")
            print(f"🔍 Parsing: {pdf_path}")
            
            # Parse PDF
            if not self.parser.load_pdf(pdf_path):
                print("❌ Failed to load PDF file")
                return False
            
            # Extract content
            doc_title = self.parser.extract_title()
            toc_entries = self.parser.extract_toc()
            sections = self.parser.extract_sections()
            metadata = self.parser.generate_metadata()
            
            print(f"✅ Extracted {len(toc_entries)} ToC entries and {len(sections)} sections")
            
            # Generate outputs
            self.output_manager.generate_toc_file(toc_entries, doc_title)
            self.output_manager.generate_spec_file(sections, doc_title)
            self.output_manager.generate_metadata_file(metadata)
            self.output_manager.generate_validation_report(toc_entries, sections, metadata)
            
            # Validate outputs
            validation_result = self.validator.validate_outputs(self.output_dir)
            
            print(f"✅ All outputs generated in: {self.output_dir}")
            print(f"📊 Validation: {'PASS' if validation_result else 'FAIL'}")
            
            return True
            
        except Exception as e:
            logger.error(f"Parsing failed: {e}")
            print(f"❌ Error: {e}")
            return False
    
    def generate_samples(self):
        """Generate sample output files for demonstration."""
        try:
            logger.info("Generating sample outputs...")
            
            # Create sample data
            sample_data = self._create_sample_data()
            
            # Generate sample files
            self.output_manager.generate_toc_file(sample_data['toc'], sample_data['title'])
            self.output_manager.generate_spec_file(sample_data['sections'], sample_data['title'])
            self.output_manager.generate_metadata_file(sample_data['metadata'])
            self.output_manager.generate_validation_report(
                sample_data['toc'], 
                sample_data['sections'], 
                sample_data['metadata']
            )
            
            print(f"✅ Sample files generated in: {self.output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Sample generation failed: {e}")
            print(f"❌ Error: {e}")
            return False
    
    def _create_sample_data(self):
        """Create sample data for demonstration."""
        return {
            'title': "USB Power Delivery Specification Rev X",
            'toc': [
                {
                    "section_id": "2",
                    "title": "Overview",
                    "page": 53,
                    "level": 1,
                    "parent_id": None,
                    "tags": []
                },
                {
                    "section_id": "2.1",
                    "title": "Introduction",
                    "page": 53,
                    "level": 2,
                    "parent_id": "2",
                    "tags": []
                },
                {
                    "section_id": "2.1.1",
                    "title": "Power Delivery Contracts",
                    "page": 53,
                    "level": 3,
                    "parent_id": "2.1",
                    "tags": ["contracts", "power"]
                }
            ],
            'sections': [
                {
                    "section_id": "2",
                    "title": "Overview",
                    "page": 53,
                    "level": 1,
                    "parent_id": None,
                    "tags": [],
                    "content_start": 53,
                    "content_end": 54,
                    "has_tables": False,
                    "has_figures": False,
                    "word_count": 150
                }
            ],
            'metadata': {
                "total_pages": 100,
                "total_sections": 3,
                "total_tables": 0,
                "total_figures": 0,
                "max_level": 3,
                "parsing_timestamp": datetime.now().isoformat()
            }
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='USB PD Specification Parser - Clean OOP Implementation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python usb_pd_parser.py -i "spec.pdf"          # Parse PDF
  python usb_pd_parser.py -i "spec.pdf" -o "out" # Custom output dir
  python usb_pd_parser.py -i "spec.pdf" --verbose # Verbose logging
  python usb_pd_parser.py --samples               # Generate samples
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        help='Path to input PDF file'
    )
    
    parser.add_argument(
        '--output_dir', '-o',
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--samples',
        action='store_true',
        help='Generate sample output files'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Initialize application
    app = USBPDParserApp(args.output_dir)
    
    if args.samples:
        # Generate sample files
        success = app.generate_samples()
        sys.exit(0 if success else 1)
    
    elif args.input:
        # Parse PDF file
        if not os.path.exists(args.input):
            print(f"❌ File not found: {args.input}")
            sys.exit(1)
        
        if not args.input.lower().endswith('.pdf'):
            print(f"❌ File must be a PDF: {args.input}")
            sys.exit(1)
        
        success = app.parse_pdf(args.input, args.verbose)
        sys.exit(0 if success else 1)
    
    else:
        # Show help
        parser.print_help()
        print("\n💡 Tip: Use --samples to generate sample output files")
        print("💡 Tip: Use -i <file.pdf> to parse a PDF file")


if __name__ == "__main__":
    main()
