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


class LLMJudgeBase(BaseEvaluator):
    """Base class for LLM-based judges with overridable prompt templates."""

    def __init__(self, model: Optional[str] = None, temperature: float = 0):
        self.model = model or Config.OPENAI_MODEL
        self.temperature = temperature
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            api_key=Config.OPENAI_API_KEY,
        )
        self.parser = JSONParser()
        self.prompt = self._create_prompt()

    def _create_prompt(self) -> ChatPromptTemplate:
        """Create and return the ChatPromptTemplate for this judge."""
        raise NotImplementedError

    def evaluate(self, post: str) -> Dict[str, Any]:
        """Evaluate a post using the configured LLM prompt."""
        result = (self.prompt | self.llm).invoke({"post": post})
        evaluation_result = self.parser.parse(result)
        evaluation_result["evaluator_type"] = "llm_based"
        evaluation_result["judge"] = self.__class__.__name__
        return evaluation_result


class CorporateJargonJudgeEvaluator(LLMJudgeBase):
    """Judge that flags corporate jargon and marketing-speak in a post."""

    def _create_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            """
            You are an evaluator that detects corporate jargon and sterile marketing-speak in LinkedIn posts.

            Task: Given the post below, detect phrases that sound like corporate jargon or vague buzzwords
            (e.g., "leverage synergies", "maximize alignment", "drive impact at scale", "unlock value", "solutioning",
            "utilize", "robust framework", "best-in-class", "mission-critical", "stakeholder alignment", etc.).

            Guidelines:
            - If any corporate-speak is present, mark passed=false. Otherwise passed=true.
            - Be strict: even one clear instance should fail the check.
            - Extract up to 10 suspicious phrases with a short explanation each.
            - Keep feedback concise and actionable.

            Post:
            {post}

            Return strict JSON with:
            - passed: boolean
            - phrases: array of strings (suspicious phrases found, empty if none)
            - feedback: short explanation (<= 2 sentences)
            """
        )


class StyleEvaluator(LLMJudgeBase):
    """Specialized evaluator for detecting style complexity and over-explanation issues."""

    def _create_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            """
            You are a LinkedIn post style evaluator focused on detecting complexity and over-explanation.
            
            A post should be considered TOO COMPLEX if it contains one or more of the following:

            1. **Over-explaining**
               - Multiple sentences dedicated to defining or restating the same concept
               - Example: repeating the same idea with multiple analogies or explanations

            2. **Extended analogies or metaphors**
               - More than one analogy to explain the same point
               - Any analogy that takes more than ~2 sentences to explain

            3. **Essay-like structure**
               - Uses long multi-paragraph exposition before reaching the main point
               - Reads like an article or report rather than a quick LinkedIn reflection

            4. **Heavy buildup before personal reflection**
               - Too much time on background before getting to the author's own thought or takeaway
               - Excessive setup phrases like "Ever heard of...", "Here's the gist...", "Imagine you're..."

            5. **Polished, generic-sounding phrasing**
               - Overly polished language that doesn't sound conversational
               - Examples: "Here's the gist," "state-of-the-art," "you're only as strong as your weakest link"

            6. **Too long for the insight given**
               - If the same takeaway could be expressed in <5 sentences but the post is 3+ long paragraphs
               - Verbose writing that doesn't respect the reader's time

            ✅ A good/simple post should:
            - Use short, direct sentences
            - Explain once, briefly, then move on
            - Share a quick personal thought or reflection instead of a long essay
            - Trust the reader to connect the dots (don't spell out every lesson)

            Post to evaluate:
            {post}

            Return strict JSON with:
            - passed: boolean (true if post is simple and direct, false if too complex)
            - feedback: short explanation of complexity issues found
            - failures: ["style"]
            - phrases: array of problematic phrases/examples found (empty if none)
            - suggestions: array of specific simplification suggestions (empty if none)
            """
        )


class LLMJudgeEvaluator(LLMJudgeBase):
    """General-purpose judge (broader criteria). Kept for completeness."""

    def _create_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            """
            You are a LinkedIn post evaluator.
            Evaluate the following post strictly according to these criteria:

            🎭 Tone & Voice
            - Friendly but not forced (human talking to a peer, not a press release)
            - Reflective (shows personal thinking/learning, not just info-dumping)
            - Slightly informal (uses contractions, conversational phrasing, "I/me" usage)

            ✍️ Style
            - Simple and direct tone is required.
            - Reward short, clear sentences that trust the reader to make their own connections.
            - Penalize over-explaining, long analogies, and overly polished "essay-like" style.
            - Not overly formal (avoid academic/report tone)
            - No corporate jargon. Treat any phrase that sounds like corporate-speak as a failure, even if it occurs once.
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

            Return strict JSON with:
            - passed: boolean (true if post meets most criteria, false otherwise)
            - feedback: short explanation of any issues found
            - failures: array of specific failure categories found (e.g., ["cliche", "jargon", "tone", "storytelling", "authenticity", "simplicity"])
            - phrases: array of problematic phrases/examples found (empty if none)
            - suggestions: array of specific improvement suggestions (empty if none)
            """
        )
