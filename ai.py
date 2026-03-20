"""
AI Service module for Prononym
Handles all Groq API interactions for synonym generation and word analysis
"""

import json
from typing import List, Dict, Optional
from groq import Groq


class AIService:
    """AI service using Groq API for word analysis"""
    
    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        """
        Initialize AI service with Groq API
        
        Args:
            api_key: Groq API key
            model: Model to use (default: mixtral-8x7b-32768)
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        
        # Fallback dictionary for common words
        self.fallback_data = {
            "eloquent": {
                "synonyms": ["articulate", "fluent", "expressive", "persuasive", "well-spoken"],
                "definition": "Fluent or persuasive in speaking or writing",
                "example": "She gave an eloquent speech that moved the entire audience."
            },
            "happy": {
                "synonyms": ["joyful", "cheerful", "delighted", "pleased", "content"],
                "definition": "Feeling or showing pleasure or contentment",
                "example": "The children were happy playing in the park."
            },
            "intelligent": {
                "synonyms": ["smart", "clever", "bright", "brilliant", "astute"],
                "definition": "Having or showing intelligence, especially of a high level",
                "example": "She is an intelligent student who excels in mathematics."
            },
            "beautiful": {
                "synonyms": ["gorgeous", "stunning", "lovely", "attractive", "pretty"],
                "definition": "Pleasing the senses or mind aesthetically",
                "example": "The sunset was beautiful with vibrant orange and pink hues."
            },
            "brave": {
                "synonyms": ["courageous", "fearless", "bold", "valiant", "heroic"],
                "definition": "Ready to face and endure danger or pain; showing courage",
                "example": "The brave firefighter rescued the family from the burning building."
            }
        }
    
    def get_word_details(self, word: str) -> Optional[Dict]:
        """
        Get word details including synonyms, definition, and example
        
        Args:
            word: The word to analyze
            
        Returns:
            Dictionary with word details or None if failed
        """
        # Try AI first
        result = self._get_from_groq(word)
        
        # Fallback to dictionary if AI fails
        if not result or not result.get('synonyms'):
            result = self._get_from_fallback(word)
        
        return result
    
    def _get_from_groq(self, word: str) -> Optional[Dict]:
        """Get word details from Groq API"""
        try:
            prompt = f"""For the word: "{word}"

Provide the following information in valid JSON format:
1. A list of 5-10 synonyms (common English synonyms only)
2. A clear, simple definition (one sentence)
3. One example sentence using the word in context

Format your response EXACTLY as valid JSON like this:
{{
  "word": "{word}",
  "synonyms": ["synonym1", "synonym2", "synonym3", "synonym4", "synonym5"],
  "definition": "A clear definition here",
  "example": "An example sentence using {word} in context"
}}

IMPORTANT: Return ONLY the JSON object, no other text."""

            # Make API call
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful English vocabulary assistant. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            word_data = json.loads(content)
            
            # Validate required fields
            if not all(key in word_data for key in ['synonyms', 'definition', 'example']):
                raise ValueError("Missing required fields in AI response")
            
            # Ensure word field exists
            if 'word' not in word_data:
                word_data['word'] = word
            
            return word_data
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw content: {content}")
            return None
        except Exception as e:
            print(f"Groq API error: {e}")
            return None
    
    def _get_from_fallback(self, word: str) -> Optional[Dict]:
        """Get word details from fallback dictionary"""
        word_lower = word.lower()
        
        if word_lower in self.fallback_data:
            data = self.fallback_data[word_lower].copy()
            data['word'] = word_lower
            return data
        
        # Generate generic response for unknown words
        return {
            'word': word_lower,
            'synonyms': [word_lower],  # Return the word itself
            'definition': f"Definition for '{word}' not available. Try another word.",
            'example': f"Please try searching for a different word."
        }
    
    def get_context_suggestions(
        self,
        sentence: str,
        target_word: str,
        max_suggestions: int = 5
    ) -> List[Dict]:
        """
        Get contextual synonym suggestions for a word in a sentence
        
        Args:
            sentence: The original sentence
            target_word: The word to replace
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of suggestion dictionaries
        """
        try:
            prompt = f"""Given this sentence:
"{sentence}"

Suggest {max_suggestions} alternative words that could replace "{target_word}" while maintaining the sentence's meaning and tone.

For each suggestion, provide:
1. The synonym
2. The rewritten sentence with that synonym
3. A confidence level (high/medium/low)

Format as valid JSON:
{{
  "suggestions": [
    {{
      "synonym": "word1",
      "example": "rewritten sentence 1",
      "confidence": "high"
    }},
    {{
      "synonym": "word2",
      "example": "rewritten sentence 2",
      "confidence": "medium"
    }}
  ]
}}

Return ONLY the JSON object."""

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert English language tutor specializing in vocabulary and synonyms. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            
            return result.get('suggestions', [])
            
        except Exception as e:
            print(f"Error getting context suggestions: {e}")
            # Return basic fallback
            return [{
                "synonym": target_word,
                "example": sentence,
                "confidence": "low"
            }]
    
    def generate_quiz_question(self, word: str, synonyms: List[str]) -> Dict:
        """
        Generate a quiz question for a word
        
        Args:
            word: The target word
            synonyms: List of correct synonyms
            
        Returns:
            Dictionary with question details
        """
        # This is a simple implementation
        # In a full version, you could use AI to generate distractors
        import random
        
        if not synonyms:
            return None
        
        correct_answer = random.choice(synonyms)
        
        return {
            'word': word,
            'correct': correct_answer,
            'type': 'synonym_match'
        }
    
    def get_random_word(self) -> str:
        """Get a random word for word of the day"""
        try:
            prompt = """Generate one interesting English vocabulary word suitable for learning.
The word should be:
- Moderately challenging (not too common, not too obscure)
- Useful in everyday conversation
- Have clear synonyms

Return ONLY the word, nothing else."""

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.8,
                max_tokens=50
            )
            
            word = response.choices[0].message.content.strip().lower()
            # Clean up any quotes or extra characters
            word = word.replace('"', '').replace("'", '').strip()
            
            return word
            
        except Exception as e:
            print(f"Error generating random word: {e}")
            # Return a fallback word
            import random
            return random.choice(list(self.fallback_data.keys()))