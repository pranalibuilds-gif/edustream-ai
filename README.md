🎓 EduStream AI: Final Project Summary

EduStream AI is a localized, AI-powered educational tool that converts YouTube lectures into comprehensive study guides and interactive quizzes. It is designed to work with long-form content (2-3 hour lectures) while maintaining user privacy and zero API costs.

🚀 Key Features Implemented

Long-Video Processing: Uses recursive summarization to process transcripts of any length by "chunking" text into manageable bites.

Multi-Language Support: Automatically detects available transcripts (including auto-generated Hindi, Spanish, etc.) and translates them into your target language (English, Spanish, French, etc.) via the LLM.

Local AI Intelligence: Powered by Llama 3.2 via Ollama, ensuring all data stays on your machine.

Optimized Learning Flow: Users read the summary first to build context before revealing a 5-question comprehensive quiz.

Robust Data Extraction: Includes a fail-safe transcript processor that handles various versions of the youtube-transcript-api library and diverse YouTube caption settings.

📁 Project Structure

app.py: The Streamlit interface and state management.

src/processor.py: The "Ear" — handles transcript fetching and cleaning.

src/llm_engine.py: The "Brain" — handles summarization, translation, and quiz generation logic.

requirements.txt: Lists all necessary Python dependencies.

🛠️ How to Run

Start Ollama: Ensure the Ollama service is running and you have the model installed:

ollama pull llama3.2


Setup Environment:

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt


Launch the App:

streamlit run app.py


🧠 Technical Highlights

Context Window Management: We bypassed the 128k token limit issues by implementing a "Map-Reduce" summary pattern.

Stateful UI: Using st.session_state, we ensured that the AI doesn't have to re-process the video if the user simply wants to toggle the quiz or check an answer.

JSON Grounding: Used Regex-based extraction to ensure that even if the LLM is "chatty," the app only parses the valid JSON array for the quiz.

Status: Project Complete & Production Ready.
