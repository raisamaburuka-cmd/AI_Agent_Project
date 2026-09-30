import streamlit as st
from google import genai
from dotenv import load_dotenv
from tools import run_tool, get_tool_definitions
from gtts import gTTS
import speech_recognition as sr
import io
import os


# Load environment variables
load_dotenv()


# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def text_to_speech(text):
    """Convert text response to speech."""
    audio_buffer = io.BytesIO()

    tts = gTTS(text=text, lang="en")
    tts.write_to_fp(audio_buffer)

    audio_buffer.seek(0)

    return audio_buffer

def speech_to_text(audio_data):
    """Convert recorded audio into text."""
    recognizer = sr.Recognizer()

    try:
        audio_bytes = audio_data.getvalue()

        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        st.warning("🎤 I couldn't understand the audio. Please try again.")
        return ""

    except sr.RequestError as e:
        st.warning(f"🌐 Speech recognition service is unavailable: {e}")
        return ""

    except Exception as e:
        st.warning(f"⚠️ Could not process the audio: {e}")
        return ""

# Streamlit page configuration
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖"
)

# Sakura Theme 🌸
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Poppins:wght@300;400;500;600&display=swap');

/* Main application */
.stApp {
    background: linear-gradient(135deg, #fffafd 0%, #fdf6fb 50%, #f8f4fc 100%);
    color: #3f3a42;
    font-family: 'Poppins', sans-serif;
}

/* 🌸 Sakura page background */
.stApp {
    background: linear-gradient(
        135deg,
        #fffafd 0%,
        #fdf3f8 50%,
        #f7eef6 100%
    ) !important;
}

/* 🌸 Sakura layout spacing */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 900px !important;
}

/* 🌸 Chat text visibility */
[data-testid="stChatMessage"] p {
    color: #3f3540 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
}

[data-testid="stChatMessage"] {
    color: #3f3540 !important;
}

/* 🌸 Soft Sakura content glow */
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Main title */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 600 !important;
    color: #8f5f78 !important;
    letter-spacing: 0.5px;
}

/* 🌸 Sakura title */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #8f5f78 !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}

/* 🌸 Subtitle */
.stApp p {
    font-family: 'Poppins', sans-serif !important;
}

/* Section headings */
h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #8f5f78 !important;
}

/* Normal text */
p, label, .stMarkdown {
    font-family: 'Poppins', sans-serif;
}

/* 🌸 Modern Sakura Messaging Interface */

/* Message row */
[data-testid="stChatMessage"] {
    width: 100% !important;
    display: flex !important;
    margin-bottom: 14px !important;
    padding: 0 !important;
    background: transparent !important;
    border: none !important;
}

/* 🌸 USER MESSAGE — RIGHT */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
}

/* 🪻 AGENT MESSAGE — LEFT */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    flex-direction: row !important;
    justify-content: flex-start !important;
}

/* Message bubble */
[data-testid="stChatMessage"] > div:last-child {
    max-width: 72% !important;
    padding: 13px 17px !important;
    box-sizing: border-box !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    border-radius: 20px !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:last-child {
    background: #f7dce9 !important;
    border: 1px solid #e8bfd1 !important;
    border-radius: 20px 20px 5px 20px !important;
    margin-left: auto !important;
    margin-right: 0 !important;
}

/* Agent bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:last-child {
    background: #e9e1f0 !important;
    border: 1px solid #d4c5df !important;
    border-radius: 20px 20px 20px 5px !important;
    margin-left: 0 !important;
    margin-right: auto !important;
}
/* Message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em {
    color: #29242c !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

/* Message headings */
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] h5,
[data-testid="stChatMessage"] h6 {
    color: #29242c !important;
}

/* Code blocks */
[data-testid="stChatMessage"] pre {
    background: #f5f2f7 !important;
    color: #29242c !important;
    white-space: pre-wrap !important;
    overflow-x: auto !important;
    border: 1px solid #d8cfe0 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

[data-testid="stChatMessage"] pre code {
    background: transparent !important;
    color: #29242c !important;
}

/* Prevent long messages from overflowing */
[data-testid="stChatMessage"] * {
    max-width: 100% !important;
    overflow-wrap: anywhere !important;
}

/* Message text */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em {
    color: #29242c !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}

/* Message headings */
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] h5,
[data-testid="stChatMessage"] h6 {
    color: #29242c !important;
}

/* Long messages */
[data-testid="stChatMessage"] * {
    max-width: 100% !important;
    overflow-wrap: anywhere !important;
}

/* Code blocks */
[data-testid="stChatMessage"] pre {
    background: #f5f2f7 !important;
    color: #29242c !important;
    white-space: pre-wrap !important;
    overflow-x: auto !important;
    border: 1px solid #d8cfe0 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

/* Code text */
[data-testid="stChatMessage"] pre code {
    background: transparent !important;
    color: #29242c !important;
}
/* 🌸 User message — RIGHT side */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    justify-content: flex-end !important;
}

/* 🪻 AI message — LEFT side */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    justify-content: flex-start !important;
}

/* Message content area */
[data-testid="stChatMessage"] > div:last-child {
    max-width: 72% !important;
    padding: 13px 17px !important;
    border-radius: 20px !important;
    box-sizing: border-box !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
}

/* 🌸 User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:last-child {
    background: #f7dce9 !important;
    border: 1px solid #e8bfd1 !important;
    border-radius: 20px 20px 5px 20px !important;
    margin-left: auto !important;
    color: #493b43 !important;
}

/* 🪻 AI Agent bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:last-child {
    background: #e9e1f0 !important;
    border: 1px solid #d4c5df !important;
    border-radius: 20px 20px 20px 5px !important;
    margin-right: auto !important;
    color: #403744 !important;
}

/* Message text */
[data-testid="stChatMessage"] p {
    color: inherit !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}

/* Prevent long content from overflowing */
[data-testid="stChatMessage"] * {
    max-width: 100% !important;
    overflow-wrap: anywhere !important;
}

/* Keep code blocks readable */
[data-testid="stChatMessage"] pre {
    white-space: pre-wrap !important;
    overflow-x: auto !important;
}
/* Text input */
.stChatInput {
    border-radius: 18px;
}

/* Buttons */
.stButton > button {
    border-radius: 14px;
    border: 1px solid #e8c8d9;
    background: #fff7fb;
    color: #8f5f78;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    transition: 0.2s ease;
}

/* 🌸 Sakura Send button */
[data-testid="stChatInput"] button {
    background: #d9a7bf !important;
    color: #ffffff !important;
    border: 1px solid #c98eac !important;
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
}

[data-testid="stChatInput"] button:hover {
    background: #c98eac !important;
    color: #ffffff !important;
}

.stButton > button:hover {
    border-color: #d8a9c1;
    background: #fcecf5;
}

/* 🌸 Sakura expanders */
[data-testid="stExpander"] {
    border: 1px solid #ead3df !important;
    border-radius: 16px !important;
    background: rgba(255, 250, 253, 0.82) !important;
    box-shadow: 0 3px 12px rgba(180, 130, 155, 0.06) !important;
    margin-bottom: 12px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Poppins', sans-serif !important;
    color: #8f5f78 !important;
    font-weight: 500 !important;
}

[data-testid="stExpander"] summary:hover {
    color: #b27696 !important;
}

/* Checkbox */
[data-testid="stCheckbox"] label {
    font-family: 'Poppins', sans-serif;
}

/* Captions */
.stCaption {
    color: #8b7a85;
}

/* 🌸 Decorative Sakura divider */
.sakura-divider {
    text-align: center;
    color: #d89ab8;
    font-size: 18px;
    letter-spacing: 10px;
    margin: 6px 0 22px 0;
    opacity: 0.85;
    text-shadow: 0 2px 8px rgba(216, 154, 184, 0.18);
}

/* 🌸 Sakura chat input */
[data-testid="stChatInput"] {
    background: #fff7fb !important;
    border: 1px solid #e7bfd3 !important;
    border-radius: 18px !important;
    box-shadow: 0 3px 12px rgba(180, 130, 155, 0.08) !important;
}

[data-testid="stChatInput"] > div {
    background: #fff7fb !important;
    border-radius: 18px !important;
}

[data-testid="stChatInput"] textarea {
    background: #fff7fb !important;
    color: #4a4148 !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #a98d9d !important;
}

/* 🌸 Clear chat text */
[data-testid="stChatMessage"] p {
    color: #3f3540 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
}

/* 🌸 Sakura area behind the typing bar */
[data-testid="stBottom"] {
    background: #f3e8f0 !important;
}

[data-testid="stBottom"] > div {
    background: #f3e8f0 !important;
}

/* 🌸 Sakura microphone input */
[data-testid="stAudioInput"] {
    background: #fff7fb !important;
    border: 1px solid #e7bfd3 !important;
    border-radius: 18px !important;
    padding: 10px !important;
    box-shadow: 0 3px 12px rgba(180, 130, 155, 0.08) !important;
}

/* 🌸 Sakura microphone button */

[data-testid="stAudioInput"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

/* Microphone control */
[data-testid="stAudioInput"] > div {
    background: #f4d7e5 !important;
    border: 1px solid #e7bfd3 !important;
    border-radius: 16px !important;
    padding: 0 !important;
    width: 52px !important;
    height: 52px !important;
    min-width: 52px !important;
    box-shadow: 0 3px 10px rgba(180, 130, 155, 0.12) !important;
}

/* Microphone button */
[data-testid="stAudioInput"] button {
    width: 52px !important;
    height: 52px !important;
    border-radius: 16px !important;
    background: #f4d7e5 !important;
    border: none !important;
    color: #8f5f78 !important;
    padding: 0 !important;
}

/* Hover */
[data-testid="stAudioInput"] button:hover {
    background: #edc5d8 !important;
    border-color: #d8a9c1 !important;
}

/* Recording state */
[data-testid="stAudioInput"] button:active {
    background: #e5b8cf !important;
}

[data-testid="stAudioInput"] > div {
    background: #fff7fb !important;
    border-radius: 18px !important;
}

[data-testid="stAudioInput"] button {
    background: #f4d7e5 !important;
    color: #8f5f78 !important;
    border: 1px solid #e7bfd3 !important;
    border-radius: 12px !important;
}

[data-testid="stAudioInput"] button:hover {
    background: #edc5d8 !important;
}

/* 🌸 Recording timer */
[data-testid="stAudioInput"] [data-testid="stAudioInputTime"] {
    color: #8f5f78 !important;
    background: #fff7fb !important;
}

[data-testid="stAudioInput"] [role="timer"] {
    color: #8f5f78 !important;
    background: #fff7fb !important;
}

[data-testid="stAudioInput"] time {
    color: #8f5f78 !important;
    background: #fff7fb !important;
}

/* 🌸 Audio player */
audio {
    border-radius: 12px;
}

[data-testid="stAudioInput"] button:hover {
    background: #edc5d8 !important;
}

/* 🌸 Sakura recording timer */
[data-testid="stAudioInputWaveformTimeCode"] {
    color: #8f5f78 !important;
    background: #fff7fb !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

/* 🌸 FINAL CHAT ALIGNMENT */

/* User message */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    margin-left: auto !important;
    margin-right: 0 !important;
    width: 100% !important;
}

/* User bubble content */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) > div:last-child {
    margin-left: auto !important;
    margin-right: 0 !important;
    text-align: left !important;
}

/* Agent message */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    margin-left: 0 !important;
    margin-right: auto !important;
    width: 100% !important;
}

/* Agent bubble content */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) > div:last-child {
    margin-left: 0 !important;
    margin-right: auto !important;
    text-align: left !important;
}

/* 🌸 Place microphone beside chat input */

[data-testid="stAudioInput"] button {
    width: 46px !important;
    height: 46px !important;
    border-radius: 14px !important;
    background: #f4d7e5 !important;
    border: 1px solid #e7bfd3 !important;
    color: #8f5f78 !important;
    box-shadow: 0 3px 10px rgba(180, 130, 155, 0.15) !important;
}

[data-testid="stAudioInput"] button:hover {
    background: #edc5d8 !important;
}

/* Microphone button */
[data-testid="stAudioInput"] button {
    width: 46px !important;
    height: 46px !important;
    border-radius: 14px !important;
    background: #f4d7e5 !important;
    border: 1px solid #e7bfd3 !important;
    color: #8f5f78 !important;
    box-shadow: 0 3px 10px rgba(180, 130, 155, 0.15) !important;
}

/* Hover */
[data-testid="stAudioInput"] button:hover {
    background: #edc5d8 !important;
}

/* Audio player */
audio {
    border-radius: 12px;
}

/* 🌸 Position microphone beside the chat input */
[data-testid="stAudioInput"] {
    position: fixed !important;
    left: calc(50% + 125px) !important;
    bottom: 58px !important;
    z-index: 999 !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}

/* 🌸 Microphone button */
[data-testid="stAudioInput"] button {
    width: 46px !important;
    height: 46px !important;
    min-width: 46px !important;
    border-radius: 14px !important;
    background: #f4d7e5 !important;
    border: 1px solid #e7bfd3 !important;
    color: #8f5f78 !important;
    box-shadow: 0 3px 10px rgba(180, 130, 155, 0.15) !important;
}

[data-testid="stAudioInput"] button:hover {
    background: #edc5d8 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="sakura-divider">🌸 ✿ 🌸 ✿ 🌸</div>',
    unsafe_allow_html=True
)

# Page title
st.title("🤖 Intelligent AI Agent")
st.write("Ask me anything using text or voice!")

enable_voice = st.checkbox(
    "🔊 Enable voice responses",
    value=True
)

st.caption("💬 Conversation memory is enabled for this session.")

if st.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

with st.expander("✨ Agent Capabilities"):
    st.markdown("""
    - 💬 Conversational interaction
    - 🧠 Conversation memory
    - 🧮 Mathematical calculations
    - 🎤 Speech-to-Text voice input
    - 🔊 Text-to-Speech voice responses
    - 🕐 Current date and time
    - 🔊 Text-to-Speech responses
    - 🤖 Gemini-powered AI responses
    """)

with st.expander("📖 About This Project"):
    st.write(
        "This project is an Intelligent AI Agent with conversational "
        "interaction and Text-to-Speech. It uses Gemini as the large "
        "language model and integrates local tools for calculations "
        "and current date/time information. The agent maintains "
        "conversation context during the session and can convert "
        "AI-generated responses into speech."
    )

# Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    if message["role"] == "user":
        avatar = "🌸"
    else:
        avatar = "🪻"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.write(message["content"])


# Chat input
audio_input = st.audio_input(
    "Microphone",
    label_visibility="collapsed"
)

user_message = st.chat_input("Type your message or use the microphone...")

if audio_input is not None:
    spoken_text = speech_to_text(audio_input)

    if spoken_text:
        user_message = spoken_text

if user_message:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

        # Display user message
    with st.chat_message("user", avatar="🌸"):
        st.write(user_message)

    try:

        # Build conversation history
        conversation = []

        for message in st.session_state.messages:
            conversation.append(
                f'{message["role"]}: {message["content"]}'
            )

        prompt = "\n".join(conversation)

        # Get available tools
        tools = get_tool_definitions()

        # Send request to Gemini
        status = st.empty()
        status.info("🤔 Thinking...")
        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
            tools=tools,
            system_instruction=(
                "You are an intelligent conversational AI agent. "
                "Answer the user's questions clearly, accurately, and helpfully. "
                "Maintain context from the conversation when appropriate. "
                "Use the calculator tool for mathematical calculations instead of "
                "calculating manually. "
                "Use the get_current_datetime tool when the user asks for the "
                "current date or time. "
                "Explain answers in a clear and easy-to-understand way. "
                "For general questions, answer normally without using tools. "
                "If a request cannot be completed, explain the limitation clearly."
            )
        )
        status.empty()
        # Check whether Gemini requested a tool
        function_call = None

        for step in response.steps:
            if step.type == "function_call":
                function_call = step
                break

        # If a tool was requested
        if function_call:

            result = run_tool(
                function_call.name,
                function_call.arguments
            )

            # Send tool result back to Gemini
            final_response = client.interactions.create(
                model="gemini-3.6-flash",
                previous_interaction_id=response.id,
                input=[
                    {
                        "type": "function_result",
                        "name": function_call.name,
                        "call_id": function_call.id,
                        "result": str(result)
                    }
                ],
                tools=tools
            )

            ai_response = final_response.output_text

        else:
            # Normal response
            ai_response = response.output_text

        # Store AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })

                       # Display AI response
        with st.chat_message("assistant", avatar="🪻"):
            st.write(ai_response)

            # Generate voice response if enabled
            if enable_voice:
                audio = text_to_speech(ai_response)
                st.audio(audio, format="audio/mp3")

    except Exception as e:

        with st.chat_message("assistant", avatar="🪻"):
            st.error(f"Error: {e}")