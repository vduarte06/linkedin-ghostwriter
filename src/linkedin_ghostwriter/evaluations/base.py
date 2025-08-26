"""Base evaluator class for LinkedIn post evaluations."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseEvaluator(ABC):
    """Abstract base class for all post evaluators."""
    
    @abstractmethod
    def evaluate(self, post: str) -> Dict[str, Any]:
        """
        Evaluate a LinkedIn post.
        
        Args:
            post: The post text to evaluate
            
        Returns:
            Dictionary containing evaluation results with at least a 'passed' key
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the evaluator."""
        return self.__class__.__name__
