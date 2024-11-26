# Spanish Trainer

An interactive Spanish language learning program that generates personalized questions using AI (OpenAI's GPT-4) based on your proficiency level.

## Features

- Interactive command-line interface
- Six proficiency levels (A1 to C2) following CEFR standards
- AI-generated questions tailored to your level
- Question types include vocabulary, conjugation, and grammar
- Immediate feedback and explanations
- Progress tracking
- Fallback questions for offline use

## Setup

1. Install Python 3.8 or higher
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install openai python-dotenv colorama
   ```
4. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the program:
   ```bash
   python main.py
   ```
2. Select your proficiency level (1-6):
   - 1: A1 (Beginner)
   - 2: A2 (Elementary)
   - 3: B1 (Intermediate)
   - 4: B2 (Upper Intermediate)
   - 5: C1 (Advanced)
   - 6: C2 (Proficient)
3. Answer the questions that appear
4. Type 'quit' at any time to exit the program

## Question Types

The program generates questions in three main categories:

1. Vocabulary - Translation and usage questions
2. Conjugation - Verb tense and person questions
3. Grammar - Structural and usage questions

Each question comes with:
- Difficulty level (easy, medium, hard)
- Explanation of the answer
- Example usage in context

## Error Handling

The program includes fallback mechanisms:
- Generates static questions if API fails
- Provides immediate feedback on errors
- Maintains progress tracking locally

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for AI-generated questions)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Updated Readme
