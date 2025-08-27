"""Rule-based evaluators for LinkedIn posts."""

import re
from typing import Dict, Any, Optional
from .base import BaseEvaluator
from ..core.config import Config


class DashCountEvaluator(BaseEvaluator):
    """Evaluator that checks for excessive use of dashes in posts."""
    
    def __init__(self, max_allowed: Optional[int] = None):
        """Initialize the evaluator with maximum allowed dashes."""
        self.max_allowed = max_allowed or Config.MAX_DASHES_ALLOWED
    
    def evaluate(self, post: str) -> Dict[str, Any]:
        """
        Count standalone hyphens not at start of line (avoid list bullets).
        
        Args:
            post: The post text to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        # Count standalone hyphens and em dashes not at start of line (avoid list bullets)
        # Match both regular hyphens (-) and em dashes (—) with optional spaces around them
        # This catches: "word - word", "word—word", "word — word", etc.
        matches = re.findall(r'(?<!^)\s*[-—]\s*', post)
        dash_count = len(matches)
        
        return {
            "passed": dash_count <= self.max_allowed,
            "dash_count": dash_count,
            "max_allowed": self.max_allowed,
            "evaluator_type": "rule_based"
        }
