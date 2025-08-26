"""Basic usage example for LinkedIn Ghostwriter."""

from src.linkedin_ghostwriter import LinkedInGhostwriter, DashCountEvaluator, LLMJudgeEvaluator


def main():
    """Demonstrate basic usage of the LinkedIn Ghostwriter."""
    
    # Initialize evaluators
    dash_evaluator = DashCountEvaluator(max_allowed=3)
    llm_evaluator = LLMJudgeEvaluator()
    
    # Create ghostwriter with evaluators
    ghostwriter = LinkedInGhostwriter([dash_evaluator, llm_evaluator])
    
    # Example raw notes
    raw_notes = """
    I learned about eval-driven development for AI apps. 
    Automating evaluations helps scale prompt improvements faster.
    """
    
    print("🎯 Generating LinkedIn post with evaluation...")
    print(f"Raw notes: {raw_notes.strip()}")
    print("-" * 50)
    
    # Generate post with evaluation
    final_post, iterations, passed = ghostwriter.generate_with_evaluation(raw_notes)
    
    print(f"\n📝 Final Post (Iteration {iterations}):")
    print(final_post)
    print("-" * 50)
    
    if passed:
        print("✅ All evaluations passed!")
    else:
        print("⚠️ Some evaluations failed, but max iterations reached.")
    
    # Show post statistics
    from src.linkedin_ghostwriter.utils.helpers import format_post_stats
    stats = format_post_stats(final_post)
    print(f"\n📊 Post Statistics:")
    print(f"Words: {stats['word_count']}")
    print(f"Characters: {stats['character_count']}")
    print(f"Lines: {stats['line_count']}")


if __name__ == "__main__":
    main()
