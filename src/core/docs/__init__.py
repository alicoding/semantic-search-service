#!/usr/bin/env python3
"""
Documentation Domain - Clean Public API
Single Responsibility: Export documentation domain services
"""

from .doc_generator import generate_api_reference
from .language_detector import detect_languages_and_frameworks


# Entry points for backward compatibility
def generate():
    """Main entry point"""
    return generate_api_reference()


def refresh():
    """Refresh documentation"""
    return generate()