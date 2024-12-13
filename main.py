from typing import Dict, Optional
import sys
from colorama import init, Fore, Style
from llm_generator import LLMQuestionGenerator
from progress_tracker import ProgressTracker
from spaced_repetition import SpacedRepetitionSystem
import random

# Initialize colorama for Windows support
init()

class SpanishTrainer:
    def __init__(self):
        self.levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        self.user_id = None
        self.progress_tracker = None
        self.llm_generator = None

    def initialize_user(self):
        """Initialize user session"""
        print("\nWelcome to Spanish Trainer!")
        print("""Choose your level:
        1. A1 (Beginner)
        2. A2 (Elementary)
        3. B1 (Intermediate)
        4. B2 (Upper Intermediate)
        5. C1 (Advanced)
        6. C2 (Proficient)
        """)
        
        while True:
            choice = input("Enter your level (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                self.user_id = f"user_{random.randint(1000, 9999)}"
                self.progress_tracker = ProgressTracker(self.user_id)
                self.spaced_repetition = SpacedRepetitionSystem(self.user_id)
                stats = self.progress_tracker.get_statistics()
                print(f"\nYour current progress:")
                print(f"Overall accuracy: {stats['accuracy']:.1f}%")
                print(f"Total questions answered: {stats['total']}")
                print(f"Items needing review: {stats['review_items']}")
                print("\nStarting new session...")
                self.progress_tracker.current_session['start_time'] = datetime.now().isoformat()
                self.llm_generator = LLMQuestionGenerator(self.levels[int(choice) - 1])
                break
            print("Please enter a number between 1 and 6.")
            print("Please enter a number between 1 and 6.")

    def run_quiz(self):
        """Run the Spanish quiz"""
        print("\nStarting the quiz...")
        print("Type 'quit' at any time to exit.")
        print("Type 'stats' to view your progress")
        print("Type 'review' to practice difficult items")

        while True:
            # Check for items that need review
            review_items = self.spaced_repetition.get_review_items()
            
            if review_items:
                print(f"\n{Fore.YELLOW}Review time! ({len(review_items)} items to review){Style.RESET_ALL}")
                for review_item in review_items:
                    item = review_item['item']
                    print(f"\n{Fore.CYAN}{item['content']}{Style.RESET_ALL}")
                    print(f"Type: {item['type']}")
                    print(f"Difficulty: {item['difficulty']}")
                    
                    user_answer = input("Your answer: ").strip().lower()
                    
                    if user_answer == 'quit':
                        self.progress_tracker.current_session['end_time'] = datetime.now().isoformat()
                        self.progress_tracker._save_progress()
                        print("\nSession ended.")
                        break
                    
                    # Validate answer
                    is_correct, feedback = self.llm_generator.validate_answer(user_answer, item['correct_answer'])
                    
                    # Update spaced repetition
                    self.spaced_repetition.update_item(item, is_correct)
                    
                    # Display feedback
                    if is_correct:
                        print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                        print(f"Moving to box {item['box']}")
                    else:
                        print(f"{Fore.RED}Incorrect.{Style.RESET_ALL} {item['correct_answer']}")
                        print(f"Moving to box 1")
                    print(f"Feedback: {feedback}")
                
                # Continue with regular questions
                if user_answer == 'quit':
                    break

            # Generate new question using LLM
            question, correct_answer, difficulty, explanation, question_type = self.llm_generator.generate_question()
            
            # Display question with color coding
            print(f"\n{Fore.CYAN}{question}{Style.RESET_ALL}")
            print(f"Difficulty: {Fore.YELLOW}{difficulty}{Style.RESET_ALL}")
            print(f"Explanation: {Fore.GREEN}{explanation}{Style.RESET_ALL}")
            
            user_answer = input("Your answer: ").strip().lower()
            
            if user_answer == 'quit':
                self.progress_tracker.current_session['end_time'] = datetime.now().isoformat()
                self.progress_tracker._save_progress()
                print("\nSession ended.")
                break
            
            if user_answer == 'stats':
                stats = self.progress_tracker.get_statistics()
                print("\nYour Progress:")
                print(f"Overall accuracy: {stats['accuracy']:.1f}%")
                print(f"Total questions answered: {stats['total']}")
                print(f"Items needing review: {stats['review_items']}")
                continue
            
            if user_answer == 'review':
                self._run_review_session()
                continue
            
            # Validate answer
            is_correct, feedback = self.llm_generator.validate_answer(user_answer, correct_answer)
            
            # Update spaced repetition
            self.spaced_repetition.add_item({
                'content': question,
                'type': question_type,
                'difficulty': difficulty,
                'correct_answer': correct_answer,
                'explanation': explanation
            })
            
            # Update progress
            self.progress_tracker.update_score(is_correct, question_type, question)
            
            # Display feedback
            if is_correct:
                print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Incorrect.{Style.RESET_ALL} {correct_answer}")
            print(f"Feedback: {feedback}")

            print(f"\n{Fore.CYAN}{question}{Style.RESET_ALL}")
            print(f"Difficulty: {difficulty}")
            print(f"Explanation: {explanation}")
            user_answer = input("Your answer: ").strip()

            if user_answer.lower() == 'quit':
                break

            is_correct, feedback = self.llm_generator.validate_answer(user_answer, correct_answer)
            
            if is_correct:
                print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                print(f"{feedback}")
                if question_type == 'vocabulary':
                    self.progress_tracker.track_vocabulary(user_answer, True)
                elif question_type == 'conjugation':
                    self.progress_tracker.track_verb(user_answer, True)
            else:
                print(f"{Fore.RED}Incorrect.{Style.RESET_ALL}")
                print(f"{feedback}")
                if question_type == 'vocabulary':
                    self.progress_tracker.track_vocabulary(user_answer, False)
                elif question_type == 'conjugation':
                    self.progress_tracker.track_verb(user_answer, False)

            self.progress_tracker.update_score(is_correct)

    def show_statistics(self):
        """Show user statistics"""
        stats = self.progress_tracker.get_statistics()
        print("\nQuiz Statistics:")
        print(f"Total Questions: {stats['total']}")
        print(f"Accuracy: {stats['accuracy']:.1f}%")

    def run(self):
        """Run the main program"""
        try:
            self.initialize_user()
            self.run_quiz()
            self.show_statistics()
        except KeyboardInterrupt:
            print("\nGoodbye!")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    trainer = SpanishTrainer()
    trainer.run()
