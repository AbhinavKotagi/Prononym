# 📚 Prononym - AI-Powered Vocabulary Learning App

A simple yet powerful Streamlit web application that helps you learn new words, discover synonyms, and practice vocabulary using AI (Groq API).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![Groq](https://img.shields.io/badge/Groq-API-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🌟 Features

### ✅ Implemented Features

- **🏠 Word of the Day**: Discover a new vocabulary word every day
- **🔍 Word Learning**: Search any word to get:
  - AI-generated synonyms (5-10 alternatives)
  - Clear definitions
  - Example sentences
- **📝 Context-Based Suggestions**: 
  - Enter your own sentence
  - Get contextual synonym suggestions
  - See how different synonyms work in context
- **🎯 Practice Quizzes**: 
  - Test your knowledge with MCQ quizzes
  - Track your performance
  - Get instant feedback
- **📊 Progress Tracking**:
  - View total words learned
  - See quiz statistics
  - Monitor accuracy over time
- **⭐ Saved Words**: 
  - Bookmark favorite words
  - Quick access to saved vocabulary

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone or download the project files**

```bash
mkdir prononym
cd prononym

# Create these files: app.py, db.py, ai.py, utils.py, requirements.txt, .env
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup environment variables**

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **How to get Groq API Key:**
> 1. Visit [console.groq.com](https://console.groq.com)
> 2. Sign up for free account
> 3. Navigate to API Keys section
> 4. Create new API key
> 5. Copy and paste into `.env` file

4. **Run the app**

```bash
streamlit run app.py
```

5. **Open in browser**

The app will automatically open at `http://localhost:8501`

---

## 📁 Project Structure

```
prononym/
├── app.py              # Main Streamlit application
├── db.py               # SQLite database operations
├── ai.py               # Groq API integration
├── utils.py            # Helper functions
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .env.example       # Example env file
├── prononym.db        # SQLite database (auto-created)
└── README.md          # This file
```

---

## 🎮 How to Use

### 1️⃣ Home Page - Word of the Day

- View the daily featured word
- See definition, synonyms, and examples
- Track your learning statistics

### 2️⃣ Learn Word

**Basic Search:**
1. Enter any English word
2. Click "🔍 Search"
3. View synonyms, definition, and example
4. Save to favorites with "⭐ Save to Favorites"

**Context-Based Learning:**
1. Enter a sentence containing your word
2. Click "✨ Generate Contextual Examples"
3. See how different synonyms work in your sentence
4. Get confidence ratings for each suggestion

### 3️⃣ Practice Quiz

1. Click "🚀 Start Quiz"
2. Answer 5 multiple-choice questions
3. Get immediate feedback
4. Review your results and accuracy
5. Take another quiz to improve

### 4️⃣ Progress Tracking

- View total words learned
- See quiz statistics
- Monitor overall accuracy
- Review recent quiz attempts

### 5️⃣ Saved Words

- Access all your favorite words
- Review saved vocabulary
- Remove words from favorites

---

## 🔧 Technical Details

### Database Schema

**Words Table:**
```sql
- id: INTEGER PRIMARY KEY
- word: TEXT UNIQUE
- synonyms: TEXT (comma-separated)
- definition: TEXT
- example: TEXT
- created_at: TIMESTAMP
```

**Progress Table:**
```sql
- id: INTEGER PRIMARY KEY
- word: TEXT
- correct: INTEGER
- total: INTEGER
- timestamp: TIMESTAMP
```

**Favorites Table:**
```sql
- id: INTEGER PRIMARY KEY
- word: TEXT UNIQUE
- added_at: TIMESTAMP
```

**Daily Word Table:**
```sql
- id: INTEGER PRIMARY KEY
- word: TEXT
- date: TEXT UNIQUE
- created_at: TIMESTAMP
```

### AI Integration

**Groq API Models Used:**
- Default: `mixtral-8x7b-32768` (balanced performance)
- Alternative: `llama3-70b-8192` (higher quality)
- Alternative: `llama3-8b-8192` (faster responses)

**API Features:**
- Synonym generation with context awareness
- Definition extraction
- Example sentence creation
- Contextual word suggestions

### Fallback System

The app includes a fallback dictionary for common words in case:
- API is unavailable
- Rate limits are reached
- Network issues occur

Words with fallback support:
- eloquent, happy, intelligent, beautiful, brave

---

## 🎨 Customization

### Change AI Model

Edit `app.py`:
```python
st.session_state.ai = AIService(
    api_key=api_key,
    model="llama3-70b-8192"  # Change this
)
```

### Modify UI Colors

Edit the CSS in `app.py` under `st.markdown("""<style>...</style>""")`:
```css
.word-card {
    background: linear-gradient(135deg, #YOUR_COLOR1, #YOUR_COLOR2);
}
```

### Add More Fallback Words

Edit `ai.py` and add to `self.fallback_data`:
```python
"your_word": {
    "synonyms": ["syn1", "syn2", ...],
    "definition": "Your definition",
    "example": "Your example sentence"
}
```

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Ensure `.env` file exists in project root
- Check that `GROQ_API_KEY=...` is set correctly
- No spaces around the `=` sign

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### Database locked errors
- Close other instances of the app
- Delete `prononym.db` to reset database

### API rate limit exceeded
- Wait a few minutes
- The app will use fallback data automatically

### Slow AI responses
- Try switching to `llama3-8b-8192` model (faster)
- Check your internet connection

---

## 📝 Example Usage

### Learning a New Word

```
Input: "meticulous"

Output:
📚 Meticulous
Definition: Showing great attention to detail; very careful and precise

Synonyms: careful, thorough, precise, fastidious, punctilious

Example: She was meticulous in her research, checking every source twice.
```

### Context-Based Suggestions

```
Input Sentence: "I am happy about the results."
Target Word: "happy"

Suggestions:
1. Delighted - "I am delighted about the results." (High confidence)
2. Pleased - "I am pleased about the results." (High confidence)
3. Thrilled - "I am thrilled about the results." (Medium confidence)
```

---

## 🚀 Future Enhancements

Potential features for future versions:

- [ ] Voice pronunciation practice
- [ ] Spaced repetition system
- [ ] Difficulty levels (beginner/intermediate/advanced)
- [ ] User accounts and cloud sync
- [ ] Word games (crosswords, matching)
- [ ] Export vocabulary lists
- [ ] Mobile-responsive design
- [ ] Multiple language support
- [ ] Flashcard mode
- [ ] Achievement badges

---

## 📊 Performance Tips

1. **Caching**: The app uses Streamlit's session state for performance
2. **Database**: SQLite is fast for this use case (single user)
3. **API Calls**: Minimized by using fallback data when possible
4. **Batch Operations**: Quiz questions generated in batches

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

MIT License - feel free to use this project for learning or production!

---

## 🙏 Acknowledgments

- **Groq** for providing fast AI inference API
- **Streamlit** for the amazing web framework
- **SQLite** for lightweight database solution

---

## 📧 Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify Groq API key is valid
4. Check Python version (3.8+)

---

## 🎓 Learning Resources

Want to learn more?
- [Streamlit Documentation](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [Python SQLite Tutorial](https://docs.python.org/3/library/sqlite3.html)

---

**Made with ❤️ for language learners**

*Start learning new words today! 📚✨*