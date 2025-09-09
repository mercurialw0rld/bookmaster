import streamlit as st
import os
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Custom CSS for Enhanced Red 8-bit Theme
def load_css():
    st.markdown("""
    <style>
    /* Enhanced 8-bit Red Theme with Animations */
    :root {
        --primary-red: #ff0040;
        --secondary-red: #ff4080;
        --dark-red: #800020;
        --light-red: #ff80a0;
        --neon-red: #ff0066;
        --electric-red: #ff1a75;
        --background: #0a0505;
        --background-secondary: #1a0a0a;
        --text-color: #ffffff;
        --text-glow: #ff4080;
        --border-color: #ff0040;
        --shadow-color: rgba(255, 0, 64, 0.5);
    }

    /* Animated Background with CRT Effect */
    .main {
        background: var(--background);
        color: var(--text-color);
        position: relative;
        overflow: hidden;
        z-index: 1;
    }

    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background:
            radial-gradient(circle at 20% 80%, rgba(255, 0, 64, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 64, 128, 0.1) 0%, transparent 50%),
            linear-gradient(45deg, transparent 25%, rgba(255, 0, 64, 0.03) 25%, rgba(255, 0, 64, 0.03) 75%, transparent 75%),
            linear-gradient(-45deg, transparent 25%, rgba(255, 64, 128, 0.03) 25%, rgba(255, 64, 128, 0.03) 75%, transparent 75%);
        background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
        background-position: 0 0, 50px 50px, 0 0, 10px 10px;
        animation: backgroundShift 20s linear infinite;
        z-index: -2;
        pointer-events: none;
    }

    /* Simplified CRT Scanlines Effect */
    .main::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(255, 0, 64, 0.02) 2px,
            rgba(255, 0, 64, 0.02) 4px
        );
        pointer-events: none;
        z-index: -1;
        opacity: 0.5;
    }

    @keyframes backgroundShift {
        0% { transform: translate(0, 0); }
        100% { transform: translate(100px, 100px); }
    }

    .stApp {
        background: linear-gradient(135deg,
            var(--background) 0%,
            var(--background-secondary) 50%,
            var(--background) 100%);
        position: relative;
        z-index: 1;
        min-height: 100vh;
    }

    /* Ensure Streamlit content is visible */
    .stApp > div:first-child {
        z-index: 2;
        position: relative;
    }

    .block-container {
        z-index: 2;
        position: relative;
        min-height: 100vh;
        padding: 20px;
    }

    /* Make sure all Streamlit elements are visible */
    .element-container, .stMarkdown, .stText, .stButton, .stForm {
        z-index: 3;
        position: relative;
    }

    /* Fix any potential opacity issues */
    .stApp {
        opacity: 1 !important;
    }

    .main {
        opacity: 1 !important;
    }

    .pixelated-border {
        border: 4px solid var(--primary-red);
        border-radius: 0px;
        background:
            linear-gradient(135deg, rgba(255, 0, 64, 0.1) 0%, rgba(255, 64, 128, 0.05) 100%),
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 3px,
                rgba(255, 0, 64, 0.1) 3px,
                rgba(255, 0, 64, 0.1) 6px
            );
        background-blend-mode: multiply;
        padding: 20px;
        margin: 15px 0;
        position: relative;
        box-shadow:
            0 0 20px var(--shadow-color),
            inset 0 0 20px rgba(255, 0, 64, 0.1);
        animation: borderGlow 3s ease-in-out infinite alternate;
    }

    @keyframes borderGlow {
        0% { box-shadow: 0 0 20px var(--shadow-color), inset 0 0 20px rgba(255, 0, 64, 0.1); }
        100% { box-shadow: 0 0 30px var(--neon-red), inset 0 0 30px rgba(255, 26, 117, 0.2); }
    }

    .retro-button {
        background:
            linear-gradient(135deg, var(--primary-red) 0%, var(--electric-red) 100%),
            var(--primary-red);
        color: white;
        border: 3px solid var(--dark-red);
        border-radius: 0px;
        padding: 15px 30px;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 3px;
        box-shadow:
            4px 4px 0px var(--dark-red),
            0 0 15px var(--shadow-color),
            inset 0 0 10px rgba(255, 255, 255, 0.1);
        transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .retro-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }

    .retro-button:hover {
        background:
            linear-gradient(135deg, var(--neon-red) 0%, var(--electric-red) 100%),
            var(--neon-red);
        transform: translate(-3px, -3px);
        box-shadow:
            6px 6px 0px var(--dark-red),
            0 0 25px var(--neon-red),
            inset 0 0 15px rgba(255, 255, 255, 0.2);
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
    }

    .retro-button:hover::before {
        left: 100%;
    }

    .retro-button:active {
        transform: translate(-1px, -1px);
        box-shadow:
            2px 2px 0px var(--dark-red),
            0 0 10px var(--shadow-color);
    }

    .retro-input {
        background:
            linear-gradient(135deg, rgba(255, 0, 64, 0.1) 0%, rgba(255, 64, 128, 0.05) 100%),
            rgba(255, 0, 64, 0.1);
        border: 3px solid var(--primary-red);
        border-radius: 0px;
        padding: 15px;
        color: white;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        box-shadow:
            0 0 10px var(--shadow-color),
            inset 0 0 10px rgba(255, 0, 64, 0.1);
        transition: all 0.3s ease;
        position: relative;
    }

    .retro-input:focus {
        outline: none;
        border-color: var(--neon-red);
        box-shadow:
            0 0 20px var(--neon-red),
            inset 0 0 15px rgba(255, 26, 117, 0.2);
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }

    .conversation-bubble {
        background:
            linear-gradient(135deg, rgba(255, 64, 128, 0.2) 0%, rgba(255, 128, 160, 0.1) 100%),
            rgba(255, 64, 128, 0.2);
        border: 2px solid var(--secondary-red);
        border-radius: 0px;
        padding: 18px;
        margin: 12px 0;
        font-family: 'Courier New', monospace;
        position: relative;
        box-shadow: 0 0 15px var(--shadow-color);
        animation: bubblePulse 4s ease-in-out infinite;
        backdrop-filter: blur(1px);
    }

    @keyframes bubblePulse {
        0%, 100% { box-shadow: 0 0 15px var(--shadow-color); }
        50% { box-shadow: 0 0 25px var(--neon-red); }
    }

    .user-message {
        background:
            linear-gradient(135deg, rgba(255, 0, 64, 0.3) 0%, rgba(255, 64, 128, 0.2) 100%),
            rgba(255, 0, 64, 0.3);
        border-left: 4px solid var(--primary-red);
        animation: userGlow 3s ease-in-out infinite alternate;
    }

    @keyframes userGlow {
        0% { border-left-color: var(--primary-red); }
        100% { border-left-color: var(--neon-red); }
    }

    .ai-message {
        background:
            linear-gradient(135deg, rgba(255, 64, 128, 0.2) 0%, rgba(255, 128, 160, 0.1) 100%),
            rgba(255, 64, 128, 0.2);
        border-left: 4px solid var(--light-red);
        animation: aiGlow 3s ease-in-out infinite alternate;
    }

    @keyframes aiGlow {
        0% { border-left-color: var(--light-red); }
        100% { border-left-color: var(--electric-red); }
    }

    .header-text {
        font-family: 'Courier New', monospace;
        font-size: 42px;
        font-weight: bold;
        color: var(--primary-red);
        text-shadow:
            3px 3px 0px var(--dark-red),
            0 0 20px var(--neon-red),
            0 0 40px var(--neon-red),
            0 0 60px var(--electric-red);
        text-align: center;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 6px;
        animation: titleGlow 2s ease-in-out infinite alternate;
        background: linear-gradient(45deg, var(--primary-red), var(--neon-red), var(--electric-red));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
    }

    .header-text::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 4px;
        background: linear-gradient(90deg, transparent, var(--neon-red), transparent);
        animation: underlineSlide 3s linear infinite;
    }

    @keyframes titleGlow {
        0% {
            text-shadow: 3px 3px 0px var(--dark-red), 0 0 20px var(--neon-red);
            filter: brightness(1);
        }
        100% {
            text-shadow: 3px 3px 0px var(--dark-red), 0 0 30px var(--electric-red), 0 0 50px var(--neon-red);
            filter: brightness(1.2);
        }
    }

    @keyframes underlineSlide {
        0% { transform: translateX(-50%) scaleX(0); }
        50% { transform: translateX(-50%) scaleX(1); }
        100% { transform: translateX(-50%) scaleX(0); }
    }

    .subheader {
        font-family: 'Courier New', monospace;
        font-size: 20px;
        color: var(--secondary-red);
        text-align: center;
        margin-bottom: 25px;
        text-shadow: 0 0 10px var(--light-red);
        animation: subtitlePulse 3s ease-in-out infinite;
        letter-spacing: 2px;
    }

    @keyframes subtitlePulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.02); }
    }

    .file-info {
        background:
            linear-gradient(135deg, rgba(128, 0, 32, 0.3) 0%, rgba(160, 0, 40, 0.2) 100%),
            rgba(128, 0, 32, 0.3);
        border: 2px solid var(--dark-red);
        padding: 15px;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
        text-align: center;
        box-shadow: 0 0 15px var(--shadow-color);
        animation: infoGlow 4s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }

    .file-info::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 26, 117, 0.1), transparent);
        animation: infoShimmer 3s linear infinite;
    }

    @keyframes infoGlow {
        0%, 100% { box-shadow: 0 0 15px var(--shadow-color); }
        50% { box-shadow: 0 0 25px var(--electric-red); }
    }

    @keyframes infoShimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .status-text {
        font-family: 'Courier New', monospace;
        color: var(--light-red);
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 8px var(--text-glow);
        animation: statusFlicker 2s ease-in-out infinite;
        letter-spacing: 1px;
    }

    @keyframes statusFlicker {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* Hide Streamlit's default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Particle Effects */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -2;
    }

    .particle {
        position: absolute;
        width: 3px;
        height: 3px;
        background: var(--primary-red);
        border-radius: 50%;
        animation: particleFloat 15s linear infinite;
        opacity: 0.3;
        box-shadow: 0 0 2px var(--primary-red);
    }

    .particle:nth-child(2n) {
        background: var(--neon-red);
        animation-duration: 20s;
        animation-delay: -5s;
        opacity: 0.25;
        box-shadow: 0 0 3px var(--neon-red);
    }

    .particle:nth-child(3n) {
        background: var(--electric-red);
        animation-duration: 25s;
        animation-delay: -10s;
        opacity: 0.2;
        box-shadow: 0 0 4px var(--electric-red);
    }

    @keyframes particleFloat {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% { opacity: 0.6; }
        90% { opacity: 0.6; }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }

    /* Loading Animation Enhancement */
    .stSpinner > div {
        border-color: var(--primary-red) transparent transparent transparent !important;
        border-width: 4px !important;
    }

    /* Success/Error Message Styling */
    .stSuccess, .stError, .stWarning {
        background: linear-gradient(135deg, rgba(255, 0, 64, 0.1) 0%, rgba(255, 64, 128, 0.05) 100%);
        border: 2px solid var(--primary-red);
        border-radius: 0px;
        box-shadow: 0 0 15px var(--shadow-color);
        animation: messageGlow 2s ease-in-out infinite alternate;
    }

    @keyframes messageGlow {
        0% { box-shadow: 0 0 15px var(--shadow-color); }
        100% { box-shadow: 0 0 25px var(--neon-red); }
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 12px;
    }

    ::-webkit-scrollbar-track {
        background: var(--background);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-red);
        border-radius: 0px;
        box-shadow: 0 0 5px var(--shadow-color);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--neon-red);
        box-shadow: 0 0 10px var(--neon-red);
    }

    /* Typing Animation for AI Responses */
    .typing-indicator {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid var(--light-red);
        border-radius: 50%;
        border-top-color: transparent;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Enhanced Form Styling */
    .stForm {
        background: rgba(255, 0, 64, 0.05);
        border: 2px solid var(--primary-red);
        border-radius: 0px;
        padding: 20px;
        box-shadow: 0 0 20px var(--shadow-color);
    }

    /* Progress Bar Enhancement */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-red), var(--neon-red), var(--electric-red));
        border-radius: 0px;
        box-shadow: 0 0 10px var(--shadow-color);
    }

    /* File Uploader Enhancement */
    .stFileUploader {
        background: rgba(255, 0, 64, 0.1);
        border: 2px dashed var(--primary-red);
        border-radius: 0px;
        padding: 20px;
        transition: all 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: var(--neon-red);
        box-shadow: 0 0 15px var(--shadow-color);
    }

    /* Responsive Design Enhancements */
    @media (max-width: 768px) {
        .header-text {
            font-size: 28px;
            letter-spacing: 3px;
        }

        .subheader {
            font-size: 16px;
        }

        .pixelated-border {
            padding: 15px;
            margin: 10px 0;
        }

        .retro-button {
            padding: 12px 20px;
            font-size: 14px;
        }
    }
    </style>

    """, unsafe_allow_html=True)

# Optional: Add particles back later if needed
# st.markdown("""
#     <div class="particles">
#         <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
#         <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
#         <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
#         <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
#         <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
#         <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
#         <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
#         <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
#         <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
#     </div>
# """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'doc_pages' not in st.session_state:
        st.session_state.doc_pages = None
    if 'pdf_name' not in st.session_state:
        st.session_state.pdf_name = None
    if 'chain' not in st.session_state:
        st.session_state.chain = None
    if 'llm' not in st.session_state:
        st.session_state.llm = None

def format_conversation_history():
    if not st.session_state.conversation_history:
        return "No previous conversation."

    formatted_history = ""
    for i, (user_msg, ai_response) in enumerate(st.session_state.conversation_history, 1):
        formatted_history += f"\n--- Exchange {i} ---\n"
        formatted_history += f"User: {user_msg}\n"
        formatted_history += f"Assistant: {ai_response[:300]}..."  # Truncate long responses
        formatted_history += "\n"

    return formatted_history

def process_pdf(uploaded_file):
    """Process uploaded PDF file"""
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Load and split PDF
        loader = PyPDFLoader(file_path=temp_path)
        pages = loader.load_and_split()

        # Clean up temp file
        os.remove(temp_path)

        return pages
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def main():
    load_css()
    init_session_state()

    # Header
    st.markdown('<h1 class="header-text">📚 BOOK MASTER</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">YOUR PDF AI ASSISTANT</p>', unsafe_allow_html=True)

    # PDF Upload Section
    st.markdown('<div class="pixelated-border">', unsafe_allow_html=True)
    st.markdown("### 📤 UPLOAD PDF FILE")
    uploaded_file = st.file_uploader(
        "SELECT YOUR PDF DOCUMENT",
        type=['pdf'],
        help="Choose a PDF file to analyze"
    )

    if uploaded_file is not None and st.session_state.pdf_name != uploaded_file.name:
        with st.spinner("PROCESSING PDF..."):
            doc_pages = process_pdf(uploaded_file)
            if doc_pages:
                st.session_state.doc_pages = doc_pages
                st.session_state.pdf_name = uploaded_file.name

                # Initialize LLM and chain
                st.session_state.llm = init_chat_model(
                    "gemini-1.5-flash",
                    model_provider="google_genai",
                    temperature=0.3,
                    google_api_key=GEMINI_API_KEY
                )

                # Create prompt
                system_prompt = """
                You are a helpful, very friendly, kind and patient assistant that can answer questions about the following documents: {query}
                You will be given a query and a document, plus the conversation history for context.

                IMPORTANT RULES FOR YOU TO FOLLOW:
                -If the user just says to summarize the document but NO SPECIFIC SECTION, you should give them a very detailed and pedagogic summary of the document, omitting as little information as possible. (For example, they might ask you to summarize the document, you should give them a very detailed summary of the document).
                -If the user asks for a summary of a section of the document, you should give them a very detailed and pedagogic summary of the section, omitting as little information as possible. (For example, they might ask you to summarize the derivatives part of the document, you should give them a very detailed summary of the derivatives part of a math textbook).
                -If the user asks for a test, you should give them 3 questions or exercises of increasing difficulty based on the document. You might get inspiration of exercises from the document to create the test (if any). If the document is about Comp Sci and doesn't have code, you may create the exercises based on the concepts of the document but with some coding exercises. EXAMPLE: If the section grasped on A* algorithm but doesn't have some code exercises, you might create a problem to be solved using A* algorithm.
                -You should only give the test if the user asks for it. You should not create a test if the user doesn't ask for it.
                -You should only give the summary if the user asks for it. You should not create a summary if the user doesn't ask for it.
                -If the user query does not fit any of the above categories, you might respond normally to the query.

                CONVERSATION HISTORY (for context):
                {conversation_history}

                Current user query: {query}
                """

                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{context}")
                ])

                st.session_state.chain = create_stuff_documents_chain(st.session_state.llm, prompt)

                st.success("✅ PDF PROCESSED SUCCESSFULLY!")

    st.markdown('</div>', unsafe_allow_html=True)

    # File info display
    if st.session_state.pdf_name:
        st.markdown(f"""
        <div class="file-info">
        📄 CURRENT FILE: {st.session_state.pdf_name}<br>
        📊 PAGES LOADED: {len(st.session_state.doc_pages) if st.session_state.doc_pages else 0}
        </div>
        """, unsafe_allow_html=True)

    # Conversation Section
    if st.session_state.chain and st.session_state.doc_pages:
        st.markdown('<div class="pixelated-border">', unsafe_allow_html=True)
        st.markdown("### 💬 CONVERSATION")

        # Display conversation history
        if st.session_state.conversation_history:
            st.markdown(f'<p class="status-text">💾 CONVERSATION HISTORY: {len(st.session_state.conversation_history)} EXCHANGES</p>', unsafe_allow_html=True)

            for i, (user_msg, ai_response) in enumerate(st.session_state.conversation_history, 1):
                st.markdown(f"""
                <div class="conversation-bubble user-message">
                <strong>YOU:</strong> {user_msg}
                </div>
                <div class="conversation-bubble ai-message">
                <strong>AI:</strong> {ai_response}
                </div>
                """, unsafe_allow_html=True)

        # Query input
        with st.form(key='query_form'):
            user_query = st.text_area(
                "ENTER YOUR QUERY:",
                height=100,
                placeholder="Ask me anything about the document...",
                help="Type your question or request here"
            )

            submit_button = st.form_submit_button(
                "🚀 SEND QUERY",
                use_container_width=True
            )

        if submit_button and user_query.strip():
            if user_query.lower() in ['quit', 'exit', 'bye']:
                st.warning("Goodbye! Thanks for using Book Master!")
                return

            try:
                with st.spinner("AI IS THINKING..."):
                    result = st.session_state.chain.invoke({
                        "query": user_query,
                        "context": st.session_state.doc_pages,
                        "conversation_history": format_conversation_history()
                    })

                # Add to conversation history
                st.session_state.conversation_history.append((user_query, result))

                # Limit history to last 10 exchanges
                if len(st.session_state.conversation_history) > 10:
                    st.session_state.conversation_history = st.session_state.conversation_history[-10:]

                st.rerun()

            except Exception as e:
                st.error(f"❌ ERROR: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="pixelated-border">
        <h3 style="color: var(--secondary-red); text-align: center; font-family: 'Courier New', monospace;">
        📤 UPLOAD A PDF FILE TO BEGIN
        </h3>
        <p style="text-align: center; color: var(--light-red); font-family: 'Courier New', monospace;">
        Choose a PDF document from the uploader above to start your AI conversation!
        </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
