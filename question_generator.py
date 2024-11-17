from typing import Dict, List, Tuple
import random
from difflib import SequenceMatcher
from levels import VERBS, VOCABULARY

PRONOUNS = {
    'yo': 'I',
    'tú': 'you',
    'él': 'he',
    'ella': 'she',
    'nosotros': 'we',
    'vosotros': 'you (plural)',
    'ellos': 'they'
}

TENSES = {
    'present': 'present',
    'preterite': 'past',
    'imperfect': 'imperfect',
    'future': 'future'
}

class QuestionGenerator:
    def __init__(self, level: str):
        self.level = level
        self.vocabulary = self._get_vocabulary()

    def _get_vocabulary(self) -> List[Dict[str, str]]:
        """Get vocabulary for the user's level"""
        return VOCABULARY.get(self.level, [])

    def generate_vocabulary_question(self) -> Tuple[str, str]:
        """Generate a vocabulary translation question"""
        word = random.choice(self.vocabulary)
        return f"Translate '{word['english']}' to Spanish:", word['spanish']

    def generate_conjugation_question(self) -> Tuple[str, str]:
        """Generate a verb conjugation question"""
        verb = random.choice(VERBS)
        pronoun = random.choice(list(PRONOUNS.keys()))
        
        # Define endings for each verb type
        endings = {
            'ar': {
                'yo': 'o', 'tú': 'as', 'él': 'a', 'ella': 'a',
                'nosotros': 'amos', 'vosotros': 'áis', 'ellos': 'an'
            },
            'er': {
                'yo': 'o', 'tú': 'es', 'él': 'e', 'ella': 'e',
                'nosotros': 'emos', 'vosotros': 'éis', 'ellos': 'en'
            },
            'ir': {
                'yo': 'o', 'tú': 'es', 'él': 'e', 'ella': 'e',
                'nosotros': 'imos', 'vosotros': 'ís', 'ellos': 'en'
            }
        }
        
        # Get the correct endings for this verb type
        verb_endings = endings.get(verb['type'], endings['ar'])  # Default to 'ar' endings if not found
        
        # Conjugate the verb
        conjugated = verb['stem'] + verb_endings[pronoun]
        
        return (
            f"Conjugate '{verb['infinitive']}' in present tense, {PRONOUNS[pronoun]} form:",
            conjugated
        )

# Removed fill-in-the-blank question type since it's not useful

    def validate_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Validate user's answer with some tolerance for typos"""
        # Case-insensitive comparison
        user_answer = user_answer.lower()
        correct_answer = correct_answer.lower()
        
        # Exact match
        if user_answer == correct_answer:
            return True
            
        # Allow some leeway for typos using SequenceMatcher
        similarity = SequenceMatcher(None, user_answer, correct_answer).ratio()
        return similarity > 0.8  # 80% similarity threshold
