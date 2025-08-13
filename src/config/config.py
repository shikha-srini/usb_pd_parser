"""
Configuration file for USB PD Specification Parser
Contains configurable settings and parameters.
"""

import os
from typing import List, Dict

# PDF Parsing Configuration
PDF_CONFIG = {
    'max_toc_search_pages': 20,  # Maximum pages to search for ToC
    'min_toc_entries': 3,        # Minimum ToC entries to consider valid
    'max_section_level': 5,       # Maximum section nesting level
    'page_margin_tolerance': 2,   # Page number tolerance for matching
}

# Section Pattern Configuration
SECTION_PATTERNS = [
    # Primary pattern: "2.1.2 Power Delivery Contract Negotiation"
    {
        'regex': r'^(\d+(?:\.\d+)*)\s+([^\n]+?)(?:\s+(\d+))?$',
        'priority': 1,
        'description': 'Standard numbered sections with optional page numbers'
    },
    # Secondary pattern: "2.1.2 Power Delivery Contract Negotiation 53"
    {
        'regex': r'^(\d+(?:\.\d+)*)\s+([^\n]+?)\s+(\d+)$',
        'priority': 2,
        'description': 'Numbered sections with page numbers at end'
    },
    # Tertiary pattern: "Chapter 2 Overview"
    {
        'regex': r'^(?:Chapter\s+)?(\d+)\s+([^\n]+?)(?:\s+(\d+))?$',
        'priority': 3,
        'description': 'Chapter-based sections'
    }
]

# ToC Indicators
TOC_INDICATORS = [
    'contents',
    'table of contents', 
    'toc',
    'index',
    'overview',
    'introduction',
    'specification',
    'requirements',
    'chapters',
    'sections'
]

# USB PD Specific Terms for Tag Generation
USB_PD_TERMS = [
    # Core concepts
    'power', 'delivery', 'contract', 'negotiation', 'communication',
    'protocol', 'state', 'machine', 'voltage', 'current', 'cable',
    
    # Technical terms
    'sop', 'sop\'', 'sop\'\'', 'collision', 'avoidance', 'plug',
    'source', 'sink', 'dual-role', 'pd', 'usb', 'type-c',
    
    # Operational terms
    'operational', 'capability', 'compatibility', 'revision',
    'implementation', 'requirements', 'specification'
]

# Semantic Tag Categories
TAG_CATEGORIES = {
    'overview': ['overview', 'introduction', 'background', 'scope'],
    'requirements': ['requirements', 'specifications', 'standards', 'compliance'],
    'implementation': ['implementation', 'design', 'architecture', 'structure'],
    'protocol': ['protocol', 'communication', 'signaling', 'timing'],
    'hardware': ['hardware', 'cable', 'connector', 'plug', 'port'],
    'software': ['software', 'firmware', 'driver', 'application']
}

# Output Configuration
OUTPUT_CONFIG = {
    'default_output_dir': 'output',
    'file_encodings': 'utf-8',
    'json_indent': None,  # No indentation for JSONL
    'excel_engine': 'openpyxl',
    'validation_report_sheets': [
        'Summary',
        'ToC_vs_Parsed', 
        'Detailed_Analysis',
        'Statistics'
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'usb_pd_parser.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Validation Configuration
VALIDATION_CONFIG = {
    'strict_mode': False,  # Whether to fail on schema validation errors
    'max_validation_errors': 100,  # Maximum errors to report
    'generate_validation_report': True,
    'validate_jsonl_integrity': True,
    'check_page_consistency': True
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'max_pages_per_batch': 50,  # Process pages in batches
    'enable_parallel_processing': False,  # Future enhancement
    'memory_limit_mb': 512,  # Memory usage limit
    'timeout_seconds': 300,  # Processing timeout
}

# Error Handling Configuration
ERROR_CONFIG = {
    'continue_on_parse_error': True,
    'log_all_errors': True,
    'max_retries': 3,
    'graceful_degradation': True
}

def get_config_value(config_dict: Dict, key: str, default=None):
    """Get configuration value with environment variable override support."""
    # Check environment variable first
    env_key = f"USB_PD_PARSER_{key.upper()}"
    env_value = os.getenv(env_key)
    
    if env_value is not None:
        # Try to convert to appropriate type
        try:
            if isinstance(default, bool):
                return env_value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(default, int):
                return int(env_value)
            elif isinstance(default, float):
                return float(env_value)
            elif isinstance(default, list):
                return env_value.split(',')
            else:
                return env_value
        except (ValueError, TypeError):
            pass
    
    # Return config value or default
    return config_dict.get(key, default)

def get_pdf_config(key: str, default=None):
    """Get PDF configuration value."""
    return get_config_value(PDF_CONFIG, key, default)

def get_output_config(key: str, default=None):
    """Get output configuration value."""
    return get_config_value(OUTPUT_CONFIG, key, default)

def get_validation_config(key: str, default=None):
    """Get validation configuration value."""
    return get_config_value(VALIDATION_CONFIG, key, default)

def get_performance_config(key: str, default=None):
    """Get performance configuration value."""
    return get_config_value(PERFORMANCE_CONFIG, key, default)

def get_error_config(key: str, default=None):
    """Get error handling configuration value."""
    return get_config_value(ERROR_CONFIG, key, default)
