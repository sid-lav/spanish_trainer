import os
from typing import Tuple, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMQuestionGenerator:
    def __init__(self, level: str):
        """Initialize the LLM question generator
        
        Args:
            level: CEFR level (A1, A2, B1, etc.)
        """
        self.level = level
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = f"""You are a Spanish language teacher. Generate appropriate Spanish learning questions 
        for level {level}. The questions should be challenging but not too difficult for this level.
        
        Format your response as JSON with these fields:
        {{
            "question_type": "vocabulary" | "conjugation",
            "question": "The question text",
            "answer": "The correct answer",
            "difficulty": "easy" | "medium" | "hard"
        }}
        """

    def generate_question(self) -> Tuple[str, str]:
        """Generate a question using LLM"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for better quality
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "Generate a Spanish learning question"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            question_data = response.choices[0].message.content
            question_data = eval(question_data)  # Convert string to dict
            
            return question_data['question'], question_data['answer']
            
        except Exception as e:
            print(f"Error generating question: {str(e)}")
            # Fallback to static question if LLM fails
            return self._generate_fallback_question()

    def _generate_fallback_question(self) -> Tuple[str, str]:
        """Generate a fallback question if LLM fails"""
        return "Translate 'hello' to Spanish:", "hola"

    def validate_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Validate user's answer using LLM"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Spanish language teacher. Evaluate if the user's answer is correct."},
                    {"role": "user", "content": f"User's answer: {user_answer}\nCorrect answer: {correct_answer}\nIs this answer correct?"}
                ]
            )
            
            # Get the evaluation
            evaluation = response.choices[0].message.content.lower()
            return "correct" in evaluation or "yes" in evaluation
            
        except Exception as e:
            print(f"Error validating answer: {str(e)}")
            # Fallback to simple string comparison
            return user_answer.lower() == correct_answer.lower()
