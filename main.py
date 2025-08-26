from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from rule_based_evals import eval_dash_count 
from llm_based_evals import llm_judge
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL"),
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Base prompt
base_prompt = """
You are a LinkedIn ghostwriter. Turn raw notes into professional, concise, and engaging LinkedIn posts. Use my tone: friendly, reflective, and slightly informal. Incorporate specific examples, personal anecdotes, or relatable stories from my experiences (e.g., software engineering, aspiring AI work, neurophysiology, or everyday life with family) to make abstract ideas tangible and actionable. Avoid being vague—ground insights in real experiences that the audience can connect with. 

Before writing each post, pick **one of these post styles** and stick to it consistently: 
1) Personal Story / Lesson Learned
2) Insights / Tips / How-To
3) Reflections / Opinions
4) Questions / Polls
5) Case Studies / Results

Do not mix multiple styles in the same post. Posts should encourage reflection and offer relatable lessons or practical insights without resorting to clichés, overly polished "universal truths," or generic motivational phrases. Write in a natural, conversational style—if it doesn’t sound like me explaining it to a friend, rewrite it. Wherever possible, bring concepts to life by using a story-first approach. Frame ideas through firsthand experiences or specific moments, allowing the story to naturally reveal its takeaway without forcing “the moral.” Don’t over-explain connections; trust the audience to follow the narrative and draw their own meaning.

Raw notes:
{raw_notes}
"""

# Function to generate a post with optional feedback
def ghostwriter(raw_notes: str, feedback: str = "") -> str:
    prompt_text = base_prompt
    if feedback:
        prompt_text += f"\n\nFeedback from previous attempt:\n{feedback}"
    prompt = ChatPromptTemplate.from_template(prompt_text)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"raw_notes": raw_notes})

# List of evaluation functions
evals = [eval_dash_count, llm_judge]  # you can add more eval functions here

# Helper: run all evals on a post and collect failing feedback
def run_evals(post: str):
    feedback_list = []
    passed_all = True
    for eval_fn in evals:
        result = eval_fn(post)
        if not result.get("passed", False):
            passed_all = False
            # generic feedback using all keys except "passed"
            details = ", ".join(f"{k}={v}" for k, v in result.items() if k != "passed")
            feedback_list.append(f"{eval_fn.__name__} failed: {details}")
    return passed_all, "\n".join(feedback_list)

# Main loop
if __name__ == "__main__":
    raw = "I learned about eval-driven development for AI apps. Automating evaluations helps scale prompt improvements faster."
    max_iterations = 5
    iteration = 0
    feedback = ""

    while iteration < max_iterations:
        post = ghostwriter(raw, feedback)
        passed, feedback = run_evals(post)

        print(f"\nIteration {iteration+1}:\n{post}")
        print("Feedback / Eval result:\n", feedback if not passed else "✅ All evals passed!")

        if passed:
            break

        iteration += 1
    else:
        print("\n⚠️ Max iterations reached. Post may still not pass all evals.")