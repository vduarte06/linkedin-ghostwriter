# LinkedIn Ghostwriter

An AI-powered LinkedIn post generator with evaluation-driven development for creating engaging, authentic content.

## 🚀 Features

- **AI-Powered Generation**: Uses OpenAI's language models to transform raw notes into professional LinkedIn posts
- **Evaluation-Driven Development**: Multiple evaluators ensure post quality and style consistency
- **Iterative Improvement**: Automatically refines posts based on evaluation feedback
- **Customizable Style**: Supports multiple post styles (Personal Story, Insights, Reflections, Questions, Case Studies)
- **Rule-Based & AI Evaluations**: Combines simple rules with sophisticated AI judgment

## 📁 Project Structure

```
linkedin-ghostwriter/
├── src/linkedin_ghostwriter/     # Main package source
│   ├── core/                     # Core functionality
│   ├── evaluations/              # Post evaluation modules
│   ├── prompts/                  # Prompt templates
│   └── utils/                    # Utility functions
├── examples/                     # Usage examples
├── tests/                        # Test suite
├── scripts/                      # Command-line tools
└── docs/                         # Documentation
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd linkedin-ghostwriter
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key
   ```

## 🔧 Configuration

Create a `.env` file with your OpenAI credentials:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o
```

## 📖 Usage

### Basic Usage

```python
from src.linkedin_ghostwriter import LinkedInGhostwriter, DashCountEvaluator, LLMJudgeEvaluator

# Initialize evaluators
dash_evaluator = DashCountEvaluator(max_allowed=3)
llm_evaluator = LLMJudgeEvaluator()

# Create ghostwriter
ghostwriter = LinkedInGhostwriter([dash_evaluator, llm_evaluator])

# Generate a post
raw_notes = "I learned about eval-driven development for AI apps..."
final_post, iterations, passed = ghostwriter.generate_with_evaluation(raw_notes)

print(f"Generated in {iterations} iterations: {final_post}")
```

### Command Line Interface

The unified CLI provides multiple modes of operation:

#### **Main Interactive Workflow**
```bash
python main.py main
```
Generates LinkedIn posts from raw notes with full evaluation and iteration.

#### **Test Individual Evaluators**
```bash
# Test LLM judge with custom text
python main.py test-judge --text "Your post text here"

# Test corporate jargon judge with custom text
python main.py test-jargon --text "Your post text here"

# Test dash evaluator with custom text
python main.py dash --text "Your post text here"

# Test with custom parameters
python main.py test-judge --text "..." --model gpt-4o --temperature 0.1

# Test from file with pretty output
python main.py test-judge --file post.txt --pretty
```

#### **CLI Options**
- `test-judge`: Test the general LLM judge evaluator
- `test-jargon`: Test the corporate jargon LLM judge evaluator
- `dash`: Test the dash count evaluator
- `--text`: Provide text directly (use quotes for multi-word text)
- `--file`: Read text from a file
- `--model`: Override LLM model (for LLM judges)
- `--temperature`: Set LLM temperature (for LLM judges, default: 0.0)
- `--max-dashes`: Set maximum allowed dashes (for dash evaluator, default: 3)
- `--pretty`: Pretty-print JSON output

### Examples

Check out the examples in the `examples/` directory for more detailed usage patterns.

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

## 🔍 Evaluators

### Rule-Based Evaluators

- **DashCountEvaluator**: Ensures posts don't overuse dashes (configurable limit)

### AI-Based Evaluators

- **LLMJudgeEvaluator**: Uses AI to evaluate post quality based on:
  - Tone & Voice (friendly, reflective, informal)
  - Style (no corporate jargon, clichés)
  - Storytelling (personal anecdotes, balanced insights)
  - Authenticity (personal voice, human-like)

## 🏗️ Architecture

The project follows a modular, extensible architecture:

- **Core Module**: Main ghostwriter logic and configuration
- **Evaluation System**: Pluggable evaluators with a common interface
- **Prompt Management**: Centralized prompt templates
- **Utility Functions**: Helper functions for text processing and analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/) for LLM orchestration
- Powered by OpenAI's language models
- Inspired by evaluation-driven development practices