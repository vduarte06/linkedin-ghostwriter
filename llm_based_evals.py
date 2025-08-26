from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
import os
from dotenv import load_dotenv
import json

load_dotenv()

judge_llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0)

prompt = ChatPromptTemplate.from_template("""
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
- Has a personal anecdote (narrative, e.g., “the other day I…”)
- No over-explaining the moral (lesson implied, not spelled out)
- Good balance of story and insight (ties story to a takeaway without dragging)

👤 Authenticity / Voice
- Personal voice visible (“I/me/my experience” vs. faceless advice)
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

class JSONParser(BaseOutputParser):
    def parse(self, message):
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

parser = JSONParser()

def llm_judge(post: str) -> dict:
    result = (prompt | judge_llm).invoke({"post": post})
    return parser.parse(result)

example_post = """
The other day, I was debugging a script late at night when my 4-year-old came into the office and asked, “Why are you talking to the computer?”

I laughed, but it made me pause. From her perspective, I wasn’t solving a problem — I was having a conversation with a machine.

And honestly, that’s exactly what it felt like. When the code finally worked, it wasn’t because I “beat” the computer. It was because I finally understood how to communicate with it properly.

That moment reminded me that building software is less about brute force and more about empathy: understanding how the system “thinks,” where it struggles, and how to meet it halfway.

If we bring that same mindset to our teams, we don’t just improve collaboration — we achieve better cross-functional alignment
"""

if __name__ == "__main__":
    result = llm_judge(example_post)
    print(result)