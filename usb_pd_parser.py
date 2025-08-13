#!/usr/bin/env python3
"""
Main USB PD Specification Parser Script
Orchestrates the entire parsing process with interactive PDF upload.
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from src.core import USBPDParser, OutputGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('usb_pd_parser.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_pdf_path():
    """Get PDF path from user input."""
    print("\n" + "="*60)
    print("USB PD Specification Parser")
    print("="*60)
    print("\n📁 Please provide the path to your USB PD specification PDF file.")
    print("   Examples:")
    print("   - C:\\Documents\\usb_pd_spec.pdf")
    print("   - /home/user/documents/spec.pdf")
    print("   - ./spec.pdf (if in current directory)")
    print("   - Just press Enter to use 'sample.pdf' if it exists")
    
    while True:
        pdf_path = input("\n📄 PDF file path: ").strip().strip('"')
        
        # If user just presses Enter, try to use sample.pdf
        if not pdf_path:
            if os.path.exists('sample.pdf'):
                pdf_path = 'sample.pdf'
                print(f"✅ Using sample.pdf")
                break
            else:
                print("❌ No sample.pdf found. Please provide a valid PDF path.")
                continue
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            print(f"❌ File not found: {pdf_path}")
            continue
        
        # Check if it's a PDF
        if not pdf_path.lower().endswith('.pdf'):
            print(f"❌ File must be a PDF: {pdf_path}")
            continue
        
        print(f"✅ PDF file found: {pdf_path}")
        break
    
    return pdf_path

def get_output_directory():
    """Get output directory from user input."""
    print("\n📂 Where would you like to save the output files?")
    print("   Examples:")
    print("   - output (default)")
    print("   - C:\\Documents\\usb_pd_output")
    print("   - ./results")
    
    output_dir = input("\n📁 Output directory (press Enter for 'output'): ").strip().strip('"')
    
    if not output_dir:
        output_dir = 'output'
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory: {output_dir}")
    
    return output_dir

def confirm_parsing(pdf_path, output_dir):
    """Confirm parsing parameters with user."""
    print("\n" + "="*60)
    print("📋 PARSING CONFIGURATION")
    print("="*60)
    print(f"📄 Input PDF: {pdf_path}")
    print(f"📁 Output Directory: {output_dir}")
    print(f"📊 Files to generate:")
    print(f"   • usb_pd_toc.jsonl (Table of Contents)")
    print(f"   • usb_pd_spec.jsonl (Document Sections)")
    print(f"   • usb_pd_metadata.jsonl (Document Metadata)")
    print(f"   • validation_report.xlsx (Validation Report)")
    
    while True:
        confirm = input("\n🚀 Proceed with parsing? (y/n): ").strip().lower()
        if confirm in ['y', 'yes', '']:
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' or 'n'")

def parse_pdf(pdf_path, output_dir, verbose=False):
    """Parse PDF with given parameters."""
    try:
        # Set logging level
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Start parsing
        logger.info("=" * 60)
        logger.info("USB PD Specification Parser Starting")
        logger.info("=" * 60)
        
        # Initialize output generator
        output_gen = OutputGenerator(output_dir)
        
        logger.info(f"Processing PDF: {pdf_path}")
        logger.info(f"Output directory: {output_dir}")
        
        # Initialize PDF parser
        pdf_parser = USBPDParser(pdf_path)
        
        # Open PDF
        print("\n🔍 Opening PDF file...")
        if not pdf_parser.open_pdf():
            logger.error("Failed to open PDF file")
            print("❌ Failed to open PDF file. Please check if the file is corrupted or password-protected.")
            return False
        
        # Extract document title
        print("📖 Extracting document title...")
        doc_title = pdf_parser.extract_document_title()
        logger.info(f"Document title: {doc_title}")
        print(f"✅ Document title: {doc_title}")
        
        # Extract Table of Contents
        print("📑 Extracting Table of Contents...")
        logger.info("Extracting Table of Contents...")
        toc_entries = pdf_parser.extract_toc_entries()
        
        if not toc_entries:
            logger.warning("No ToC entries found. This might indicate parsing issues.")
            print("⚠️  No ToC entries found. This might indicate parsing issues.")
        else:
            logger.info(f"Found {len(toc_entries)} ToC entries")
            print(f"✅ Found {len(toc_entries)} ToC entries")
        
        # Extract sections
        print("📝 Extracting document sections...")
        logger.info("Extracting document sections...")
        sections = pdf_parser.extract_sections()
        
        if not sections:
            logger.warning("No sections extracted. This might indicate parsing issues.")
            print("⚠️  No sections extracted. This might indicate parsing issues.")
        else:
            logger.info(f"Extracted {len(sections)} sections")
            print(f"✅ Extracted {len(sections)} sections")
        
        # Generate metadata
        print("📊 Generating metadata...")
        logger.info("Generating metadata...")
        metadata = pdf_parser.generate_metadata()
        
        # Generate output files
        print("\n💾 Generating output files...")
        logger.info("Generating output files...")
        
        # ToC JSONL
        print("   📋 Generating ToC JSONL...")
        toc_file = output_gen.generate_toc_jsonl(toc_entries, doc_title)
        if toc_file:
            logger.info(f"✓ ToC JSONL generated: {toc_file}")
            print(f"   ✅ ToC JSONL: {os.path.basename(toc_file)}")
        
        # Spec JSONL
        print("   📄 Generating Spec JSONL...")
        spec_file = output_gen.generate_spec_jsonl(sections, doc_title)
        if spec_file:
            logger.info(f"✓ Spec JSONL generated: {spec_file}")
            print(f"   ✅ Spec JSONL: {os.path.basename(spec_file)}")
        
        # Metadata JSONL
        print("   📊 Generating Metadata JSONL...")
        metadata_file = output_gen.generate_metadata_jsonl(metadata)
        if metadata_file:
            logger.info(f"✓ Metadata JSONL generated: {metadata_file}")
            print(f"   ✅ Metadata JSONL: {os.path.basename(metadata_file)}")
        
        # Validation report
        print("   📈 Generating Validation Report...")
        validation_file = output_gen.generate_validation_report(toc_entries, sections, metadata)
        if validation_file:
            logger.info(f"✓ Validation report generated: {validation_file}")
            print(f"   ✅ Validation Report: {os.path.basename(validation_file)}")
        
        # Close PDF
        pdf_parser.close()
        
        # Summary
        print("\n" + "="*60)
        print("🎉 PARSING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📄 Document: {doc_title}")
        print(f"📊 Total Pages: {metadata.get('total_pages', 'Unknown')}")
        print(f"📑 ToC Entries: {len(toc_entries)}")
        print(f"📝 Sections Parsed: {len(sections)}")
        print(f"📊 Tables Detected: {metadata.get('total_tables', 0)}")
        print(f"🖼️  Figures Detected: {metadata.get('total_figures', 0)}")
        print(f"📁 Output Directory: {output_dir}")
        
        # List generated files
        print("\n📋 Generated Files:")
        total_size = 0
        for filename in os.listdir(output_dir):
            if filename.endswith(('.jsonl', '.xlsx')):
                filepath = os.path.join(output_dir, filename)
                filesize = os.path.getsize(filepath)
                total_size += filesize
                print(f"   📄 {filename} ({filesize:,} bytes)")
        
        print(f"\n💾 Total output size: {total_size:,} bytes")
        print(f"🎯 All files saved to: {os.path.abspath(output_dir)}")
        print("\n✅ Parsing completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error during parsing: {e}")
        logger.error(f"Unexpected error during parsing: {e}")
        logger.exception("Full traceback:")
        return False

def main():
    """Main function to run the USB PD parser."""
    parser = argparse.ArgumentParser(
        description='Parse USB PD Specification PDF and generate structured output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python usb_pd_parser.py                    # Interactive mode
  python usb_pd_parser.py -i "spec.pdf"     # Command-line mode
  python usb_pd_parser.py -i "spec.pdf" -o "output/" --verbose
  python usb_pd_parser.py --generate_samples # Generate sample files
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        help='Path to input PDF file (if not provided, runs in interactive mode)'
    )
    
    parser.add_argument(
        '--output_dir', '-o',
        default='output',
        help='Output directory for generated files (default: output/)'
    )
    
    parser.add_argument(
        '--generate_samples', '-s',
        action='store_true',
        help='Generate sample output files for demonstration'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--validate_only',
        action='store_true',
        help='Only validate existing output files without parsing'
    )
    
    args = parser.parse_args()
    
    # Generate sample files if requested
    if args.generate_samples:
        logger.info("Generating sample output files...")
        output_gen = OutputGenerator(args.output_dir)
        sample_dir = output_gen.generate_sample_output()
        if sample_dir:
            logger.info(f"Sample files generated in: {sample_dir}")
            print(f"✅ Sample files generated in: {sample_dir}")
        return
    
    # Validate existing outputs if requested
    if args.validate_only:
        if validate_existing_outputs(args.output_dir):
            print("✅ All output files validated successfully!")
        else:
            print("❌ Validation failed!")
        return
    
    # If input file is provided, run in command-line mode
    if args.input:
        if not os.path.exists(args.input):
            print(f"❌ Input file not found: {args.input}")
            return
        
        if not args.input.lower().endswith('.pdf'):
            print(f"❌ Input file must be a PDF: {args.input}")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Parse PDF
        success = parse_pdf(args.input, args.output_dir, args.verbose)
        
        if success:
            # Ask if user wants to open output directory
            try:
                open_dir = input("\n📂 Open output directory? (y/n): ").strip().lower()
                if open_dir in ['y', 'yes']:
                    if sys.platform == 'win32':
                        os.startfile(args.output_dir)
                    elif sys.platform == 'darwin':
                        os.system(f'open "{args.output_dir}"')
                    else:
                        os.system(f'xdg-open "{args.output_dir}"')
                    print("✅ Output directory opened!")
            except:
                pass
        
        return
    
    # Interactive mode
    try:
        # Get PDF path from user
        pdf_path = get_pdf_path()
        
        # Get output directory
        output_dir = get_output_directory()
        
        # Confirm parsing
        if not confirm_parsing(pdf_path, output_dir):
            print("\n❌ Parsing cancelled by user")
            return
        
        # Parse PDF
        success = parse_pdf(pdf_path, output_dir)
        
        if success:
            # Ask if user wants to open output directory
            try:
                open_dir = input("\n📂 Open output directory? (y/n): ").strip().lower()
                if open_dir in ['y', 'yes']:
                    if sys.platform == 'win32':
                        os.startfile(output_dir)
                    elif sys.platform == 'darwin':
                        os.system(f'open "{output_dir}"')
                    else:
                        os.system(f'xdg-open "{output_dir}"')
                    print("✅ Output directory opened!")
            except:
                pass
        
    except KeyboardInterrupt:
        print("\n\n❌ Parsing interrupted by user")
        logger.info("\nParsing interrupted by user")
        return

def validate_existing_outputs(output_dir: str):
    """Validate existing output files without parsing."""
    logger.info("Validating existing output files...")
    
    try:
        output_gen = OutputGenerator(output_dir)
        
        # Check if output files exist
        required_files = [
            'usb_pd_toc.jsonl',
            'usb_pd_spec.jsonl', 
            'usb_pd_metadata.jsonl',
            'validation_report.xlsx'
        ]
        
        missing_files = []
        for filename in required_files:
            filepath = os.path.join(output_dir, filename)
            if not os.path.exists(filepath):
                missing_files.append(filename)
        
        if missing_files:
            logger.warning(f"Missing output files: {missing_files}")
            return False
        
        logger.info("All required output files found")
        return True
        
    except Exception as e:
        logger.error(f"Error validating outputs: {e}")
        return False

if __name__ == "__main__":
    main()
