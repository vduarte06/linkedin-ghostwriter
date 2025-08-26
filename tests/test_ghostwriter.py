"""Tests for the LinkedInGhostwriter class."""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from linkedin_ghostwriter.core.ghostwriter import LinkedInGhostwriter
from linkedin_ghostwriter.evaluations.base import BaseEvaluator


class MockEvaluator(BaseEvaluator):
    """Mock evaluator for testing."""
    
    def __init__(self, should_pass: bool = True):
        self.should_pass = should_pass
    
    def evaluate(self, post: str):
        return {"passed": self.should_pass, "feedback": "Mock feedback"}


class TestLinkedInGhostwriter:
    """Test cases for LinkedInGhostwriter."""
    
    @patch('linkedin_ghostwriter.core.config.Config.validate')
    @patch('linkedin_ghostwriter.core.config.Config.get_openai_config')
    def test_initialization(self, mock_config, mock_validate):
        """Test ghostwriter initialization."""
        mock_config.return_value = {"api_key": "test", "model": "test", "temperature": 0.7}
        mock_validate.return_value = True
        
        ghostwriter = LinkedInGhostwriter()
        assert ghostwriter.evaluators == []
        assert ghostwriter.base_prompt is not None
    
    def test_add_evaluator(self):
        """Test adding evaluators."""
        with patch('linkedin_ghostwriter.core.config.Config.validate') as mock_validate:
            mock_validate.return_value = True
            with patch('linkedin_ghostwriter.core.config.Config.get_openai_config') as mock_config:
                mock_config.return_value = {"api_key": "test", "model": "test", "temperature": 0.7}
                
                ghostwriter = LinkedInGhostwriter()
                evaluator = MockEvaluator()
                
                ghostwriter.add_evaluator(evaluator)
                assert len(ghostwriter.evaluators) == 1
                assert ghostwriter.evaluators[0] == evaluator
    
    def test_run_evaluations_no_evaluators(self):
        """Test running evaluations with no evaluators."""
        with patch('linkedin_ghostwriter.core.config.Config.validate') as mock_validate:
            mock_validate.return_value = True
            with patch('linkedin_ghostwriter.core.config.Config.get_openai_config') as mock_config:
                mock_config.return_value = {"api_key": "test", "model": "test", "temperature": 0.7}
                
                ghostwriter = LinkedInGhostwriter()
                passed, feedback = ghostwriter.run_evaluations("test post")
                
                assert passed is True
                assert "No evaluators configured" in feedback
    
    def test_run_evaluations_with_evaluators(self):
        """Test running evaluations with evaluators."""
        with patch('linkedin_ghostwriter.core.config.Config.validate') as mock_validate:
            mock_validate.return_value = True
            with patch('linkedin_ghostwriter.core.config.Config.get_openai_config') as mock_config:
                mock_config.return_value = {"api_key": "test", "model": "test", "temperature": 0.7}
                
                ghostwriter = LinkedInGhostwriter()
                evaluator1 = MockEvaluator(should_pass=True)
                evaluator2 = MockEvaluator(should_pass=False)
                
                ghostwriter.add_evaluator(evaluator1)
                ghostwriter.add_evaluator(evaluator2)
                
                passed, feedback = ghostwriter.run_evaluations("test post")
                
                assert passed is False
                assert "MockEvaluator failed" in feedback
