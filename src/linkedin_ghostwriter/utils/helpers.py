"""Helper utility functions for LinkedIn Ghostwriter."""

import re
from typing import List, Dict, Any


def clean_text(text: str) -> str:
    """Clean and normalize text input."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text."""
    hashtags = re.findall(r'#\w+', text)
    return hashtags


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def format_post_stats(post: str) -> Dict[str, Any]:
    """Get statistics about a LinkedIn post."""
    return {
        "word_count": count_words(post),
        "character_count": len(post),
        "hashtag_count": len(extract_hashtags(post)),
        "line_count": len(post.splitlines())
    }
