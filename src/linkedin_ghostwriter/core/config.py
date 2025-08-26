"""Configuration management for LinkedIn Ghostwriter."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for LinkedIn Ghostwriter."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Generation Settings
    DEFAULT_TEMPERATURE: float = 0.7
    MAX_ITERATIONS: int = 5
    
    # Evaluation Settings
    MAX_DASHES_ALLOWED: int = 3
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """Get OpenAI configuration as a dictionary."""
        return {
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.OPENAI_MODEL,
            "temperature": cls.DEFAULT_TEMPERATURE
        }
