from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

class SpacedRepetitionSystem:
    def __init__(self, user_id: str):
        """Initialize spaced repetition system
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.data_file = Path(f"spaced_repetition_{user_id}.json")
        self.boxes = self._load_boxes()
        self.review_settings = {
            'default_intervals': [1, 2, 4, 8, 16],  # Days
            'priority_threshold': 0.7,  # Threshold for high priority items
            'max_review_items': 10,  # Maximum items to review at once
            'review_priority': 'adaptive'  # adaptive, balanced, or oldest
        }
        self.review_items = []
        
    def _load_boxes(self) -> Dict[int, List[Dict]]:
        """Load or initialize boxes for spaced repetition"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.boxes = data.get('boxes', {
                    1: [], 2: [], 3: [], 4: [], 5: []
                })
                self.review_settings = data.get('review_settings', {
                    'default_intervals': [1, 2, 4, 8, 16],
                    'priority_threshold': 0.7,
                    'max_review_items': 10,
                    'review_priority': 'adaptive'
                })
                return self.boxes
        return {
            1: [], 2: [], 3: [], 4: [], 5: []
        }

    def _save_boxes(self):
        """Save boxes to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({
                'boxes': self.boxes,
                'review_settings': self.review_settings
            }, f, indent=4)

    def add_item(self, item: Dict):
        """Add a new item to the first box
        
        Args:
            item: Dictionary containing item data with keys:
                  - content: The content to learn
                  - type: Type of content (vocabulary, grammar, etc.)
                  - difficulty: Difficulty level
                  - last_review: Last review timestamp
                  - box: Current box number
        """
        item['last_review'] = datetime.now().isoformat()
        item['box'] = 1
        self.boxes[1].append(item)
        self._save_boxes()

    def get_review_items(self) -> List[Dict]:
        """Get items that need review based on priority and settings
        
        Returns:
            List of items that need to be reviewed
        """
        review_items = []
        now = datetime.now()
        
        # Calculate priority scores for each item
        priority_scores = []
        for box_num, items in self.boxes.items():
            for item in items:
                last_review = datetime.fromisoformat(item['last_review'])
                interval = timedelta(days=self.review_settings['default_intervals'][box_num - 1])
                
                # Calculate priority based on:
                # 1. Time since last review
                # 2. Box number (lower boxes have higher priority)
                # 3. Difficulty level
                time_priority = (now - last_review).days / interval.days
                box_priority = 1 / box_num
                difficulty_priority = 1 if item.get('difficulty', 'easy') == 'hard' else 0.5
                
                priority = time_priority * box_priority * difficulty_priority
                
                if now - last_review >= interval:
                    priority_scores.append({
                        'item': item,
                        'box': box_num,
                        'priority': priority,
                        'last_review': last_review
                    })
        
        # Sort items by priority based on settings
        if self.review_settings['review_priority'] == 'adaptive':
            priority_scores.sort(key=lambda x: x['priority'], reverse=True)
        elif self.review_settings['review_priority'] == 'oldest':
            priority_scores.sort(key=lambda x: x['last_review'])
        else:  # balanced
            priority_scores.sort(key=lambda x: (x['box'], x['last_review']))
        
        # Limit to max_review_items
        review_items = priority_scores[:self.review_settings['max_review_items']]
        return review_items

    def update_item(self, item: Dict, is_correct: bool):
        """Update item's box based on performance
        
        Args:
            item: Item to update
            is_correct: Whether the answer was correct
        """
        current_box = item['box']
        item['last_review'] = datetime.now().isoformat()
        
        if is_correct:
            # Move to next box if not in last box
            if current_box < 5:
                self.boxes[current_box].remove(item)
                self.boxes[current_box + 1].append(item)
                item['box'] = current_box + 1
        else:
            # Move to first box if incorrect
            self.boxes[current_box].remove(item)
            self.boxes[1].append(item)
            item['box'] = 1
        
        self._save_boxes()

    def get_statistics(self) -> Dict:
        """Get detailed statistics about the spaced repetition system
        
        Returns:
            Dictionary with comprehensive statistics
        """
        stats = {
            'total_items': sum(len(items) for items in self.boxes.values()),
            'items_per_box': {str(k): len(v) for k, v in self.boxes.items()},
            'items_due': len(self.get_review_items()),
            'review_settings': self.review_settings,
            'box_distribution': self._get_box_distribution(),
            'performance_metrics': self._get_performance_metrics(),
            'next_review_time': self.get_next_review_time()
        }
        return stats

    def _get_box_distribution(self) -> Dict:
        """Get distribution of items across boxes"""
        distribution = {}
        for box_num, items in self.boxes.items():
            distribution[str(box_num)] = {
                'total': len(items),
                'difficulty': self._get_difficulty_distribution(items),
                'type': self._get_type_distribution(items)
            }
        return distribution

    def _get_difficulty_distribution(self, items: List[Dict]) -> Dict:
        """Get distribution of difficulty levels"""
        distribution = {'easy': 0, 'medium': 0, 'hard': 0}
        for item in items:
            difficulty = item.get('difficulty', 'easy')
            if difficulty in distribution:
                distribution[difficulty] += 1
        return distribution

    def _get_type_distribution(self, items: List[Dict]) -> Dict:
        """Get distribution of question types"""
        distribution = {}
        for item in items:
            item_type = item.get('type', 'unknown')
            distribution[item_type] = distribution.get(item_type, 0) + 1
        return distribution

    def _get_performance_metrics(self) -> Dict:
        """Calculate performance metrics"""
        metrics = {
            'average_box': self._calculate_average_box(),
            'review_efficiency': self._calculate_review_efficiency(),
            'difficulty_performance': self._get_difficulty_performance()
        }
        return metrics

    def _calculate_average_box(self) -> float:
        """Calculate average box number"""
        total_items = sum(len(items) for items in self.boxes.values())
        if total_items == 0:
            return 0
        
        total = sum(len(items) * box_num for box_num, items in self.boxes.items())
        return total / total_items

    def _calculate_review_efficiency(self) -> float:
        """Calculate review efficiency"""
        items = [item for box in self.boxes.values() for item in box]
        if not items:
            return 0
            
        total_days = sum(
            (datetime.now() - datetime.fromisoformat(item['last_review'])).days
            for item in items
        )
        return total_days / len(items)

    def _get_difficulty_performance(self) -> Dict:
        """Get performance metrics by difficulty"""
        performance = {}
        for box_num, items in self.boxes.items():
            for item in items:
                difficulty = item.get('difficulty', 'easy')
                if difficulty not in performance:
                    performance[difficulty] = {
                        'count': 0,
                        'box_sum': 0
                    }
                performance[difficulty]['count'] += 1
                performance[difficulty]['box_sum'] += box_num
        
        # Calculate average box per difficulty
        for diff in performance:
            if performance[diff]['count'] > 0:
                performance[diff]['avg_box'] = (
                    performance[diff]['box_sum'] / performance[diff]['count']
                )
        return performance

    def get_next_review_time(self) -> datetime:
        """Get the time when the next review is due
        
        Returns:
            datetime object of next review time
        """
        next_review = None
        
        for box_num, items in self.boxes.items():
            for item in items:
                last_review = datetime.fromisoformat(item['last_review'])
                interval = timedelta(days=2 ** (box_num - 1))
                review_time = last_review + interval
                
                if next_review is None or review_time < next_review:
                    next_review = review_time
        
        return next_review if next_review else datetime.now()
