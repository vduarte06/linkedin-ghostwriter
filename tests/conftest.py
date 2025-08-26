"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_post():
    """Sample LinkedIn post for testing."""
    return """
    The other day, I was debugging a script late at night when my 4-year-old came into the office and asked, "Why are you talking to the computer?"

    I laughed, but it made me pause. From her perspective, I wasn't solving a problem — I was having a conversation with a machine.

    And honestly, that's exactly what it felt like. When the code finally worked, it wasn't because I "beat" the computer. It was because I finally understood how to communicate with it properly.

    That moment reminded me that building software is less about brute force and more about empathy: understanding how the system "thinks," where it struggles, and how to meet it halfway.

    If we bring that same mindset to our teams, we don't just improve collaboration — we achieve better cross-functional alignment.
    """


@pytest.fixture
def sample_raw_notes():
    """Sample raw notes for testing."""
    return "I learned about eval-driven development for AI apps. Automating evaluations helps scale prompt improvements faster."
