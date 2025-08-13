#!/usr/bin/env python3
"""
Quick Start script for USB PD Specification Parser
Helps users quickly set up and test the system.
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
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
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_tests():
    """Run the test suite."""
    print("\n🧪 Running tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_parser.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def generate_sample_output():
    """Generate sample output files."""
    print("\n📄 Generating sample output...")
    
    try:
        result = subprocess.run([
            sys.executable, "usb_pd_parser.py", "--generate_samples"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample output generated successfully")
            return True
        else:
            print("❌ Failed to generate sample output:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to generate sample output: {e}")
        return False

def run_demo():
    """Run the demo script."""
    print("\n🚀 Running demo...")
    
    try:
        result = subprocess.run([
            sys.executable, "demo.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Demo completed successfully")
            return True
        else:
            print("❌ Demo failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run demo: {e}")
        return False

def show_file_structure():
    """Show the generated file structure."""
    print("\n📁 Generated file structure:")
    
    output_dir = Path("output")
    if output_dir.exists():
        for file_path in output_dir.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(output_dir)
                size = file_path.stat().st_size
                print(f"  📄 {relative_path} ({size:,} bytes)")
    else:
        print("  No output directory found")

def show_usage_examples():
    """Show usage examples."""
    print("\n💡 Usage Examples:")
    print("  1. Parse a PDF file:")
    print("     python usb_pd_parser.py --input your_spec.pdf")
    print("")
    print("  2. Generate sample output:")
    print("     python usb_pd_parser.py --generate_samples")
    print("")
    print("  3. Run with verbose logging:")
    print("     python usb_pd_parser.py --input your_spec.pdf --verbose")
    print("")
    print("  4. Specify custom output directory:")
    print("     python usb_pd_parser.py --input your_spec.pdf --output_dir custom_output/")

def main():
    """Main quick start function."""
    print("🚀 USB PD Specification Parser - Quick Start")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        if not install_dependencies():
            print("\n❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Tests failed, but continuing with setup...")
    
    # Generate sample output
    if not generate_sample_output():
        print("\n⚠️  Failed to generate sample output, but continuing...")
    
    # Run demo
    if not run_demo():
        print("\n⚠️  Demo failed, but continuing...")
    
    # Show results
    show_file_structure()
    
    # Show usage examples
    show_usage_examples()
    
    print("\n" + "=" * 60)
    print("✅ Quick start completed!")
    print("\n📋 Next steps:")
    print("  1. Place your USB PD specification PDF in the project directory")
    print("  2. Run: python usb_pd_parser.py --input your_file.pdf")
    print("  3. Check the 'output' directory for generated files")
    print("  4. Review the validation report for parsing quality")
    
    print("\n🔧 Troubleshooting:")
    print("  • If you encounter issues, check the log file: usb_pd_parser.log")
    print("  • Run with --verbose flag for detailed logging")
    print("  • Ensure your PDF has a clear table of contents")
    print("  • Check that the PDF is not password-protected or corrupted")

if __name__ == "__main__":
    main()
