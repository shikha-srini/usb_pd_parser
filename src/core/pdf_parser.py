"""
Core PDF Parser for USB PD Specification documents.
Handles text extraction, ToC identification, and section parsing.
"""

import re
import logging
import pdfplumber
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import os
from ..config import SECTION_PATTERNS, TOC_INDICATORS, USB_PD_TERMS, TAG_CATEGORIES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class USBPDParser:
    """Main parser class for USB PD specification documents."""
    
    def __init__(self, pdf_path: str):
        """Initialize parser with PDF file path."""
        self.pdf_path = pdf_path
        self.pdf = None
        self.doc_title = "USB Power Delivery Specification"
        self.toc_entries = []
        self.sections = []
        self.metadata = {}
        
        # Regex patterns for section identification
        self.section_patterns = SECTION_PATTERNS
        
        # Common words that indicate ToC entries
        self.toc_indicators = TOC_INDICATORS
    
    def open_pdf(self) -> bool:
        """Open and validate PDF file."""
        try:
            if not os.path.exists(self.pdf_path):
                logger.error(f"PDF file not found: {self.pdf_path}")
                return False
            
            self.pdf = pdfplumber.open(self.pdf_path)
            logger.info(f"Successfully opened PDF with {len(self.pdf.pages)} pages")
            return True
            
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            return False
    
    def extract_document_title(self) -> str:
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
                        if any(keyword in line.lower() for keyword in ['usb', 'power delivery', 'specification']):
                            self.doc_title = line.strip()
                            logger.info(f"Extracted document title: {self.doc_title}")
                            return self.doc_title
            
            logger.warning("Could not extract document title, using default")
            return self.doc_title
            
        except Exception as e:
            logger.error(f"Error extracting document title: {e}")
            return self.doc_title
    
    def identify_toc_pages(self) -> List[int]:
        """Identify pages that likely contain the Table of Contents."""
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
                    logger.info(f"Potential ToC page found: {page_num + 1}")
                
                # Check for numbered section patterns
                lines = text.split('\n')
                numbered_lines = 0
                for line in lines:
                    if re.match(r'^\d+\.', line.strip()):
                        numbered_lines += 1
                
                # If more than 3 numbered lines, likely ToC
                if numbered_lines > 3:
                    toc_pages.append(page_num)
                    logger.info(f"ToC candidate page (numbered sections): {page_num + 1}")
            
            # Remove duplicates and sort
            toc_pages = sorted(list(set(toc_pages)))
            logger.info(f"Identified {len(toc_pages)} potential ToC pages: {[p+1 for p in toc_pages]}")
            
            return toc_pages
            
        except Exception as e:
            logger.error(f"Error identifying ToC pages: {e}")
            return []
    
    def extract_toc_entries(self) -> List[Dict]:
        """Extract Table of Contents entries from identified pages."""
        toc_pages = self.identify_toc_pages()
        entries = []
        
        try:
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
            
            # Sort entries by section_id
            entries.sort(key=lambda x: self._section_id_to_tuple(x['section_id']))
            
            # Build parent-child relationships
            self._build_hierarchy(entries)
            
            logger.info(f"Extracted {len(entries)} ToC entries")
            self.toc_entries = entries
            return entries
            
        except Exception as e:
            logger.error(f"Error extracting ToC entries: {e}")
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
                            'doc_title': self.doc_title,
                            'section_id': section_id,
                            'title': title,
                            'page': page,
                            'level': level,
                            'parent_id': None,  # Will be set later
                            'full_path': f"{section_id} {title}",
                            'tags': tags
                        }
                        
                        return entry
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing ToC line '{line}': {e}")
            return None
    
    def _section_id_to_tuple(self, section_id: str) -> Tuple[int, ...]:
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
        usb_terms = USB_PD_TERMS
        
        for term in usb_terms:
            if term in title_lower:
                tags.append(term)
        
        # Add level-specific tags
        if 'overview' in title_lower or 'introduction' in title_lower:
            tags.append('overview')
        elif 'requirements' in title_lower:
            tags.append('requirements')
        elif 'implementation' in title_lower:
            tags.append('implementation')
        
        return tags
    
    def extract_sections(self) -> List[Dict]:
        """Extract all document sections based on ToC entries."""
        if not self.toc_entries:
            logger.error("No ToC entries available. Run extract_toc_entries() first.")
            return []
        
        sections = []
        
        try:
            for i, toc_entry in enumerate(self.toc_entries):
                section = toc_entry.copy()
                
                # Add section-specific fields
                section['content_start'] = toc_entry['page']
                
                # Determine content end (next section's start - 1)
                if i + 1 < len(self.toc_entries):
                    section['content_end'] = self.toc_entries[i + 1]['page'] - 1
                else:
                    section['content_end'] = None
                
                # Analyze section content
                content_analysis = self._analyze_section_content(section)
                section.update(content_analysis)
                
                sections.append(section)
            
            logger.info(f"Extracted {len(sections)} sections")
            self.sections = sections
            return sections
            
        except Exception as e:
            logger.error(f"Error extracting sections: {e}")
            return []
    
    def _analyze_section_content(self, section: Dict) -> Dict:
        """Analyze section content for tables, figures, and word count."""
        try:
            start_page = section['content_start']
            end_page = section['content_end'] or start_page
            
            has_tables = False
            has_figures = False
            word_count = 0
            
            # Analyze pages in section
            for page_num in range(start_page - 1, min(end_page, len(self.pdf.pages))):
                if page_num < 0 or page_num >= len(self.pdf.pages):
                    continue
                
                page = self.pdf.pages[page_num]
                
                # Check for tables
                if page.find_tables():
                    has_tables = True
                
                # Check for figures (simplified - look for figure references)
                text = page.extract_text()
                if re.search(r'figure\s+\d+', text, re.IGNORECASE):
                    has_figures = True
                
                # Count words
                word_count += len(text.split())
            
            return {
                'has_tables': has_tables,
                'has_figures': has_figures,
                'word_count': word_count
            }
            
        except Exception as e:
            logger.error(f"Error analyzing section content: {e}")
            return {
                'has_tables': False,
                'has_figures': False,
                'word_count': 0
            }
    
    def generate_metadata(self) -> Dict:
        """Generate document metadata and statistics."""
        try:
            metadata = {
                'doc_title': self.doc_title,
                'total_pages': len(self.pdf.pages),
                'total_sections': len(self.sections),
                'total_tables': sum(1 for s in self.sections if s.get('has_tables', False)),
                'total_figures': sum(1 for s in self.sections if s.get('has_figures', False)),
                'max_level': max((s['level'] for s in self.sections), default=1),
                'parsing_timestamp': datetime.now().isoformat(),
                'pdf_file_size': os.path.getsize(self.pdf_path),
                'parsing_errors': []
            }
            
            self.metadata = metadata
            logger.info(f"Generated metadata: {metadata}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata: {e}")
            return {}
    
    def close(self):
        """Close PDF file."""
        if self.pdf:
            self.pdf.close()
            logger.info("PDF file closed")
