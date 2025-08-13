"""
Output Generator for USB PD Specification parsing system.
Handles JSONL file creation and Excel validation reports.
"""

import json
import logging
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime
import os
from jsonschema import validate, ValidationError
from ..schemas import TOC_SCHEMA, SECTION_SCHEMA, METADATA_SCHEMA

logger = logging.getLogger(__name__)

class OutputGenerator:
    """Generates structured output files and validation reports."""
    
    def __init__(self, output_dir: str = "output"):
        """Initialize output generator with output directory."""
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Created output directory: {self.output_dir}")
    
    def generate_toc_jsonl(self, toc_entries: List[Dict], doc_title: str) -> str:
        """Generate Table of Contents JSONL file."""
        try:
            output_file = os.path.join(self.output_dir, "usb_pd_toc.jsonl")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for entry in toc_entries:
                    # Validate entry against schema
                    try:
                        validate(entry, TOC_SCHEMA)
                        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    except ValidationError as e:
                        logger.warning(f"Schema validation failed for ToC entry: {e}")
                        # Write entry anyway but log the issue
                        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            logger.info(f"Generated ToC JSONL file: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating ToC JSONL: {e}")
            return ""
    
    def generate_spec_jsonl(self, sections: List[Dict], doc_title: str) -> str:
        """Generate specification sections JSONL file."""
        try:
            output_file = os.path.join(self.output_dir, "usb_pd_spec.jsonl")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for section in sections:
                    # Validate section against schema
                    try:
                        validate(section, SECTION_SCHEMA)
                        f.write(json.dumps(section, ensure_ascii=False) + '\n')
                    except ValidationError as e:
                        logger.warning(f"Schema validation failed for section: {e}")
                        # Write section anyway but log the issue
                        f.write(json.dumps(section, ensure_ascii=False) + '\n')
            
            logger.info(f"Generated spec JSONL file: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating spec JSONL: {e}")
            return ""
    
    def generate_metadata_jsonl(self, metadata: Dict) -> str:
        """Generate metadata JSONL file."""
        try:
            output_file = os.path.join(self.output_dir, "usb_pd_metadata.jsonl")
            
            # Validate metadata against schema
            try:
                validate(metadata, METADATA_SCHEMA)
            except ValidationError as e:
                logger.warning(f"Schema validation failed for metadata: {e}")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(metadata, ensure_ascii=False) + '\n')
            
            logger.info(f"Generated metadata JSONL file: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating metadata JSONL: {e}")
            return ""
    
    def generate_validation_report(self, toc_entries: List[Dict], sections: List[Dict], 
                                 metadata: Dict) -> str:
        """Generate Excel validation report comparing ToC vs parsed content."""
        try:
            output_file = os.path.join(self.output_dir, "validation_report.xlsx")
            
            # Create validation data
            validation_data = self._create_validation_data(toc_entries, sections, metadata)
            
            # Create Excel writer
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Summary sheet
                summary_df = pd.DataFrame([validation_data['summary']])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # ToC vs Parsed comparison
                comparison_df = pd.DataFrame(validation_data['comparison'])
                comparison_df.to_excel(writer, sheet_name='ToC_vs_Parsed', index=False)
                
                # Detailed analysis
                detailed_df = pd.DataFrame(validation_data['detailed'])
                detailed_df.to_excel(writer, sheet_name='Detailed_Analysis', index=False)
                
                # Statistics
                stats_df = pd.DataFrame([validation_data['statistics']])
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)
            
            logger.info(f"Generated validation report: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating validation report: {e}")
            return ""
    
    def _create_validation_data(self, toc_entries: List[Dict], sections: List[Dict], 
                               metadata: Dict) -> Dict:
        """Create validation data for Excel report."""
        try:
            # Summary data
            summary = {
                'Document Title': metadata.get('doc_title', 'Unknown'),
                'Total Pages': metadata.get('total_pages', 0),
                'Total Sections in ToC': len(toc_entries),
                'Total Sections Parsed': len(sections),
                'Total Tables Detected': metadata.get('total_tables', 0),
                'Total Figures Detected': metadata.get('total_figures', 0),
                'Maximum Section Level': metadata.get('max_level', 1),
                'Parsing Timestamp': metadata.get('parsing_timestamp', ''),
                'Validation Status': 'PASS' if len(toc_entries) == len(sections) else 'FAIL'
            }
            
            # Comparison data
            comparison = []
            for toc_entry in toc_entries:
                section_id = toc_entry['section_id']
                
                # Find corresponding parsed section
                parsed_section = next((s for s in sections if s['section_id'] == section_id), None)
                
                comparison.append({
                    'Section ID': section_id,
                    'ToC Title': toc_entry['title'],
                    'ToC Page': toc_entry['page'],
                    'ToC Level': toc_entry['level'],
                    'Parsed Title': parsed_section['title'] if parsed_section else 'NOT FOUND',
                    'Parsed Page': parsed_section['page'] if parsed_section else 'N/A',
                    'Parsed Level': parsed_section['level'] if parsed_section else 'N/A',
                    'Status': 'MATCH' if parsed_section else 'MISSING',
                    'Page Difference': (parsed_section['page'] - toc_entry['page']) if parsed_section else 'N/A'
                })
            
            # Detailed analysis
            detailed = []
            for section in sections:
                detailed.append({
                    'Section ID': section['section_id'],
                    'Title': section['title'],
                    'Level': section['level'],
                    'Page': section['page'],
                    'Parent ID': section.get('parent_id', ''),
                    'Content Start': section.get('content_start', ''),
                    'Content End': section.get('content_end', ''),
                    'Has Tables': section.get('has_tables', False),
                    'Has Figures': section.get('has_figures', False),
                    'Word Count': section.get('word_count', 0),
                    'Tags': ', '.join(section.get('tags', []))
                })
            
            # Statistics
            statistics = {
                'Total Sections': len(sections),
                'Level 1 Sections': len([s for s in sections if s['level'] == 1]),
                'Level 2 Sections': len([s for s in sections if s['level'] == 2]),
                'Level 3 Sections': len([s for s in sections if s['level'] == 3]),
                'Level 4+ Sections': len([s for s in sections if s['level'] >= 4]),
                'Sections with Tables': len([s for s in sections if s.get('has_tables', False)]),
                'Sections with Figures': len([s for s in sections if s.get('has_figures', False)]),
                'Average Word Count': sum(s.get('word_count', 0) for s in sections) / max(len(sections), 1),
                'Total Word Count': sum(s.get('word_count', 0) for s in sections)
            }
            
            return {
                'summary': summary,
                'comparison': comparison,
                'detailed': detailed,
                'statistics': statistics
            }
            
        except Exception as e:
            logger.error(f"Error creating validation data: {e}")
            return {
                'summary': {},
                'comparison': [],
                'detailed': [],
                'statistics': {}
            }
    
    def generate_sample_output(self) -> str:
        """Generate sample JSONL files for demonstration."""
        try:
            sample_dir = os.path.join(self.output_dir, "samples")
            if not os.path.exists(sample_dir):
                os.makedirs(sample_dir)
            
            # Sample ToC entries
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
                }
            ]
            
            # Sample sections
            sample_sections = [
                {
                    "doc_title": "USB Power Delivery Specification Rev X",
                    "section_id": "2",
                    "title": "Overview",
                    "full_path": "2 Overview",
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
            ]
            
            # Sample metadata
            sample_metadata = {
                "doc_title": "USB Power Delivery Specification Rev X",
                "total_pages": 100,
                "total_sections": 3,
                "total_tables": 0,
                "total_figures": 0,
                "max_level": 3,
                "parsing_timestamp": datetime.now().isoformat(),
                "pdf_file_size": 1024000,
                "parsing_errors": []
            }
            
            # Generate sample files
            self.generate_toc_jsonl(sample_toc, "Sample")
            self.generate_spec_jsonl(sample_sections, "Sample")
            self.generate_metadata_jsonl(sample_metadata)
            
            logger.info("Generated sample output files")
            return sample_dir
            
        except Exception as e:
            logger.error(f"Error generating sample output: {e}")
            return ""
