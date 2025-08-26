"""LLM-based evaluators for LinkedIn posts."""

import json
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from .base import BaseEvaluator
from ..core.config import Config


class JSONParser(BaseOutputParser):
    """Parser for JSON output from LLM evaluators."""
    
    def parse(self, message) -> Dict[str, Any]:
        """Parse the LLM message content into a dictionary."""
        # Extract content if it's an AIMessage
        if hasattr(message, "content"):
            text = message.content
        else:
            text = message
        
        # Remove triple backticks and language tags
        text = text.strip()
        if text.startswith("```") and text.endswith("```"):
            # Remove ```json or ```
            text = "\n".join(text.splitlines()[1:-1])
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"passed": False, "feedback": "Failed to parse judge output."}


class LLMJudgeEvaluator(BaseEvaluator):
    """LLM-based evaluator that judges post quality using AI."""
    
    def __init__(self, model: Optional[str] = None, temperature: float = 0):
        """Initialize the LLM judge evaluator."""
        self.model = model or Config.OPENAI_MODEL
        self.temperature = temperature
        self.llm = ChatOpenAI(
            model=self.model, 
            temperature=self.temperature,
            api_key=Config.OPENAI_API_KEY
        )
        self.parser = JSONParser()
        self.prompt = self._create_prompt()
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the evaluation prompt template."""
        return ChatPromptTemplate.from_template("""
    You are a LinkedIn post evaluator.  
Evaluate the following post strictly according to these criteria:

🎭 Tone & Voice
- Friendly but not forced (human talking to a peer, not a press release)
- Reflective (shows personal thinking/learning, not just info-dumping)
- Slightly informal (uses contractions, conversational phrasing, "I/me" usage)

✍️ Style
- Not overly formal (avoid academic/report tone)
- No corporate jargon. Treat **any phrase that sounds like corporate-speak** as a failure, even if it occurs once. Do not ignore subtle phrases. Do not require a list; rely on your understanding of typical corporate language.
- No clichés or generic motivational fluff

📖 Storytelling
- Has a personal anecdote (narrative, e.g., "the other day I…")
- No over-explaining the moral (lesson implied, not spelled out)
- Good balance of story and insight (ties story to a takeaway without dragging)

👤 Authenticity / Voice
- Personal voice visible ("I/me/my experience" vs. faceless advice)
- Not generic AI-sounding (should feel human-written)
- Shows curiosity/openness (ends with reflection/invitation vs. heavy-handed conclusion)

⚠️ Negative Style Flags
- Avoid sterile marketing copy
- Avoid preachy/lecturing tone
- Avoid forced/over-engineered analogies

Post:
{post}

Return JSON with:
- passed: true if the post meets most criteria, false otherwise
- feedback: short explanation of any issues found, including any detected corporate phrases
""")
    
    def evaluate(self, post: str) -> Dict[str, Any]:
        """
        Evaluate a post using the LLM judge.
        
        Args:
            post: The post text to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        result = (self.prompt | self.llm).invoke({"post": post})
        evaluation_result = self.parser.parse(result)
        evaluation_result["evaluator_type"] = "llm_based"
        return evaluation_result
