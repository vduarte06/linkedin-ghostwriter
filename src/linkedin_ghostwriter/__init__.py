"""
LinkedIn Ghostwriter - AI-powered LinkedIn post generation with evaluation-driven development.
"""

from .core.ghostwriter import LinkedInGhostwriter
from .evaluations.rule_based import DashCountEvaluator
from .evaluations.llm_based import LLMJudgeEvaluator, CorporateJargonJudgeEvaluator, StyleEvaluator

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = [
    "LinkedInGhostwriter",
    "DashCountEvaluator", 
    "LLMJudgeEvaluator",
    "CorporateJargonJudgeEvaluator",
    "StyleEvaluator",
]
