#!/usr/bin/env python3
"""
Test script for USB PD Specification Parser
Tests various components and provides validation.
"""

import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch
from src.core import USBPDParser, OutputGenerator
from src.schemas import TOC_SCHEMA, SECTION_SCHEMA, METADATA_SCHEMA
from jsonschema import validate, ValidationError

class TestUSBPDParser(unittest.TestCase):
    """Test cases for USB PD Parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_pdf_path = os.path.join(self.temp_dir, "sample.pdf")
        
        # Create a mock PDF file
        with open(self.sample_pdf_path, 'w') as f:
            f.write("Mock PDF content")
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_parser_initialization(self):
        """Test parser initialization."""
        parser = USBPDParser(self.sample_pdf_path)
        self.assertEqual(parser.pdf_path, self.sample_pdf_path)
        self.assertIsNone(parser.pdf)
        self.assertEqual(parser.doc_title, "USB Power Delivery Specification")
    
    def test_section_id_parsing(self):
        """Test section ID parsing logic."""
        parser = USBPDParser(self.sample_pdf_path)
        
        # Test section ID to tuple conversion
        self.assertEqual(parser._section_id_to_tuple("2.1.3"), (2, 1, 3))
        self.assertEqual(parser._section_id_to_tuple("1"), (1,))
        self.assertEqual(parser._section_id_to_tuple("10.5.2.1"), (10, 5, 2, 1))
    
    def test_tag_generation(self):
        """Test semantic tag generation."""
        parser = USBPDParser(self.sample_pdf_path)
        
        # Test tag generation for different titles
        tags = parser._generate_tags("Power Delivery Contract Negotiation")
        self.assertIn("power", tags)
        self.assertIn("delivery", tags)
        self.assertIn("contract", tags)
        self.assertIn("negotiation", tags)
        
        tags = parser._generate_tags("Overview and Introduction")
        self.assertIn("overview", tags)
        
        tags = parser._generate_tags("Implementation Requirements")
        self.assertIn("requirements", tags)
        self.assertIn("implementation", tags)
    
    def test_hierarchy_building(self):
        """Test parent-child relationship building."""
        parser = USBPDParser(self.sample_pdf_path)
        
        # Mock ToC entries
        entries = [
            {"section_id": "2", "title": "Overview", "page": 53, "level": 1, "parent_id": None},
            {"section_id": "2.1", "title": "Introduction", "page": 53, "level": 2, "parent_id": None},
            {"section_id": "2.1.1", "title": "Details", "page": 53, "level": 3, "parent_id": None}
        ]
        
        parser._build_hierarchy(entries)
        
        # Check parent relationships
        self.assertIsNone(entries[0]["parent_id"])  # "2" has no parent
        self.assertEqual(entries[1]["parent_id"], "2")  # "2.1" parent is "2"
        self.assertEqual(entries[2]["parent_id"], "2.1")  # "2.1.1" parent is "2.1"

class TestOutputGenerator(unittest.TestCase):
    """Test cases for Output Generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_gen = OutputGenerator(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_output_directory_creation(self):
        """Test output directory creation."""
        new_dir = os.path.join(self.temp_dir, "new_output")
        output_gen = OutputGenerator(new_dir)
        self.assertTrue(os.path.exists(new_dir))
    
    def test_toc_jsonl_generation(self):
        """Test ToC JSONL file generation."""
        sample_toc = [
            {
                "doc_title": "Test Spec",
                "section_id": "1",
                "title": "Introduction",
                "page": 1,
                "level": 1,
                "parent_id": None,
                "full_path": "1 Introduction",
                "tags": []
            }
        ]
        
        output_file = self.output_gen.generate_toc_jsonl(sample_toc, "Test Spec")
        self.assertTrue(os.path.exists(output_file))
        
        # Verify content
        with open(output_file, 'r') as f:
            content = f.read().strip()
            self.assertIn("Test Spec", content)
            self.assertIn("Introduction", content)
    
    def test_schema_validation(self):
        """Test JSON schema validation."""
        # Valid entry
        valid_entry = {
            "doc_title": "Test",
            "section_id": "1.1",
            "title": "Test Section",
            "page": 1,
            "level": 2,
            "parent_id": "1",
            "full_path": "1.1 Test Section",
            "tags": []
        }
        
        # Should not raise exception
        validate(valid_entry, TOC_SCHEMA)
        
        # Invalid entry (missing required field)
        invalid_entry = {
            "doc_title": "Test",
            "section_id": "1.1",
            # Missing title
            "page": 1,
            "level": 2,
            "parent_id": "1",
            "full_path": "1.1 Test Section",
            "tags": []
        }
        
        # Should raise exception
        with self.assertRaises(ValidationError):
            validate(invalid_entry, TOC_SCHEMA)

class TestSchemas(unittest.TestCase):
    """Test cases for JSON schemas."""
    
    def test_toc_schema_validation(self):
        """Test ToC schema validation."""
        valid_toc = {
            "doc_title": "USB PD Spec",
            "section_id": "2.1.2",
            "title": "Power Delivery Contract Negotiation",
            "page": 53,
            "level": 3,
            "parent_id": "2.1",
            "full_path": "2.1.2 Power Delivery Contract Negotiation",
            "tags": ["contracts", "negotiation"]
        }
        
        # Should validate successfully
        validate(valid_toc, TOC_SCHEMA)
    
    def test_section_schema_validation(self):
        """Test section schema validation."""
        valid_section = {
            "doc_title": "USB PD Spec",
            "section_id": "2.1.2",
            "title": "Power Delivery Contract Negotiation",
            "page": 53,
            "level": 3,
            "parent_id": "2.1",
            "full_path": "2.1.2 Power Delivery Contract Negotiation",
            "tags": ["contracts", "negotiation"],
            "content_start": 53,
            "content_end": 54,
            "has_tables": False,
            "has_figures": False,
            "word_count": 150
        }
        
        # Should validate successfully
        validate(valid_section, SECTION_SCHEMA)
    
    def test_metadata_schema_validation(self):
        """Test metadata schema validation."""
        valid_metadata = {
            "doc_title": "USB PD Spec",
            "total_pages": 100,
            "total_sections": 25,
            "total_tables": 5,
            "total_figures": 3,
            "max_level": 4,
            "parsing_timestamp": "2024-01-01T00:00:00",
            "pdf_file_size": 1024000,
            "parsing_errors": []
        }
        
        # Should validate successfully
        validate(valid_metadata, METADATA_SCHEMA)

def run_tests():
    """Run all tests."""
    print("Running USB PD Parser Tests...")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestUSBPDParser))
    test_suite.addTest(unittest.makeSuite(TestOutputGenerator))
    test_suite.addTest(unittest.makeSuite(TestSchemas))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
