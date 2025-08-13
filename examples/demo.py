#!/usr/bin/env python3
"""
Demo script for USB PD Specification Parser
Demonstrates the system's capabilities with sample data.
"""

import os
import json
import tempfile
from datetime import datetime
from src.core import OutputGenerator
from src.schemas import TOC_SCHEMA, SECTION_SCHEMA, METADATA_SCHEMA
from jsonschema import validate

def create_sample_data():
    """Create sample data for demonstration."""
    
    # Sample ToC entries based on the assignment requirements
    sample_toc = [
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2",
            "title": "Overview",
            "full_path": "2 Overview",
            "page": 53,
            "level": 1,
            "parent_id": None,
            "tags": []
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.1",
            "title": "Introduction",
            "full_path": "2.1 Introduction",
            "page": 53,
            "level": 2,
            "parent_id": "2",
            "tags": []
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.1.1",
            "title": "Power Delivery Source Operational Contracts",
            "full_path": "2.1.1 Power Delivery Source Operational Contracts",
            "page": 53,
            "level": 3,
            "parent_id": "2.1",
            "tags": ["contracts", "source"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.1.2",
            "title": "Power Delivery Contract Negotiation",
            "full_path": "2.1.2 Power Delivery Contract Negotiation",
            "page": 53,
            "level": 3,
            "parent_id": "2.1",
            "tags": ["contracts", "negotiation"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.1.3",
            "title": "Other Uses for Power Delivery",
            "full_path": "2.1.3 Other Uses for Power Delivery",
            "page": 54,
            "level": 3,
            "parent_id": "2.1",
            "tags": ["applications"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.2",
            "title": "Compatibility with Revision 2.0",
            "full_path": "2.2 Compatibility with Revision 2.0",
            "page": 54,
            "level": 2,
            "parent_id": "2",
            "tags": ["revision"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.3",
            "title": "USB Power Delivery Capable Devices",
            "full_path": "2.3 USB Power Delivery Capable Devices",
            "page": 55,
            "level": 2,
            "parent_id": "2",
            "tags": ["devices"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.4",
            "title": "SOP* Communication",
            "full_path": "2.4 SOP* Communication",
            "page": 57,
            "level": 2,
            "parent_id": "2",
            "tags": ["communication"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.4.1",
            "title": "Introduction",
            "full_path": "2.4.1 Introduction",
            "page": 57,
            "level": 3,
            "parent_id": "2.4",
            "tags": []
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.4.2",
            "title": "SOP* Collision Avoidance",
            "full_path": "2.4.2 SOP* Collision Avoidance",
            "page": 57,
            "level": 3,
            "parent_id": "2.4",
            "tags": ["collision", "avoidance"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.4.3",
            "title": "SOP Communication",
            "full_path": "2.4.3 SOP Communication",
            "page": 57,
            "level": 3,
            "parent_id": "2.4",
            "tags": ["communication"]
        },
        {
            "doc_title": "USB Power Delivery Specification Rev X",
            "section_id": "2.4.4",
            "title": "SOP'/SOP'' Communication with Cable Plugs",
            "full_path": "2.4.4 SOP'/SOP'' Communication with Cable Plugs",
            "page": 57,
            "level": 3,
            "parent_id": "2.4",
            "tags": ["cable", "SOP'"]
        }
    ]
    
    # Sample sections with additional metadata
    sample_sections = []
    for i, toc_entry in enumerate(sample_toc):
        section = toc_entry.copy()
        
        # Add section-specific fields
        section['content_start'] = toc_entry['page']
        
        # Determine content end (next section's start - 1)
        if i + 1 < len(sample_toc):
            section['content_end'] = sample_toc[i + 1]['page'] - 1
        else:
            section['content_end'] = None
        
        # Add content analysis
        section.update({
            'has_tables': i % 3 == 0,  # Every 3rd section has tables
            'has_figures': i % 4 == 0,  # Every 4th section has figures
            'word_count': 100 + (i * 25)  # Increasing word count
        })
        
        sample_sections.append(section)
    
    # Sample metadata
    sample_metadata = {
        "doc_title": "USB Power Delivery Specification Rev X",
        "total_pages": 100,
        "total_sections": len(sample_sections),
        "total_tables": sum(1 for s in sample_sections if s.get('has_tables', False)),
        "total_figures": sum(1 for s in sample_sections if s.get('has_figures', False)),
        "max_level": max((s['level'] for s in sample_sections), default=1),
        "parsing_timestamp": datetime.now().isoformat(),
        "pdf_file_size": 1024000,
        "parsing_errors": []
    }
    
    return sample_toc, sample_sections, sample_metadata

def demonstrate_schema_validation():
    """Demonstrate JSON schema validation."""
    print("🔍 Demonstrating JSON Schema Validation...")
    
    sample_toc, sample_sections, sample_metadata = create_sample_data()
    
    # Validate ToC entries
    print("\n📋 Validating ToC entries...")
    for i, entry in enumerate(sample_toc):
        try:
            validate(entry, TOC_SCHEMA)
            print(f"  ✓ ToC entry {i+1}: {entry['section_id']} - {entry['title']}")
        except Exception as e:
            print(f"  ✗ ToC entry {i+1} validation failed: {e}")
    
    # Validate sections
    print("\n📖 Validating sections...")
    for i, section in enumerate(sample_sections):
        try:
            validate(section, SECTION_SCHEMA)
            print(f"  ✓ Section {i+1}: {section['section_id']} - {section['title']}")
        except Exception as e:
            print(f"  ✗ Section {i+1} validation failed: {e}")
    
    # Validate metadata
    print("\n📊 Validating metadata...")
    try:
        validate(sample_metadata, METADATA_SCHEMA)
        print(f"  ✓ Metadata validation passed")
    except Exception as e:
        print(f"  ✗ Metadata validation failed: {e}")
    
    return sample_toc, sample_sections, sample_metadata

def demonstrate_output_generation():
    """Demonstrate output file generation."""
    print("\n🔄 Demonstrating Output Generation...")
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        output_gen = OutputGenerator(temp_dir)
        
        # Generate sample data
        sample_toc, sample_sections, sample_metadata = create_sample_data()
        
        # Generate ToC JSONL
        print("\n📄 Generating ToC JSONL...")
        toc_file = output_gen.generate_toc_jsonl(sample_toc, "USB Power Delivery Specification Rev X")
        if toc_file:
            print(f"  ✓ ToC JSONL generated: {os.path.basename(toc_file)}")
            
            # Show file contents
            with open(toc_file, 'r') as f:
                first_line = f.readline().strip()
                print(f"  📝 Sample line: {first_line[:80]}...")
        
        # Generate Spec JSONL
        print("\n📚 Generating Spec JSONL...")
        spec_file = output_gen.generate_spec_jsonl(sample_sections, "USB Power Delivery Specification Rev X")
        if spec_file:
            print(f"  ✓ Spec JSONL generated: {os.path.basename(spec_file)}")
            
            # Show file contents
            with open(spec_file, 'r') as f:
                first_line = f.readline().strip()
                print(f"  📝 Sample line: {first_line[:80]}...")
        
        # Generate Metadata JSONL
        print("\n📊 Generating Metadata JSONL...")
        metadata_file = output_gen.generate_metadata_jsonl(sample_metadata)
        if metadata_file:
            print(f"  ✓ Metadata JSONL generated: {os.path.basename(metadata_file)}")
        
        # Generate Validation Report
        print("\n📊 Generating Validation Report...")
        validation_file = output_gen.generate_validation_report(sample_toc, sample_sections, sample_metadata)
        if validation_file:
            print(f"  ✓ Validation report generated: {os.path.basename(validation_file)}")
        
        # List generated files
        print(f"\n📁 Generated files in: {temp_dir}")
        for filename in os.listdir(temp_dir):
            if filename.endswith(('.jsonl', '.xlsx')):
                filepath = os.path.join(temp_dir, filename)
                filesize = os.path.getsize(filepath)
                print(f"  📄 {filename} ({filesize:,} bytes)")

def demonstrate_hierarchy_analysis():
    """Demonstrate hierarchy analysis capabilities."""
    print("\n🌳 Demonstrating Hierarchy Analysis...")
    
    sample_toc, sample_sections, sample_metadata = create_sample_data()
    
    # Analyze hierarchy levels
    level_counts = {}
    for section in sample_sections:
        level = section['level']
        level_counts[level] = level_counts.get(level, 0) + 1
    
    print("\n📊 Hierarchy Analysis:")
    for level in sorted(level_counts.keys()):
        count = level_counts[level]
        indent = "  " * (level - 1)
        print(f"{indent}Level {level}: {count} sections")
    
    # Show parent-child relationships
    print("\n👨‍👩‍👧‍👦 Parent-Child Relationships:")
    for section in sample_sections:
        if section['parent_id']:
            parent = next((s for s in sample_sections if s['section_id'] == section['parent_id']), None)
            if parent:
                indent = "  " * (section['level'] - 1)
                print(f"{indent}{section['section_id']} → {parent['section_id']} ({parent['title']})")
    
    # Analyze content distribution
    print("\n📈 Content Distribution:")
    total_words = sum(s.get('word_count', 0) for s in sample_sections)
    sections_with_tables = sum(1 for s in sample_sections if s.get('has_tables', False))
    sections_with_figures = sum(1 for s in sample_sections if s.get('has_figures', False))
    
    print(f"  Total word count: {total_words:,}")
    print(f"  Sections with tables: {sections_with_tables}")
    print(f"  Sections with figures: {sections_with_figures}")
    print(f"  Average words per section: {total_words // len(sample_sections):,}")

def main():
    """Main demo function."""
    print("🚀 USB PD Specification Parser Demo")
    print("=" * 50)
    
    try:
        # Demonstrate schema validation
        sample_toc, sample_sections, sample_metadata = demonstrate_schema_validation()
        
        # Demonstrate output generation
        demonstrate_output_generation()
        
        # Demonstrate hierarchy analysis
        demonstrate_hierarchy_analysis()
        
        print("\n" + "=" * 50)
        print("✅ Demo completed successfully!")
        print("\n📋 Summary:")
        print(f"  • ToC entries: {len(sample_toc)}")
        print(f"  • Sections: {len(sample_sections)}")
        print(f"  • Max hierarchy level: {sample_metadata['max_level']}")
        print(f"  • Tables detected: {sample_metadata['total_tables']}")
        print(f"  • Figures detected: {sample_metadata['total_figures']}")
        
        print("\n💡 Next steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run tests: python test_parser.py")
        print("  3. Parse a PDF: python usb_pd_parser.py --input your_file.pdf")
        print("  4. Generate samples: python usb_pd_parser.py --generate_samples")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
