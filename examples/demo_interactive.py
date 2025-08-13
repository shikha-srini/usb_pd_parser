#!/usr/bin/env python3
"""
Interactive Demo for USB PD Specification Parser
This script demonstrates the interactive PDF upload and parsing functionality.
"""

import os
import sys
from pathlib import Path

def show_demo():
    """Show the interactive demo."""
    print("🎯 USB PD Specification Parser - Interactive Demo")
    print("=" * 60)
    print()
    print("This demo shows how the interactive PDF upload works.")
    print("The system will guide you through:")
    print("  1. 📁 Providing PDF file path")
    print("  2. 📂 Choosing output directory")
    print("  3. 📋 Confirming parsing parameters")
    print("  4. 🔍 Processing the PDF")
    print("  5. 💾 Generating structured outputs")
    print()
    
    # Check if sample.pdf exists
    if os.path.exists('sample.pdf'):
        print("✅ Found 'sample.pdf' - you can use this for testing")
        print("   Just press Enter when asked for PDF path")
    else:
        print("📄 No 'sample.pdf' found")
        print("   You'll need to provide a path to your USB PD specification PDF")
    
    print()
    print("🚀 To start the interactive parser, run:")
    print("   python usb_pd_parser.py")
    print()
    print("💡 Tips:")
    print("   - Use absolute paths for best compatibility")
    print("   - Make sure the PDF is not password-protected")
    print("   - The system will create output directories automatically")
    print("   - All outputs are validated against JSON schemas")
    print()
    
    # Show available commands
    print("🔧 Available Commands:")
    print("   python usb_pd_parser.py              # Interactive mode")
    print("   python usb_pd_parser.py -i file.pdf  # Command-line mode")
    print("   python usb_pd_parser.py --generate_samples  # Generate samples")
    print("   python usb_pd_parser.py --validate_only     # Validate outputs")
    print()
    
    # Show project structure
    print("📁 Project Structure:")
    project_files = [
        'usb_pd_parser.py - Main interactive parser',
        'pdf_parser.py - PDF parsing logic',
        'output_generator.py - Output generation',
        'schemas.py - JSON schema definitions',
        'config.py - Configuration settings',
        'test_parser.py - Test suite',
        'requirements.txt - Python dependencies'
    ]
    
    for file_info in project_files:
        print(f"   📄 {file_info}")
    
    print()
    print("🎉 Ready to parse your USB PD specification!")
    print("   Run 'python usb_pd_parser.py' to begin")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pdfplumber',
        'pandas', 
        'openpyxl',
        'jsonschema'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install them with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed!")
        return True

def main():
    """Main demo function."""
    print("🚀 USB PD Specification Parser - Interactive Demo")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return
    
    print()
    
    # Show demo
    show_demo()
    
    # Ask if user wants to run the parser
    print("\n" + "="*60)
    try:
        run_now = input("🚀 Would you like to run the parser now? (y/n): ").strip().lower()
        if run_now in ['y', 'yes', '']:
            print("\n🎯 Starting USB PD Parser...")
            print("   (This will launch the interactive interface)")
            print()
            
            # Import and run the parser
            try:
                import sys
                import os
                # Add the parent directory to the path
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from usb_pd_parser import main as run_parser
                run_parser()
            except ImportError as e:
                print(f"❌ Error importing parser: {e}")
                print("   Make sure all files are in the same directory")
            except Exception as e:
                print(f"❌ Error running parser: {e}")
        else:
            print("\n👋 Demo completed! Run 'python usb_pd_parser.py' when ready.")
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Run 'python usb_pd_parser.py' when ready.")

if __name__ == "__main__":
    main()
