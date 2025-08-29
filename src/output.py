"""
Output Manager Module
Handles generation of all output files in different formats.
"""

import json
import logging
import os
import pandas as pd
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class OutputManager:
    """Manages generation of all output files."""
    
    def __init__(self, output_dir: str):
        """Initialize output manager."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory: {output_dir}")
    
    def generate_toc_file(self, toc_entries: List[Dict], doc_title: str) -> str:
        """Generate table of contents JSONL file."""
        try:
            output_file = os.path.join(self.output_dir, "usb_pd_toc.jsonl")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for entry in toc_entries:
                    # Add document title to each entry
                    entry_with_title = {
                        'doc_title': doc_title,
                        'section_id': entry['section_id'],
                        'title': entry['title'],
                        'page': entry['page'],
                        'level': entry['level'],
                        'parent_id': entry['parent_id'],
                        'full_path': f"{entry['section_id']} {entry['title']}",
                        'tags': entry['tags']
                    }
                    
                    f.write(json.dumps(entry_with_title, ensure_ascii=False) + '\n')
            
            logger.info(f"Generated ToC file: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating ToC file: {e}")
            return ""
    
    def generate_spec_file(self, sections: List[Dict], doc_title: str) -> str:
        """Generate specification sections JSONL file."""
        try:
            output_file = os.path.join(self.output_dir, "usb_pd_spec.jsonl")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for section in sections:
                    # Add document title to each section
                    section_with_title = {
                        'doc_title': doc_title,
                        'section_id': section['section_id'],
                        'title': section['title'],
                        'page': section['page'],
                        'level': section['level'],
                        'parent_id': section['parent_id'],
                        'full_path': f"{section['section_id']} {section['title']}",
                        'tags': section['tags'],
                        'content_start': section.get('content_start'),
                        'content_end': section.get('content_end'),
                        'has_tables': section.get('has_tables', False),
                        'has_figures': section.get('has_figures', False),
                        'word_count': section.get('word_count', 0)
                    }
                    
                    f.write(json.dumps(section_with_title, ensure_ascii=False) + '\n')
            
            logger.info(f"Generated spec file: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating spec file: {e}")
            return ""
    
    def generate_metadata_file(self, metadata: Dict) -> str:
        """Generate metadata JSONL file."""
        try:
            output_file = os.path.join(self.output_dir, "usb_pd_metadata.jsonl")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json.dumps(metadata, ensure_ascii=False) + '\n')
            
            logger.info(f"Generated metadata file: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating metadata file: {e}")
            return ""
    
    def generate_validation_report(self, toc_entries: List[Dict], 
                                 sections: List[Dict], metadata: Dict) -> str:
        """Generate Excel validation report."""
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
    
    def _create_validation_data(self, toc_entries: List[Dict], 
                               sections: List[Dict], metadata: Dict) -> Dict:
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
                # Find matching parsed section
                parsed_section = next(
                    (s for s in sections if s['section_id'] == toc_entry['section_id']), 
                    None
                )
                
                comparison.append({
                    'ToC Section ID': toc_entry['section_id'],
                    'ToC Title': toc_entry['title'],
                    'ToC Page': toc_entry['page'],
                    'ToC Level': toc_entry['level'],
                    'Parsed Title': parsed_section['title'] if parsed_section else 'NOT FOUND',
                    'Parsed Page': parsed_section['page'] if parsed_section else 'N/A',
                    'Parsed Level': parsed_section['level'] if parsed_section else 'N/A',
                    'Status': 'MATCH' if parsed_section else 'MISSING',
                    'Page Difference': (
                        parsed_section['page'] - toc_entry['page']
                    ) if parsed_section else 'N/A'
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
                'Sections with Tables': len([
                    s for s in sections if s.get('has_tables', False)
                ]),
                'Sections with Figures': len([
                    s for s in sections if s.get('has_figures', False)
                ]),
                'Average Word Count': (
                    sum(s.get('word_count', 0) for s in sections) / 
                    max(len(sections), 1)
                ),
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

