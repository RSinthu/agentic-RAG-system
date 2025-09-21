import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import graph, State 
from audio_recorder_streamlit import audio_recorder
import whisper
import tempfile
import os

@st.cache_resource
def load_whisper_model():
    """Loads the Whisper model."""
    model = whisper.load_model("small")
    return model

model = load_whisper_model()

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

def display_chat_history():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

def transcribe_audio(audio_bytes):
    """Transcribe audio using Whisper model."""
    if audio_bytes:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            # Transcribe using Whisper
            result = model.transcribe(tmp_file_path)
            return result["text"]
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
    return ""

def main():
    st.set_page_config(
        page_title="Agentic RAG Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Agentic RAG Chatbot")
    st.markdown("Ask questions about AI agents, research papers, or general topics!")
    
    init_session_state()
    
    with st.sidebar:
        st.header("Available Tools")
        st.markdown("""
        - 📄 **Document Retriever**: Microsoft AI agents article
        - 📚 **Wikipedia**: General knowledge
        - 🔬 **ArXiv**: Academic papers
        - 🌐 **Tavily Search**: Web search
        """)
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.rerun()
    
    # Audio input setup
    col1, col2 = st.columns([10, 1])
    
    with col1:
        prompt = st.chat_input("Ask anything...")
    
    with col2:
        # Audio recorder with microphone styling
        audio_bytes = audio_recorder(
            text="",
            recording_color="#ff4444",
            neutral_color="#666666",
            icon_name="microphone",
            icon_size="2x",
            auto_start=False,
            pause_threshold=2.0,
            sample_rate=16000
        )

    # Handle audio input
    if audio_bytes and audio_bytes != st.session_state.get("last_audio", None):
        st.session_state.last_audio = audio_bytes
        with st.spinner("🎤 Transcribing audio..."):
            transcribed_text = transcribe_audio(audio_bytes)
            if transcribed_text.strip():
                prompt = transcribed_text
    
    # Process new user input
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner("Thinking..."):
            try:
                all_messages = []
                for msg in st.session_state.conversation_history:
                    all_messages.append(msg)
                all_messages.append(HumanMessage(content=prompt))
                
                response = graph.invoke({"messages": all_messages})
                
                ai_response = ""
                for msg in response["messages"]:
                    if isinstance(msg, AIMessage):
                        ai_response = msg.content
                
                st.session_state.conversation_history.extend(response["messages"])
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Display all chat history (this will show all messages in order)
    display_chat_history()

if __name__ == "__main__":
    main()