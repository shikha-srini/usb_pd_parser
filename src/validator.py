"""
Validation Manager Module
Handles validation of output files and data integrity.
"""

import json
import logging
import os
from typing import List, Dict, Tuple
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class ValidationManager:
    """Manages validation of output files and data integrity."""
    
    def __init__(self):
        """Initialize validation manager."""
        self.schemas = self._load_schemas()
    
    def validate_outputs(self, output_dir: str) -> bool:
        """Validate all output files in the directory."""
        try:
            logger.info(f"Validating outputs in: {output_dir}")
            
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
            
            # Validate JSONL files
            toc_valid = self._validate_jsonl_file(
                os.path.join(output_dir, 'usb_pd_toc.jsonl'),
                self.schemas['toc']
            )
            
            spec_valid = self._validate_jsonl_file(
                os.path.join(output_dir, 'usb_pd_spec.jsonl'),
                self.schemas['spec']
            )
            
            metadata_valid = self._validate_jsonl_file(
                os.path.join(output_dir, 'usb_pd_metadata.jsonl'),
                self.schemas['metadata']
            )
            
            # All validations must pass
            all_valid = toc_valid and spec_valid and metadata_valid
            
            if all_valid:
                logger.info("All output files validated successfully")
            else:
                logger.warning("Some output files failed validation")
            
            return all_valid
            
        except Exception as e:
            logger.error(f"Error during validation: {e}")
            return False
    
    def _validate_jsonl_file(self, filepath: str, schema: Dict) -> bool:
        """Validate a JSONL file against its schema."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not lines:
                logger.warning(f"Empty file: {filepath}")
                return False
            
            # Validate each line
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    validate(data, schema)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON at line {line_num} in {filepath}: {e}")
                    return False
                except ValidationError as e:
                    logger.error(f"Schema validation failed at line {line_num} in {filepath}: {e}")
                    return False
            
            logger.info(f"Validated {filepath}: {len(lines)} lines")
            return True
            
        except Exception as e:
            logger.error(f"Error validating {filepath}: {e}")
            return False
    
    def _load_schemas(self) -> Dict[str, Dict]:
        """Load JSON schemas for validation."""
        return {
            'toc': {
                "type": "object",
                "properties": {
                    "doc_title": {"type": "string"},
                    "section_id": {"type": "string", "pattern": r"^\d+(\.\d+)*$"},
                    "title": {"type": "string", "minLength": 1},
                    "page": {"type": "integer", "minimum": 1},
                    "level": {"type": "integer", "minimum": 1, "maximum": 5},
                    "parent_id": {"type": ["string", "null"]},
                    "full_path": {"type": "string", "minLength": 1},
                    "tags": {"type": "array", "items": {"type": "string"}}
                },
                "required": [
                    "doc_title", "section_id", "title", "page", 
                    "level", "parent_id", "full_path"
                ],
                "additionalProperties": False
            },
            
            'spec': {
                "type": "object",
                "properties": {
                    "doc_title": {"type": "string"},
                    "section_id": {"type": "string", "pattern": r"^\d+(\.\d+)*$"},
                    "title": {"type": "string", "minLength": 1},
                    "page": {"type": "integer", "minimum": 1},
                    "level": {"type": "integer", "minimum": 1, "maximum": 5},
                    "parent_id": {"type": ["string", "null"]},
                    "full_path": {"type": "string", "minLength": 1},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "content_start": {"type": "integer", "minimum": 1},
                    "content_end": {"type": ["integer", "null"]},
                    "has_tables": {"type": "boolean"},
                    "has_figures": {"type": "boolean"},
                    "word_count": {"type": "integer", "minimum": 0}
                },
                "required": [
                    "doc_title", "section_id", "title", "page", 
                    "level", "parent_id", "full_path"
                ],
                "additionalProperties": False
            },
            
            'metadata': {
                "type": "object",
                "properties": {
                    "doc_title": {"type": "string"},
                    "total_pages": {"type": "integer", "minimum": 1},
                    "total_sections": {"type": "integer", "minimum": 0},
                    "total_tables": {"type": "integer", "minimum": 0},
                    "total_figures": {"type": "integer", "minimum": 0},
                    "max_level": {"type": "integer", "minimum": 1},
                    "parsing_timestamp": {"type": "string", "format": "date-time"},
                    "pdf_file_size": {"type": "integer", "minimum": 0},
                    "parsing_errors": {"type": "array", "items": {"type": "string"}}
                },
                "required": [
                    "doc_title", "total_pages", "total_sections", "parsing_timestamp"
                ],
                "additionalProperties": False
            }
        }
    
    def validate_data_integrity(self, toc_entries: List[Dict], 
                               sections: List[Dict]) -> Tuple[bool, List[str]]:
        """Validate data integrity between ToC and sections."""
        errors = []
        
        try:
            # Check if all ToC entries have corresponding sections
            toc_ids = {entry['section_id'] for entry in toc_entries}
            section_ids = {section['section_id'] for section in sections}
            
            missing_sections = toc_ids - section_ids
            extra_sections = section_ids - toc_ids
            
            if missing_sections:
                errors.append(f"Missing sections for ToC entries: {missing_sections}")
            
            if extra_sections:
                errors.append(f"Extra sections not in ToC: {extra_sections}")
            
            # Check page consistency
            for toc_entry in toc_entries:
                section = next(
                    (s for s in sections if s['section_id'] == toc_entry['section_id']), 
                    None
                )
                
                if section and toc_entry['page'] != section['page']:
                    errors.append(
                        f"Page mismatch for {toc_entry['section_id']}: "
                        f"ToC={toc_entry['page']}, Section={section['page']}"
                    )
            
            # Check hierarchy consistency
            for entry in toc_entries:
                if entry['parent_id']:
                    parent_exists = any(
                        e['section_id'] == entry['parent_id'] for e in toc_entries
                    )
                    if not parent_exists:
                        errors.append(
                            f"Parent {entry['parent_id']} not found for {entry['section_id']}"
                        )
            
            is_valid = len(errors) == 0
            
            if is_valid:
                logger.info("Data integrity validation passed")
            else:
                logger.warning(f"Data integrity validation failed: {len(errors)} errors")
            
            return is_valid, errors
            
        except Exception as e:
            logger.error(f"Error during data integrity validation: {e}")
            errors.append(f"Validation error: {e}")
            return False, errors

