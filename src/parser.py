"""
PDF Parser Module
Handles PDF loading, text extraction, and content parsing.
"""

import re
import logging
import pdfplumber
from typing import List, Dict, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class PDFParser:
    """PDF parsing and content extraction class."""
    
    def __init__(self):
        """Initialize the PDF parser."""
        self.pdf = None
        self.pdf_path = None
        self.doc_title = "USB Power Delivery Specification"
        self.toc_entries = []
        self.sections = []
        
        # Section patterns for identification
        self.section_patterns = [
            r'^(\d+(?:\.\d+)*)\s+([^\n]+?)(?:\s+(\d+))?$',  # "2.1.2 Title [page]"
            r'^(\d+(?:\.\d+)*)\s+([^\n]+?)\s+(\d+)$',       # "2.1.2 Title 53"
            r'^(?:Chapter\s+)?(\d+)\s+([^\n]+?)(?:\s+(\d+))?$'  # "Chapter 2 Title"
        ]
        
        # ToC indicators
        self.toc_indicators = [
            'contents', 'table of contents', 'toc', 'index',
            'overview', 'introduction', 'specification',
            'requirements', 'chapters', 'sections'
        ]
    
    def load_pdf(self, pdf_path: str) -> bool:
        """Load and validate PDF file."""
        try:
            if not os.path.exists(pdf_path):
                logger.error(f"PDF file not found: {pdf_path}")
                return False
            
            self.pdf = pdfplumber.open(pdf_path)
            self.pdf_path = pdf_path
            
            logger.info(f"Successfully loaded PDF: {pdf_path}")
            logger.info(f"Total pages: {len(self.pdf.pages)}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            return False
    
    def extract_title(self) -> str:
        """Extract document title from first few pages."""
        try:
            # Check first 3 pages for title
            for page_num in range(min(3, len(self.pdf.pages))):
                page = self.pdf.pages[page_num]
                text = page.extract_text()
                
                # Look for title patterns
                lines = text.split('\n')
                for line in lines[:10]:  # Check first 10 lines
                    line = line.strip()
                    if len(line) > 10 and len(line) < 200:
                        # Check if line contains USB PD related keywords
                        keywords = ['usb', 'power delivery', 'specification']
                        if any(keyword in line.lower() for keyword in keywords):
                            self.doc_title = line.strip()
                            logger.info(f"Extracted title: {self.doc_title}")
                            return self.doc_title
            
            logger.warning("Could not extract title, using default")
            return self.doc_title
            
        except Exception as e:
            logger.error(f"Error extracting title: {e}")
            return self.doc_title
    
    def extract_toc(self) -> List[Dict]:
        """Extract table of contents entries."""
        try:
            toc_pages = self._identify_toc_pages()
            entries = []
            
            for page_num in toc_pages:
                page = self.pdf.pages[page_num]
                text = page.extract_text()
                lines = text.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Try to match section patterns
                    entry = self._parse_toc_line(line, page_num + 1)
                    if entry:
                        entries.append(entry)
            
            # Sort entries and build hierarchy
            entries.sort(key=lambda x: self._section_id_to_tuple(x['section_id']))
            self._build_hierarchy(entries)
            
            self.toc_entries = entries
            logger.info(f"Extracted {len(entries)} ToC entries")
            
            return entries
            
        except Exception as e:
            logger.error(f"Error extracting ToC: {e}")
            return []
    
    def extract_sections(self) -> List[Dict]:
        """Extract document sections based on ToC entries."""
        if not self.toc_entries:
            logger.error("No ToC entries available")
            return []
        
        try:
            sections = []
            
            for i, toc_entry in enumerate(self.toc_entries):
                section = toc_entry.copy()
                
                # Add section-specific fields
                section['content_start'] = toc_entry['page']
                
                # Determine content end (next section's start - 1)
                if i + 1 < len(self.toc_entries):
                    section['content_end'] = self.toc_entries[i + 1]['page'] - 1
                else:
                    section['content_end'] = None
                
                # Add content analysis fields
                section['has_tables'] = self._check_for_tables(section)
                section['has_figures'] = self._check_for_figures(section)
                section['word_count'] = self._estimate_word_count(section)
                
                sections.append(section)
            
            self.sections = sections
            logger.info(f"Extracted {len(sections)} sections")
            
            return sections
            
        except Exception as e:
            logger.error(f"Error extracting sections: {e}")
            return []
    
    def generate_metadata(self) -> Dict:
        """Generate document metadata."""
        try:
            metadata = {
                'doc_title': self.doc_title,
                'total_pages': len(self.pdf.pages) if self.pdf else 0,
                'total_sections': len(self.sections),
                'total_tables': sum(1 for s in self.sections if s.get('has_tables', False)),
                'total_figures': sum(1 for s in self.sections if s.get('has_figures', False)),
                'max_level': max((s.get('level', 1) for s in self.sections), default=1),
                'parsing_timestamp': datetime.now().isoformat(),
                'pdf_file_size': os.path.getsize(self.pdf_path) if self.pdf_path else 0,
                'parsing_errors': []
            }
            
            logger.info("Generated metadata")
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata: {e}")
            return {}
    
    def _identify_toc_pages(self) -> List[int]:
        """Identify pages that likely contain the table of contents."""
        toc_pages = []
        
        try:
            # Check first 20 pages for ToC indicators
            search_pages = min(20, len(self.pdf.pages))
            
            for page_num in range(search_pages):
                page = self.pdf.pages[page_num]
                text = page.extract_text().lower()
                
                # Check for ToC indicators
                if any(indicator in text for indicator in self.toc_indicators):
                    toc_pages.append(page_num)
                    logger.info(f"ToC page found: {page_num + 1}")
                
                # Check for numbered section patterns
                lines = text.split('\n')
                numbered_lines = sum(1 for line in lines if re.match(r'^\d+\.', line.strip()))
                
                # If more than 3 numbered lines, likely ToC
                if numbered_lines > 3:
                    toc_pages.append(page_num)
                    logger.info(f"ToC candidate page: {page_num + 1}")
            
            # Remove duplicates and sort
            toc_pages = sorted(list(set(toc_pages)))
            logger.info(f"Identified {len(toc_pages)} ToC pages")
            
            return toc_pages
            
        except Exception as e:
            logger.error(f"Error identifying ToC pages: {e}")
            return []
    
    def _parse_toc_line(self, line: str, page_num: int) -> Optional[Dict]:
        """Parse a single ToC line into a structured entry."""
        try:
            # Try different patterns
            for pattern in self.section_patterns:
                match = re.match(pattern, line)
                if match:
                    groups = match.groups()
                    
                    if len(groups) >= 2:
                        section_id = groups[0]
                        title = groups[1].strip()
                        
                        # Extract page number if present
                        page = page_num
                        if len(groups) > 2 and groups[2]:
                            try:
                                page = int(groups[2])
                            except ValueError:
                                pass
                        
                        # Determine level from section_id
                        level = section_id.count('.') + 1
                        
                        # Generate tags based on title content
                        tags = self._generate_tags(title)
                        
                        entry = {
                            'section_id': section_id,
                            'title': title,
                            'page': page,
                            'level': level,
                            'parent_id': None,  # Will be set later
                            'tags': tags
                        }
                        
                        return entry
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing ToC line '{line}': {e}")
            return None
    
    def _section_id_to_tuple(self, section_id: str) -> tuple:
        """Convert section_id to tuple for sorting."""
        try:
            return tuple(int(part) for part in section_id.split('.'))
        except ValueError:
            return (0,)
    
    def _build_hierarchy(self, entries: List[Dict]):
        """Build parent-child relationships between sections."""
        for entry in entries:
            section_id = entry['section_id']
            parts = section_id.split('.')
            
            if len(parts) > 1:
                # Find parent by removing last part
                parent_id = '.'.join(parts[:-1])
                
                # Find parent entry
                for potential_parent in entries:
                    if potential_parent['section_id'] == parent_id:
                        entry['parent_id'] = parent_id
                        break
    
    def _generate_tags(self, title: str) -> List[str]:
        """Generate semantic tags from section title."""
        tags = []
        title_lower = title.lower()
        
        # Common USB PD terms
        usb_terms = [
            'usb', 'power', 'delivery', 'specification',
            'overview', 'introduction', 'requirements',
            'implementation', 'contract', 'negotiation'
        ]
        
        for term in usb_terms:
            if term in title_lower:
                tags.append(term)
        
        return tags
    
    def _check_for_tables(self, section: Dict) -> bool:
        """Check if section contains tables."""
        # Simplified check - in real implementation, analyze content
        return 'table' in section.get('title', '').lower()
    
    def _check_for_figures(self, section: Dict) -> bool:
        """Check if section contains figures."""
        # Simplified check - in real implementation, analyze content
        return 'figure' in section.get('title', '').lower()
    
    def _estimate_word_count(self, section: Dict) -> int:
        """Estimate word count for section."""
        # Simplified estimation - in real implementation, count actual words
        title = section.get('title', '')
        return len(title.split()) * 10  # Rough estimate
    
    def close(self):
        """Close the PDF file."""
        if self.pdf:
            self.pdf.close()
            logger.info("PDF file closed")

