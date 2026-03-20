"""
Utility functions for Prononym app
Helper functions for quiz generation, formatting, etc.
"""

import random
from typing import List, Dict, Tuple


def generate_quiz_options(
    words_data: List[Tuple],
    num_questions: int = 5
) -> List[Dict]:
    """
    Generate quiz questions with multiple choice options
    
    Args:
        words_data: List of tuples (word, synonyms) from database
        num_questions: Number of questions to generate
        
    Returns:
        List of question dictionaries
    """
    # Filter words that have synonyms
    valid_words = [
        (word, synonyms.split(',')) 
        for word, synonyms in words_data 
        if synonyms and synonyms.strip()
    ]
    
    if len(valid_words) < num_questions:
        num_questions = len(valid_words)
    
    # Randomly select words for quiz
    selected_words = random.sample(valid_words, num_questions)
    
    questions = []
    for word, synonyms in selected_words:
        # Clean synonyms
        synonyms = [s.strip() for s in synonyms if s.strip()]
        
        if not synonyms:
            continue
        
        # Pick a correct answer
        correct_answer = random.choice(synonyms)
        
        # Generate wrong options from other words' synonyms
        wrong_options = []
        other_words = [w for w, _ in valid_words if w != word]
        
        for other_word, other_synonyms in valid_words:
            if other_word != word:
                other_syns = [s.strip() for s in other_synonyms if s.strip()]
                wrong_options.extend(other_syns)
        
        # Remove duplicates and the correct answer
        wrong_options = list(set(wrong_options))
        if correct_answer in wrong_options:
            wrong_options.remove(correct_answer)
        
        # Select 3 random wrong options
        if len(wrong_options) >= 3:
            wrong_options = random.sample(wrong_options, 3)
        else:
            # If not enough wrong options, add generic words
            generic_wrong = ["different", "various", "multiple", "several", "numerous"]
            while len(wrong_options) < 3:
                random_word = random.choice(generic_wrong)
                if random_word != correct_answer and random_word not in wrong_options:
                    wrong_options.append(random_word)
        
        # Combine and shuffle options
        all_options = [correct_answer] + wrong_options[:3]
        random.shuffle(all_options)
        
        questions.append({
            'word': word,
            'options': all_options,
            'correct': correct_answer
        })
    
    return questions


def calculate_accuracy(correct: int, total: int) -> float:
    """
    Calculate accuracy percentage
    
    Args:
        correct: Number of correct answers
        total: Total number of questions
        
    Returns:
        Accuracy as a percentage (0-100)
    """
    if total == 0:
        return 0.0
    return round((correct / total) * 100, 2)


def format_word_display(word: str) -> str:
    """
    Format word for display (capitalize first letter)
    
    Args:
        word: The word to format
        
    Returns:
        Formatted word string
    """
    return word.strip().title()


def validate_sentence(sentence: str, target_word: str) -> bool:
    """
    Validate if target word is in the sentence
    
    Args:
        sentence: The sentence to check
        target_word: The word to find
        
    Returns:
        True if word is in sentence, False otherwise
    """
    return target_word.lower() in sentence.lower()


def clean_synonyms_list(synonyms: str) -> List[str]:
    """
    Clean and parse synonyms string from database
    
    Args:
        synonyms: Comma-separated string of synonyms
        
    Returns:
        List of cleaned synonym strings
    """
    if not synonyms:
        return []
    
    return [s.strip() for s in synonyms.split(',') if s.strip()]


def get_difficulty_emoji(accuracy: float) -> str:
    """
    Get emoji based on quiz accuracy
    
    Args:
        accuracy: Accuracy percentage
        
    Returns:
        Emoji string
    """
    if accuracy >= 90:
        return "🌟"
    elif accuracy >= 80:
        return "🎯"
    elif accuracy >= 70:
        return "👍"
    elif accuracy >= 60:
        return "📚"
    else:
        return "💪"


def generate_encouragement(accuracy: float) -> str:
    """
    Generate encouraging message based on performance
    
    Args:
        accuracy: Quiz accuracy percentage
        
    Returns:
        Encouragement message
    """
    if accuracy >= 90:
        return "Outstanding! You're a vocabulary master! 🌟"
    elif accuracy >= 80:
        return "Excellent work! Keep up the great progress! 🎯"
    elif accuracy >= 70:
        return "Good job! You're on the right track! 👍"
    elif accuracy >= 60:
        return "Nice try! Practice makes perfect! 📚"
    else:
        return "Keep learning! You'll improve with practice! 💪"


def format_timestamp(timestamp: str) -> str:
    """
    Format timestamp for display
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        Human-readable timestamp
    """
    from datetime import datetime
    
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except:
        return timestamp


def get_streak_emoji(streak_days: int) -> str:
    """
    Get emoji based on streak length
    
    Args:
        streak_days: Number of consecutive days
        
    Returns:
        Streak emoji
    """
    if streak_days >= 30:
        return "🔥🔥🔥"
    elif streak_days >= 7:
        return "🔥🔥"
    elif streak_days >= 1:
        return "🔥"
    else:
        return "⭐"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def parse_json_safely(json_string: str) -> Dict:
    """
    Safely parse JSON string with error handling
    
    Args:
        json_string: JSON string to parse
        
    Returns:
        Parsed dictionary or empty dict on error
    """
    import json
    
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return {}


def highlight_word_in_sentence(sentence: str, word: str) -> str:
    """
    Highlight target word in sentence using markdown
    
    Args:
        sentence: The sentence
        word: Word to highlight
        
    Returns:
        Sentence with highlighted word
    """
    import re
    
    # Case-insensitive replacement with bold markdown
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub(f"**{word}**", sentence)