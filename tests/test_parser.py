"""
Test cases for USB PD Parser
Tests the new OOP structure with proper naming conventions.
"""

import unittest
import tempfile
import os
import json
from src.parser import PDFParser
from src.output import OutputManager
from src.validator import ValidationManager


class TestPDFParser(unittest.TestCase):
    """Test cases for PDF Parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = PDFParser()
    
    def test_parser_initialization(self):
        """Test PDF parser initialization."""
        self.assertIsNotNone(self.parser)
        self.assertEqual(self.parser.doc_title, "USB Power Delivery Specification")
        self.assertEqual(len(self.parser.section_patterns), 3)
        self.assertEqual(len(self.parser.toc_indicators), 9)
    
    def test_section_id_to_tuple(self):
        """Test section ID to tuple conversion."""
        result = self.parser._section_id_to_tuple("2.1.3")
        self.assertEqual(result, (2, 1, 3))
        
        result = self.parser._section_id_to_tuple("5")
        self.assertEqual(result, (5,))
        
        result = self.parser._section_id_to_tuple("invalid")
        self.assertEqual(result, (0,))
    
    def test_generate_tags(self):
        """Test tag generation for different titles."""
        tags = self.parser._generate_tags("Power Delivery Contract Negotiation")
        self.assertIn("power", tags)
        self.assertIn("delivery", tags)
        self.assertIn("contract", tags)
        self.assertIn("negotiation", tags)
        
        tags = self.parser._generate_tags("Overview and Introduction")
        self.assertIn("overview", tags)
        self.assertIn("introduction", tags)
        
        tags = self.parser._generate_tags("Implementation Requirements")
        self.assertIn("implementation", tags)
        self.assertIn("requirements", tags)
    
    def test_build_hierarchy(self):
        """Test hierarchy building."""
        entries = [
            {'section_id': '2', 'parent_id': None},
            {'section_id': '2.1', 'parent_id': None},
            {'section_id': '2.1.1', 'parent_id': None}
        ]
        
        self.parser._build_hierarchy(entries)
        
        self.assertIsNone(entries[0]['parent_id'])  # Level 1
        self.assertEqual(entries[1]['parent_id'], '2')  # Level 2
        self.assertEqual(entries[2]['parent_id'], '2.1')  # Level 3


class TestOutputManager(unittest.TestCase):
    """Test cases for Output Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_manager = OutputManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_output_directory_creation(self):
        """Test output directory creation."""
        self.assertTrue(os.path.exists(self.temp_dir))
    
    def test_toc_file_generation(self):
        """Test ToC file generation."""
        toc_entries = [
            {
                'section_id': '2',
                'title': 'Overview',
                'page': 53,
                'level': 1,
                'parent_id': None,
                'tags': []
            }
        ]
        
        result = self.output_manager.generate_toc_file(toc_entries, "Test Doc")
        self.assertTrue(os.path.exists(result))
        
        # Check file content
        with open(result, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            
            data = json.loads(lines[0])
            self.assertEqual(data['doc_title'], "Test Doc")
            self.assertEqual(data['section_id'], "2")
            self.assertEqual(data['title'], "Overview")
    
    def test_spec_file_generation(self):
        """Test spec file generation."""
        sections = [
            {
                'section_id': '2',
                'title': 'Overview',
                'page': 53,
                'level': 1,
                'parent_id': None,
                'tags': [],
                'content_start': 53,
                'content_end': 54,
                'has_tables': False,
                'has_figures': False,
                'word_count': 150
            }
        ]
        
        result = self.output_manager.generate_spec_file(sections, "Test Doc")
        self.assertTrue(os.path.exists(result))
        
        # Check file content
        with open(result, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            
            data = json.loads(lines[0])
            self.assertEqual(data['doc_title'], "Test Doc")
            self.assertEqual(data['section_id'], "2")
            self.assertEqual(data['word_count'], 150)


class TestValidationManager(unittest.TestCase):
    """Test cases for Validation Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = ValidationManager()
    
    def test_schema_loading(self):
        """Test schema loading."""
        self.assertIn('toc', self.validator.schemas)
        self.assertIn('spec', self.validator.schemas)
        self.assertIn('metadata', self.validator.schemas)
        
        # Check required fields
        toc_schema = self.validator.schemas['toc']
        required_fields = toc_schema.get('required', [])
        self.assertIn('doc_title', required_fields)
        self.assertIn('section_id', required_fields)
        self.assertIn('title', required_fields)
    
    def test_data_integrity_validation(self):
        """Test data integrity validation."""
        toc_entries = [
            {'section_id': '2', 'title': 'Overview', 'page': 53, 'parent_id': None}
        ]
        
        sections = [
            {'section_id': '2', 'title': 'Overview', 'page': 53, 'parent_id': None}
        ]
        
        is_valid, errors = self.validator.validate_data_integrity(toc_entries, sections)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_data_integrity_validation_with_mismatch(self):
        """Test data integrity validation with mismatched data."""
        toc_entries = [
            {'section_id': '2', 'title': 'Overview', 'page': 53, 'parent_id': None}
        ]
        
        sections = [
            {'section_id': '2', 'title': 'Overview', 'page': 60, 'parent_id': None}
        ]
        
        is_valid, errors = self.validator.validate_data_integrity(toc_entries, sections)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)


if __name__ == '__main__':
    unittest.main()
