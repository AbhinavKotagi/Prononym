"""
Prononym - AI-Powered Vocabulary Learning App
A Streamlit prototype for learning synonyms with AI
"""

import streamlit as st
import os
from datetime import datetime, date
from dotenv import load_dotenv

# Import custom modules
from db import Database
from ai import AIService
from utils import generate_quiz_options, calculate_accuracy

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Prononym - Learn Synonyms",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .word-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        color: black;
    }
    .synonym-chip {
        background: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.3rem;
        font-weight: 500;
        color: black;
    }
    .stat-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #667eea;
        color: black;
    }
    .stat-box h2 {
        color: #000000;
        margin: 0;
    }
    .stat-box p {
        color: #555555;
        margin: 0.5rem 0 0 0;
    }
    .example-box {
        background: #fff9e6;
        padding: 1rem;
        border-left: 4px solid #ffd700;
        border-radius: 5px;
        margin: 1rem 0;
        font-style: italic; 
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = Database()

if 'ai' not in st.session_state:
    # Try to get from .env first
    api_key = os.getenv("GROQ_API_KEY")
    
    # If not found, you can temporarily hardcode it here
    if not api_key:
        # TEMPORARY: Replace with your actual key
        api_key = "gsk_your_actual_groq_api_key_here"  # ⚠️ Replace this!
        
        if api_key == "gsk_your_actual_groq_api_key_here":
            st.error("⚠️ Please replace the API key in app.py line 73!")
            st.info("""
            **Two ways to fix:**
            1. Create a `.env` file with: `GROQ_API_KEY=your_key`
            2. Or replace the key directly in app.py (line 73)
            """)
            st.stop()
    
    st.session_state.ai = AIService(api_key)

if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = None

# Main app
def main():
    # Sidebar navigation
    st.sidebar.markdown("# 📚 Prononym")
    st.sidebar.markdown("*Learn • Practice • Master*")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🔍 Learn Word", "🎯 Practice Quiz", "📊 Progress", "⭐ Saved Words"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info("AI-powered vocabulary learning app to help you master synonyms and improve your language skills.")
    
    # Route to pages
    if page == "🏠 Home":
        home_page()
    elif page == "🔍 Learn Word":
        learn_word_page()
    elif page == "🎯 Practice Quiz":
        practice_quiz_page()
    elif page == "📊 Progress":
        progress_page()
    elif page == "⭐ Saved Words":
        saved_words_page()


def home_page():
    """Home page with Word of the Day"""
    st.markdown('<h1 class="main-header">📚 Prononym</h1>', unsafe_allow_html=True)
    st.markdown("### Welcome to your daily vocabulary boost!")
    
    # Word of the Day section
    st.markdown("## 🌟 Word of the Day")
    
    # Get or generate word of the day
    today = date.today().isoformat()
    word_of_day = st.session_state.db.get_word_of_day(today)
    
    if not word_of_day:
        with st.spinner("🔮 Generating today's word..."):
            # Get a random word using AI
            word_data = st.session_state.ai.get_word_details("eloquent")  # Fallback
            if word_data:
                word_of_day = word_data['word']
                st.session_state.db.set_word_of_day(today, word_of_day)
    
    # Display Word of the Day
    if word_of_day:
        display_word_card(word_of_day, is_daily=True)
    
    # Quick stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_words = st.session_state.db.get_total_words_searched()
        st.markdown(f"""
        <div class="stat-box">
            <h2>{total_words}</h2>
            <p>Words Explored</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        quiz_count = st.session_state.db.get_total_quizzes()
        st.markdown(f"""
        <div class="stat-box">
            <h2>{quiz_count}</h2>
            <p>Quizzes Taken</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        accuracy = st.session_state.db.get_overall_accuracy()
        st.markdown(f"""
        <div class="stat-box">
            <h2>{accuracy}%</h2>
            <p>Accuracy</p>
        </div>
        """, unsafe_allow_html=True)


def learn_word_page():
    """Learn new words with AI-powered insights"""
    st.markdown("## 🔍 Learn a New Word")
    st.markdown("Enter any word to discover its synonyms and see contextual examples!")
    
    # Word input
    word_input = st.text_input(
        "Enter a word:",
        placeholder="e.g., happy, intelligent, brave...",
        key="word_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_btn = st.button("🔍 Search", type="primary", use_container_width=True)
    with col2:
        if word_input:
            save_btn = st.button("⭐ Save to Favorites", use_container_width=True)
            if save_btn:
                st.session_state.db.add_favorite(word_input.lower())
                st.success(f"✅ '{word_input}' saved to favorites!")
    
    if search_btn and word_input:
        with st.spinner(f"🤖 Analyzing '{word_input}' with AI..."):
            # Get word details from AI
            word_data = st.session_state.ai.get_word_details(word_input)
            
            if word_data and word_data.get('synonyms'):
                # Save to database
                st.session_state.db.save_word(
                    word_data['word'],
                    word_data['synonyms'],
                    word_data['definition'],
                    word_data['example']
                )
                
                # Display results
                display_word_card(word_data['word'], word_data)
                
                # Context-based examples section
                st.markdown("---")
                st.markdown("### 📝 See Synonyms in Context")
                
                context_sentence = st.text_area(
                    "Enter your own sentence:",
                    placeholder=f"Example: I am {word_input} about the results.",
                    height=100,
                    key="context_input"
                )
                
                if st.button("✨ Generate Contextual Examples", type="secondary"):
                    if context_sentence and word_input.lower() in context_sentence.lower():
                        with st.spinner("🎨 Creating contextual examples..."):
                            suggestions = st.session_state.ai.get_context_suggestions(
                                context_sentence,
                                word_input
                            )
                            
                            if suggestions:
                                st.markdown("#### 💡 Suggested Alternatives:")
                                for i, suggestion in enumerate(suggestions[:5], 1):
                                    st.markdown(f"""
                                    <div class="example-box">
                                        <strong>{i}. {suggestion['synonym'].title()}</strong><br>
                                        {suggestion['example']}
                                        <br><small>Confidence: {suggestion.get('confidence', 'medium')}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ Please include the word '{word_input}' in your sentence.")
            else:
                st.error(f"❌ Could not find details for '{word_input}'. Please try another word.")


def display_word_card(word, word_data=None, is_daily=False):
    """Display a word card with details"""
    if not word_data:
        # Fetch from database or AI
        db_word = st.session_state.db.get_word(word)
        if db_word:
            word_data = {
                'word': db_word[1],
                'synonyms': db_word[2].split(',') if db_word[2] else [],
                'definition': db_word[3],
                'example': db_word[4]
            }
        else:
            word_data = st.session_state.ai.get_word_details(word)
    
    if word_data:
        st.markdown(f"""
        <div class="word-card">
            <h1 style="margin: 0; font-size: 3rem;">
                {word_data['word'].title()}
                {'🌟' if is_daily else ''}
            </h1>
            <p style="font-size: 1.2rem; margin-top: 0.5rem; opacity: 0.9;">
                {word_data.get('definition', 'No definition available')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Synonyms
        st.markdown("#### 🔤 Synonyms:")
        synonyms_html = "".join([
            f'<span class="synonym-chip">{syn.strip()}</span>'
            for syn in word_data.get('synonyms', [])[:10]
        ])
        st.markdown(synonyms_html, unsafe_allow_html=True)
        
        # Example sentence
        if word_data.get('example'):
            st.markdown("#### 📖 Example:")
            st.markdown(f"""
            <div class="example-box">
                {word_data['example']}
            </div>
            """, unsafe_allow_html=True)


def practice_quiz_page():
    """Practice quiz page"""
    st.markdown("## 🎯 Practice Quiz")
    st.markdown("Test your synonym knowledge!")
    
    # Quiz initialization
    if st.session_state.quiz_state is None:
        difficulty = st.selectbox(
            "Select difficulty:",
            ["Easy", "Medium", "Hard"],
            index=1
        )
        
        if st.button("🚀 Start Quiz", type="primary"):
            # Get words from database
            words = st.session_state.db.get_all_words_for_quiz()
            
            if len(words) < 5:
                st.warning("⚠️ Not enough words in database. Please learn some words first!")
            else:
                # Generate quiz questions
                quiz_questions = generate_quiz_options(words, num_questions=5)
                st.session_state.quiz_state = {
                    'questions': quiz_questions,
                    'current': 0,
                    'answers': [],
                    'correct_count': 0
                }
                st.rerun()
    else:
        # Quiz in progress
        quiz = st.session_state.quiz_state
        current_q = quiz['current']
        
        if current_q < len(quiz['questions']):
            question = quiz['questions'][current_q]
            
            # Progress bar
            progress = (current_q + 1) / len(quiz['questions'])
            st.progress(progress)
            st.markdown(f"**Question {current_q + 1} of {len(quiz['questions'])}**")
            
            # Question
            st.markdown(f"### Which word is a synonym of **'{question['word']}'**?")
            
            # Options
            selected = st.radio(
                "Choose your answer:",
                question['options'],
                key=f"q_{current_q}",
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Submit Answer", type="primary"):
                    is_correct = selected == question['correct']
                    quiz['answers'].append({
                        'word': question['word'],
                        'selected': selected,
                        'correct': question['correct'],
                        'is_correct': is_correct
                    })
                    
                    if is_correct:
                        quiz['correct_count'] += 1
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong! The correct answer is: {question['correct']}")
                    
                    quiz['current'] += 1
                    
                    # Save progress
                    if quiz['current'] >= len(quiz['questions']):
                        # Quiz completed
                        accuracy = (quiz['correct_count'] / len(quiz['questions'])) * 100
                        st.session_state.db.save_quiz_result(
                            quiz['correct_count'],
                            len(quiz['questions'])
                        )
                    
                    st.rerun()
        else:
            # Quiz completed
            st.balloons()
            st.success("🎉 Quiz Completed!")
            
            accuracy = (quiz['correct_count'] / len(quiz['questions'])) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{quiz['correct_count']}/{len(quiz['questions'])}")
            with col2:
                st.metric("Accuracy", f"{accuracy:.1f}%")
            with col3:
                if accuracy >= 80:
                    grade = "🌟 Excellent"
                elif accuracy >= 60:
                    grade = "👍 Good"
                else:
                    grade = "📚 Keep Practicing"
                st.metric("Grade", grade)
            
            # Show answers
            st.markdown("### 📋 Review Your Answers:")
            for i, answer in enumerate(quiz['answers'], 1):
                icon = "✅" if answer['is_correct'] else "❌"
                st.markdown(f"""
                {icon} **{i}. {answer['word']}** - 
                You answered: *{answer['selected']}* 
                {'' if answer['is_correct'] else f"(Correct: *{answer['correct']}*)"}
                """)
            
            if st.button("🔄 Take Another Quiz"):
                st.session_state.quiz_state = None
                st.rerun()


def progress_page():
    """User progress and statistics"""
    st.markdown("## 📊 Your Progress")
    
    # Overall stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_words = st.session_state.db.get_total_words_searched()
        st.metric("Words Learned", total_words)
    
    with col2:
        quiz_count = st.session_state.db.get_total_quizzes()
        st.metric("Quizzes Taken", quiz_count)
    
    with col3:
        accuracy = st.session_state.db.get_overall_accuracy()
        st.metric("Avg Accuracy", f"{accuracy}%")
    
    with col4:
        favorites = len(st.session_state.db.get_all_favorites())
        st.metric("Saved Words", favorites)
    
    # Recent activity
    st.markdown("---")
    st.markdown("### 📈 Recent Quiz Results")
    
    recent_quizzes = st.session_state.db.get_recent_progress()
    if recent_quizzes:
        for quiz in recent_quizzes:
            accuracy = (quiz[2] / quiz[3] * 100) if quiz[3] > 0 else 0
            timestamp = quiz[4]
            
            st.markdown(f"""
            <div class="stat-box" style="text-align: left; margin: 0.5rem 0;">
                <strong>{timestamp}</strong><br>
                Score: {quiz[2]}/{quiz[3]} ({accuracy:.1f}%)
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📝 No quiz history yet. Take your first quiz to see your progress!")


def saved_words_page():
    """Saved/favorite words"""
    st.markdown("## ⭐ Saved Words")
    
    favorites = st.session_state.db.get_all_favorites()
    
    if favorites:
        st.markdown(f"*You have saved {len(favorites)} words*")
        
        # Display as expandable cards
        for word_tuple in favorites:
            word = word_tuple[1]
            with st.expander(f"📌 {word.title()}"):
                display_word_card(word)
                
                if st.button(f"🗑️ Remove '{word}'", key=f"remove_{word}"):
                    st.session_state.db.remove_favorite(word)
                    st.success(f"Removed '{word}' from favorites")
                    st.rerun()
    else:
        st.info("⭐ No saved words yet. Start learning and save your favorite words!")


if __name__ == "__main__":
    main()