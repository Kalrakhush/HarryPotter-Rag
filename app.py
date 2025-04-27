import streamlit as st
import time
import threading
import queue
from src.agents.harry_potter_crew import HarryPotterRAGCrew
import traceback

# Page configuration
st.set_page_config(
    page_title="Hogwarts Knowledge Vault",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');
        .main { background-color: #0c1624; }
        h1, h2, h3 { font-family: 'Cinzel', serif !important; color: #d4af37 !important; letter-spacing: 0.05em; }
        p, div, span, li { font-family: 'Cormorant Garamond', serif !important; color: #e6e6e6; font-size: 1.2rem; }
        .stTextInput div div input, .stSelectbox div div, .stButton button { border: 2px solid #d4af37 !important; border-radius: 5px; background-color: #1a1a2e; color: #e6e6e6 !important; }
        .stButton button { font-family: 'Cinzel', serif !important; font-weight: 600; color: #d4af37 !important; background-color: rgba(26, 26, 46, 0.85); border: 2px solid #d4af37 !important; padding: 0.5em 1em; }
        .stButton button:hover { background-color: #d4af37 !important; color: #0c1624 !important; }
        .chat-message { padding: 1.5rem; border-radius: 0.8rem; margin-bottom: 1rem; display: flex; border: 1px solid rgba(212, 175, 55, 0.2); }
        .user-message { background-color: rgba(26, 26, 46, 0.85); border-left: 5px solid #326872; }
        .assistant-message { background-color: rgba(26, 26, 46, 0.65); border-left: 5px solid #d4af37; }
        .chat-content { width: 100%; color: #e6e6e6; }
        .scroll-container { max-height: 65vh; overflow-y: auto; padding-right: 10px; margin-top: 20px; }
        .character-tag { font-size: 0.9rem; font-weight: bold; color: #d4af37; margin-bottom: 5px; }
        .stSelectbox div[data-baseweb="select"] > div {
        min-width: px !important;   /* or whatever min width you need */
        width: 100% !important;        /* fill the sidebar width */
    }
        div[role="listbox"] ul li { color: #e6e6e6 !important; background-color: #1a1a2e !important; }
        div[role="listbox"] { background-color: #1a1a2e !important; }
    </style>
    """, unsafe_allow_html=True)

# Characters
characters = [
    "Harry Potter",
    "Hermione Granger",
    "Ron Weasley",
    "Albus Dumbledore",
    "Severus Snape",
    "Draco Malfoy",
    "Luna Lovegood",
    "Rubeus Hagrid",
    "Minerva McGonagall",
    "Sirius Black"
]

# Initialize session state
def initialize_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.messages = []
        st.session_state.answer_stream = ""
        st.session_state.is_answering = False
        st.session_state.process_status = ""
        st.session_state.debug_info = []
        st.session_state.crew_instance = HarryPotterRAGCrew()  # ✅ initialize here
        st.session_state.selected_character = "Albus Dumbledore"
        st.session_state.initialized = True

initialize_session_state()  # ✅ run immediately after imports

# Updated generate_response function
def generate_response(question, character, result_queue):
    try:
        if 'debug_info' not in st.session_state:
            st.session_state.debug_info = []
        
        st.session_state.debug_info.append(f"Starting response generation for '{question}' as '{character}'")
        st.session_state.process_status = "Initializing crew..."

        # 🛠️ FIX: create crew_instance directly, like your main.py
        crew_instance = HarryPotterRAGCrew()
        crew = crew_instance.crew()

        st.session_state.process_status = "Setting up inputs..."
        inputs = {
            "question": question,
            "character": character,
        }

        st.session_state.process_status = "Generating response..."
        result = crew.kickoff(inputs=inputs)

        st.session_state.process_status = "Processing complete!"
        result_queue.put(result)
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"

        if 'debug_info' not in st.session_state:
            st.session_state.debug_info = []

        st.session_state.debug_info.append(f"ERROR: {error_msg}")
        st.session_state.process_status = "Error occurred"
        result_queue.put("I'm sorry, an error occurred while processing your question. Please try again.")

# Display messages
def display_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.container():
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="chat-content">
                        <p>{message["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.container():
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="chat-content">
                        <div class="character-tag">{message.get("character", "Assistant")}:</div>
                        <p>{message["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Main
def main():
    initialize_session_state()
    load_css()

    with st.sidebar:
        
        st.title("Hogwarts Knowledge Vault")
        st.markdown("#### _Where Magic Meets Memory_")
        st.markdown("---")

        st.markdown("### Choose a Character")

        # 🛠️ Make sure selected_character exists
        if "selected_character" not in st.session_state:
            st.session_state.selected_character = "Albus Dumbledore"
        st.markdown("<div style='width: 250px; padding-bottom: 0.5em;'>", unsafe_allow_html=True)
        selected_character = st.selectbox(
            "Who should answer your question?",
            options=characters,
            index=characters.index(st.session_state.selected_character),
            key="character_selector",
        )

        st.session_state.selected_character = selected_character

        st.markdown("---")

        if st.button("🧹 Clear Conversation"):
            st.session_state.messages = []
            st.success("Conversation cleared!")


    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="margin-bottom: 0;">Hogwarts Knowledge Vault</h1>
            <p style="font-style: italic; opacity: 0.8;">Ask anything about the wizarding world...</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        display_messages()

        if st.session_state.is_answering:
            selected_character = st.session_state.current_character
            with st.container():
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="chat-content">
                        <div class="character-tag">{selected_character}:</div>
                        <p><em>{st.session_state.process_status}</em></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                progress_bar = st.progress(0)
                if hasattr(st.session_state, 'progress_value'):
                    if st.session_state.progress_value < 100:
                        st.session_state.progress_value += 1
                else:
                    st.session_state.progress_value = 0
                progress_bar.progress(st.session_state.progress_value)

        st.markdown('</div>', unsafe_allow_html=True)

        with st.form(key="query_form", clear_on_submit=True):
            question = st.text_input("Ask your question:", key="question_input",
                                    placeholder="What's your question for the wizarding world?")
            submit = st.form_submit_button("🪄 Ask", use_container_width=True)

            if submit and question:
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })

                st.session_state.is_answering = True
                st.session_state.current_character = st.session_state.selected_character
                st.session_state.process_status = "Thinking..."
                st.session_state.progress_value = 0

                if 'result_queue' not in st.session_state:
                    st.session_state.result_queue = queue.Queue()

                while not st.session_state.result_queue.empty():
                    try:
                        st.session_state.result_queue.get_nowait()
                    except:
                        pass

                thread = threading.Thread(
                    target=generate_response,
                    args=(question, st.session_state.selected_character, st.session_state.result_queue)
                )
                thread.daemon = True
                thread.start()

                st.rerun()

    if st.session_state.is_answering and hasattr(st.session_state, 'result_queue'):
        try:
            try:
                result = st.session_state.result_queue.get_nowait()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result,
                    "character": st.session_state.current_character
                })
                st.session_state.is_answering = False
                st.session_state.progress_value = 100
                st.rerun()
            except queue.Empty:
                time.sleep(0.1)
                st.rerun()
        except Exception as e:
            st.error(f"Error processing response. Please try again.")
            st.session_state.is_answering = False

if __name__ == "__main__":
    main()
