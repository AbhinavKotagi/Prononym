"""
Database module for Prononym
Handles all SQLite database operations
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class Database:
    """SQLite database manager for Prononym app"""
    
    def __init__(self, db_name="prononym.db"):
        """Initialize database connection and create tables"""
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create all required tables if they don't exist"""
        
        # Words table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                synonyms TEXT,
                definition TEXT,
                example TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Progress table (quiz attempts)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT,
                correct INTEGER,
                total INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Favorites table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Daily word table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_word (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                date TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    # ==================== WORD OPERATIONS ====================
    
    def save_word(self, word: str, synonyms: List[str], definition: str, example: str):
        """Save a word with its details"""
        try:
            synonyms_str = ",".join(synonyms) if synonyms else ""
            self.cursor.execute("""
                INSERT OR REPLACE INTO words (word, synonyms, definition, example)
                VALUES (?, ?, ?, ?)
            """, (word.lower(), synonyms_str, definition, example))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving word: {e}")
            return False
    
    def get_word(self, word: str) -> Optional[Tuple]:
        """Get word details from database"""
        self.cursor.execute("""
            SELECT * FROM words WHERE word = ?
        """, (word.lower(),))
        return self.cursor.fetchone()
    
    def get_all_words(self) -> List[Tuple]:
        """Get all words from database"""
        self.cursor.execute("SELECT * FROM words ORDER BY created_at DESC")
        return self.cursor.fetchall()
    
    def get_all_words_for_quiz(self) -> List[Tuple]:
        """Get all words with synonyms for quiz generation"""
        self.cursor.execute("""
            SELECT word, synonyms FROM words 
            WHERE synonyms IS NOT NULL AND synonyms != ''
        """)
        return self.cursor.fetchall()
    
    def get_total_words_searched(self) -> int:
        """Get count of unique words searched"""
        self.cursor.execute("SELECT COUNT(*) FROM words")
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    # ==================== DAILY WORD OPERATIONS ====================
    
    def set_word_of_day(self, date: str, word: str):
        """Set word of the day for a specific date"""
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO daily_word (date, word)
                VALUES (?, ?)
            """, (date, word.lower()))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error setting word of day: {e}")
            return False
    
    def get_word_of_day(self, date: str) -> Optional[str]:
        """Get word of the day for a specific date"""
        self.cursor.execute("""
            SELECT word FROM daily_word WHERE date = ?
        """, (date,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    # ==================== PROGRESS/QUIZ OPERATIONS ====================
    
    def save_quiz_result(self, correct: int, total: int, word: str = "quiz"):
        """Save quiz result to progress table"""
        try:
            self.cursor.execute("""
                INSERT INTO progress (word, correct, total)
                VALUES (?, ?, ?)
            """, (word, correct, total))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving quiz result: {e}")
            return False
    
    def get_recent_progress(self, limit: int = 10) -> List[Tuple]:
        """Get recent quiz attempts"""
        self.cursor.execute("""
            SELECT * FROM progress 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()
    
    def get_total_quizzes(self) -> int:
        """Get total number of quizzes taken"""
        self.cursor.execute("SELECT COUNT(*) FROM progress")
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_overall_accuracy(self) -> float:
        """Calculate overall quiz accuracy"""
        self.cursor.execute("""
            SELECT SUM(correct), SUM(total) FROM progress
        """)
        result = self.cursor.fetchone()
        
        if result and result[1] and result[1] > 0:
            accuracy = (result[0] / result[1]) * 100
            return round(accuracy, 1)
        return 0.0
    
    # ==================== FAVORITES OPERATIONS ====================
    
    def add_favorite(self, word: str):
        """Add word to favorites"""
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO favorites (word)
                VALUES (?)
            """, (word.lower(),))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding favorite: {e}")
            return False
    
    def remove_favorite(self, word: str):
        """Remove word from favorites"""
        try:
            self.cursor.execute("""
                DELETE FROM favorites WHERE word = ?
            """, (word.lower(),))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error removing favorite: {e}")
            return False
    
    def get_all_favorites(self) -> List[Tuple]:
        """Get all favorite words"""
        self.cursor.execute("""
            SELECT * FROM favorites ORDER BY added_at DESC
        """)
        return self.cursor.fetchall()
    
    def is_favorite(self, word: str) -> bool:
        """Check if word is in favorites"""
        self.cursor.execute("""
            SELECT COUNT(*) FROM favorites WHERE word = ?
        """, (word.lower(),))
        result = self.cursor.fetchone()
        return result[0] > 0 if result else False
    
    # ==================== UTILITY METHODS ====================
    
    def clear_all_data(self):
        """Clear all data from database (use with caution!)"""
        try:
            self.cursor.execute("DELETE FROM words")
            self.cursor.execute("DELETE FROM progress")
            self.cursor.execute("DELETE FROM favorites")
            self.cursor.execute("DELETE FROM daily_word")
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        if hasattr(self, 'conn'):
            self.conn.close()