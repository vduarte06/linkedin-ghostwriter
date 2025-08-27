"""Core LinkedIn Ghostwriter functionality."""

from typing import List, Tuple, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
# Removed LLMChain import - using modern RunnableSequence instead

from ..core.config import Config
from ..evaluations.base import BaseEvaluator
from ..prompts.templates import get_base_prompt


class LinkedInGhostwriter:
    """Main class for LinkedIn post generation with evaluation-driven development."""
    
    def __init__(self, evaluators: Optional[List[BaseEvaluator]] = None):
        """Initialize the ghostwriter with optional evaluators."""
        Config.validate()
        
        self.llm = ChatOpenAI(**Config.get_openai_config())
        self.evaluators = evaluators or []
        self.base_prompt = get_base_prompt()
        
    def add_evaluator(self, evaluator: BaseEvaluator) -> None:
        """Add an evaluator to the list."""
        self.evaluators.append(evaluator)
    
    def generate_post(self, raw_notes: str, feedback: str = "") -> str:
        """Generate a LinkedIn post from raw notes with optional feedback."""
        prompt_text = self.base_prompt
        if feedback:
            prompt_text += f"\n\nFeedback from previous attempt:\n{feedback}"
            
        prompt = ChatPromptTemplate.from_template(prompt_text)
        # Use modern RunnableSequence instead of deprecated LLMChain
        chain = prompt | self.llm
        result = chain.invoke({"raw_notes": raw_notes})
        # Extract text content from the response
        return result.content
    
    def run_evaluations(self, post: str) -> Tuple[bool, str]:
        """Run all evaluations on a post and return results."""
        if not self.evaluators:
            return True, "No evaluators configured"
            
        feedback_list = []
        passed_all = True
        
        for evaluator in self.evaluators:
            result = evaluator.evaluate(post)
            if not result.get("passed", False):
                passed_all = False
                details = ", ".join(f"{k}={v}" for k, v in result.items() if k != "passed")
                feedback_list.append(f"{evaluator.__class__.__name__} failed: {details}")
        
        return passed_all, "\n".join(feedback_list)
    
    def generate_with_evaluation(
        self, 
        raw_notes: str, 
        max_iterations: Optional[int] = None
    ) -> Tuple[str, int, bool]:
        """
        Generate a post with iterative evaluation and improvement.
        
        Returns:
            Tuple of (final_post, iterations_used, evaluation_passed)
        """
        max_iterations = max_iterations or Config.MAX_ITERATIONS
        iteration = 0
        feedback = ""
        
        while iteration < max_iterations:
            post = self.generate_post(raw_notes, feedback)
            passed, feedback = self.run_evaluations(post)
            
            if passed:
                return post, iteration + 1, True
                
            iteration += 1
        
        # Return the last generated post even if it didn't pass all evaluations
        return post, max_iterations, False
