"""
JSON Schemas for USB PD Specification parsing system.
Defines the structure for ToC entries and document sections.
"""

TOC_SCHEMA = {
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
    "required": ["doc_title", "section_id", "title", "page", "level", "parent_id", "full_path"],
    "additionalProperties": False
}

SECTION_SCHEMA = {
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
    "required": ["doc_title", "section_id", "title", "page", "level", "parent_id", "full_path"],
    "additionalProperties": False
}

METADATA_SCHEMA = {
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
    "required": ["doc_title", "total_pages", "total_sections", "parsing_timestamp"],
    "additionalProperties": False
}
