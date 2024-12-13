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
        self.current_box = 1
        self.review_items = []
        
    def _load_boxes(self) -> Dict[int, List[Dict]]:
        """Load or initialize boxes for spaced repetition"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            1: [],  # Easy box
            2: [],  # Medium box
            3: [],  # Hard box
            4: [],  # Mastered box
            5: []   # Mastered box
        }

    def _save_boxes(self):
        """Save boxes to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.boxes, f, indent=4)

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
        """Get items that need review based on their box and last review time
        
        Returns:
            List of items that need to be reviewed
        """
        review_items = []
        now = datetime.now()
        
        # Check each box for items that need review
        for box_num, items in self.boxes.items():
            for item in items:
                last_review = datetime.fromisoformat(item['last_review'])
                
                # Calculate review interval based on box number
                interval = timedelta(days=2 ** (box_num - 1))
                
                if now - last_review >= interval:
                    review_items.append({
                        'item': item,
                        'box': box_num
                    })
        
        # Shuffle items to avoid memorizing order
        random.shuffle(review_items)
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
        """Get statistics about the spaced repetition system
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_items': sum(len(items) for items in self.boxes.values()),
            'items_per_box': {str(k): len(v) for k, v in self.boxes.items()},
            'items_due': len(self.get_review_items())
        }
        return stats

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
