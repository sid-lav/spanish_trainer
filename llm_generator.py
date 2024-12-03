import json
from typing import Tuple, Dict, Optional, List
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import random as random_module
import os

load_dotenv()

class LLMQuestionGenerator:
    def __init__(self, level: str):
        """Initialize the LLM question generator
        
        Args:
            level: CEFR level (A1, A2, B1, etc.)
        """
        self.level = level
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.question_cache = []  # Cache for recent questions
        self.last_cache_update = datetime.now()
        self.cache_duration = 60  # Cache duration in seconds
        
        # Enhanced system prompt with more specific instructions
        self.system_prompt = f"""You are a Spanish language teacher. Generate appropriate Spanish learning questions 
        for level {level}. The questions should be challenging but not too difficult for this level.
        
        Format your response as JSON with these fields:
        {{
            "question_type": "vocabulary" | "conjugation" | "grammar",
            "question": "The question text",
            "answer": "The correct answer",
            "difficulty": "easy" | "medium" | "hard",
            "explanation": "Brief explanation of the answer",
            "example": "Example sentence using the word/conjugation"
        }}
        
        When generating questions:
        1. For vocabulary questions, provide common usage examples
        2. For conjugation questions, include different tenses and pronouns
        3. For grammar questions, explain the grammatical rule
        """

    def _update_cache(self):
        """Update the question cache with new questions"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "Generate 5 Spanish learning questions"}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            questions = eval(response.choices[0].message.content)
            if isinstance(questions, dict):
                questions = [questions]
            
            self.question_cache.extend(questions)
            self.last_cache_update = datetime.now()
        except Exception as e:
            print(f"Error updating cache: {str(e)}")

    def generate_question(self) -> Tuple[str, str, str, str]:
        """Generate a question using LLM with caching
        
        Returns:
            Tuple containing:
            - Question text
            - Correct answer
            - Difficulty level
            - Explanation/example
        """
        try:
            # Check if cache needs to be updated
            if len(self.question_cache) < 3 or \
               (datetime.now() - self.last_cache_update).total_seconds() > self.cache_duration:
                self._update_cache()
            
            # Get a random question from cache
            if self.question_cache:
                question_data = random_module.choice(self.question_cache)
                self.question_cache.remove(question_data)  # Remove used question
                return (
                    question_data['question'],
                    question_data['answer'],
                    question_data['difficulty'],
                    f"{question_data.get('explanation', '')}\n{question_data.get('example', '')}"
                )
            
            # Fallback to static question if cache is empty
            fallback_questions = [
                {
                    "question": "Translate 'hello' to Spanish:",
                    "answer": "hola",
                    "difficulty": "easy",
                    "explanation": "Basic greeting in Spanish",
                    "example": "Hola, ¿cómo estás?"
                },
                {
                    "question": "Conjugate 'comer' in present tense, 'yo' form:",
                    "answer": "como",
                    "difficulty": "medium",
                    "explanation": "Present tense conjugation of -ar verbs",
                    "example": "Yo como una manzana cada mañana."
                }
            ]
            question_data = random_module.choice(fallback_questions)
            return (
                question_data['question'],
                question_data['answer'],
                question_data['difficulty'],
                question_data['explanation']
            )

        except Exception as e:
            print(f"Error generating question: {str(e)}")
            fallback_questions = [
                {
                    "question": "Translate 'hello' to Spanish:",
                    "answer": "hola",
                    "difficulty": "easy",
                    "explanation": "Basic greeting in Spanish",
                    "example": "Hola, ¿cómo estás?"
                },
                {
                    "question": "Conjugate 'comer' in present tense, 'yo' form:",
                    "answer": "como",
                    "difficulty": "medium",
                    "explanation": "Present tense conjugation of -ar verbs",
                    "example": "Yo como una manzana cada mañana."
                }
            ]
            question_data = random_module.choice(fallback_questions)
            return (
                question_data['question'],
                question_data['answer'],
                question_data['difficulty'],
                question_data['explanation']
            )

    def validate_answer(self, user_answer: str, correct_answer: str) -> Tuple[bool, str]:
        """Validate user's answer using LLM and provide feedback
        
        Returns:
            Tuple containing:
            - Boolean indicating if answer is correct
            - Feedback/explanation about the answer
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Spanish language teacher. Evaluate if the user's answer is correct and provide feedback."},
                    {"role": "user", "content": f"User's answer: {user_answer}\nCorrect answer: {correct_answer}\nIs this answer correct? If not, explain why and provide the correct answer."}
                ]
            )
            
            # Get the evaluation and feedback
            evaluation = response.choices[0].message.content
            is_correct = "correct" in evaluation.lower() or "yes" in evaluation.lower()
            
            # Extract feedback
            feedback_start = evaluation.lower().find("feedback")
            feedback = evaluation[feedback_start:] if feedback_start != -1 else ""
            
            return is_correct, feedback
            
        except Exception as e:
            print(f"Error validating answer: {str(e)}")
            # Fallback to simple string comparison
            is_correct = user_answer.lower() == correct_answer.lower()
            feedback = "Correct answer!" if is_correct else f"Incorrect. The correct answer was: {correct_answer}"
            return is_correct, feedback
