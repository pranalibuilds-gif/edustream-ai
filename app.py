import streamlit as st
from src.processor import extract_video_id, get_video_transcript, clean_transcript_text
from src.llm_engine import LLMEngine

# Page Configuration
st.set_page_config(page_title="EduStream AI", page_icon="🎓", layout="wide")

# Initialize our AI Engine
@st.cache_resource
def load_engine():
    return LLMEngine(model_name="llama3.2")

engine = load_engine()

# --- UI Header ---
st.title("🎓 EduStream AI: Video Summarizer & Quizzer")
st.markdown("Transform YouTube lectures into multilingual study guides—**100% locally.**")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    # Language Selector
    target_lang = st.selectbox(
        "Output Language",
        ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese", "Arabic"],
        index=0
    )
    
    st.divider()
    if st.button("Clear Session / New Video"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Main Input Section ---
video_url = st.text_input("Paste YouTube Video URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Learning Module", type="primary"):
    if not video_url:
        st.warning("Please enter a valid URL.")
    else:
        # Reset quiz visibility for a new video process
        st.session_state['show_quiz'] = False
        
        with st.status(f"Processing in {target_lang}... This takes longer for long videos.", expanded=True) as status:
            video_id = extract_video_id(video_url)
            
            if not video_id:
                st.error("Invalid YouTube URL.")
            else:
                raw_transcript = get_video_transcript(video_id)
                
                if "Error" in raw_transcript:
                    st.error(raw_transcript)
                else:
                    clean_text = clean_transcript_text(raw_transcript)
                    
                    st.write(f"🧠 AI is translating and summarizing into {target_lang}...")
                    summary = engine.generate_summary(clean_text, target_lang=target_lang)
                    st.session_state['summary'] = summary
                    
                    st.write(f"❓ Creating {target_lang} quiz questions...")
                    # We pass the summary to the quiz generator to ensure full coverage
                    quiz = engine.generate_quiz(summary, target_lang=target_lang)
                    st.session_state['quiz'] = quiz
                    
                    status.update(label="Complete!", state="complete", expanded=False)

# --- Display Results ---

# PART 1: The Summary (Always shown first once generated)
if 'summary' in st.session_state:
    st.divider()
    st.subheader(f"📖 Video Summary ({target_lang})")
    st.markdown(st.session_state['summary'])
    
    # PART 2: The "Take Quiz" Button (Only shown if quiz isn't already active)
    if not st.session_state.get('show_quiz', False):
        st.write("---")
        if st.button("✍️ Take Quiz", type="secondary", use_container_width=True):
            st.session_state['show_quiz'] = True
            st.rerun()

# PART 3: The Quiz Section (Revealed after clicking the button)
if st.session_state.get('show_quiz', False):
    st.divider()
    st.subheader(f"💡 Revision Quiz ({target_lang})")
    quiz_data = st.session_state.get('quiz', [])
    
    if not quiz_data:
        st.warning("Could not generate quiz in this language.")
    else:
        # We use a form to collect all answers before scoring
        with st.form("quiz_form"):
            for i, q in enumerate(quiz_data):
                st.write(f"**Q{i+1}: {q['question']}**")
                st.radio(f"Select your answer for Q{i+1}:", q['options'], key=f"q_{i}")
                st.write("---")
            
            submitted = st.form_submit_button("Submit All Answers")
            
            if submitted:
                correct_count = 0
                st.subheader("Results:")
                for i, q in enumerate(quiz_data):
                    user_ans = st.session_state.get(f"q_{i}")
                    if user_ans == q['answer']:
                        correct_count += 1
                        st.success(f"Q{i+1}: Correct! ✅")
                    else:
                        st.error(f"Q{i+1}: Incorrect. The right answer was: {q['answer']}")
                
                # Show final score metric
                st.metric("Final Score", f"{correct_count}/{len(quiz_data)}")
                
                # Celebration if they get everything right!
                if correct_count == len(quiz_data):
                    st.balloons()