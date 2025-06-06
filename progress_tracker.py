from typing import Dict, List, Tuple
import json
from pathlib import Path

class ProgressTracker:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.progress_file = Path(f"progress_{user_id}.json")
        self.progress = self._load_progress()
        self.review_queue = []  # Items to review based on performance
        self.current_session = {
            'start_time': None,
            'end_time': None,
            'questions': [],
            'score': 0,
            'total_questions': 0
        }

    def _load_progress(self) -> Dict:
        """Load user progress from file or create new if not exists"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'correct_answers': 0,
            'total_questions': 0,
            'vocabulary': {},
            'verbs': {},
            'levels': {
                'A1': {'completed': False, 'accuracy': 0, 'total_questions': 0},
                'A2': {'completed': False, 'accuracy': 0, 'total_questions': 0},
                'B1': {'completed': False, 'accuracy': 0, 'total_questions': 0},
                'B2': {'completed': False, 'accuracy': 0, 'total_questions': 0},
                'C1': {'completed': False, 'accuracy': 0, 'total_questions': 0},
                'C2': {'completed': False, 'accuracy': 0, 'total_questions': 0}
            },
            'sessions': [],
            'review_items': []  # Items that need review based on performance
        }
        }

    def _save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=4)

    def update_score(self, is_correct: bool, question_type: str, content: str):
        """Update the user's score and track question details"""
        self.progress['total_questions'] += 1
        if is_correct:
            self.progress['correct_answers'] += 1

        # Track question details
        self.current_session['questions'].append({
            'type': question_type,
            'content': content,
            'correct': is_correct,
            'timestamp': datetime.now().isoformat()
        })

        # Add to review queue if incorrect
        if not is_correct:
            self.review_queue.append({
                'content': content,
                'type': question_type,
                'timestamp': datetime.now().isoformat(),
                'attempts': 1
            })

        self._save_progress()

    def get_statistics(self) -> Dict:
        """Get comprehensive user statistics"""
        total = self.progress['total_questions']
        if total == 0:
            return {
                'accuracy': 0,
                'total': 0,
                'levels': {},
                'review_items': 0
            }
        
        return {
            'accuracy': (self.progress['correct_answers'] / total) * 100,
            'total': total,
            'levels': self.progress['levels'],
            'review_items': len(self.review_queue),
            'recent_sessions': self.progress['sessions'][-5:]  # Last 5 sessions
        }

    def track_vocabulary(self, word: str, is_correct: bool):
        """Track vocabulary performance"""
        if word not in self.progress['vocabulary']:
            self.progress['vocabulary'][word] = {
                'correct': 0,
                'total': 0
            }
        self.progress['vocabulary'][word]['total'] += 1
        if is_correct:
            self.progress['vocabulary'][word]['correct'] += 1
        self._save_progress()

    def track_verb(self, verb: str, is_correct: bool):
        """Track verb conjugation performance"""
        if verb not in self.progress['verbs']:
            self.progress['verbs'][verb] = {
                'correct': 0,
                'total': 0
            }
        self.progress['verbs'][verb]['total'] += 1
        if is_correct:
            self.progress['verbs'][verb]['correct'] += 1
        self._save_progress()

    def get_vocabulary_stats(self, word: str) -> Tuple[int, int]:
        """Get statistics for a specific word"""
        if word in self.progress['vocabulary']:
            stats = self.progress['vocabulary'][word]
            return stats['correct'], stats['total']
        return 0, 0

    def get_verb_stats(self, verb: str) -> Tuple[int, int]:
        """Get statistics for a specific verb"""
        if verb in self.progress['verbs']:
            stats = self.progress['verbs'][verb]
            return stats['correct'], stats['total']
        return 0, 0
