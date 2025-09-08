import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph import graph, State 

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
    
    display_chat_history()
    
    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
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
                    
                    st.markdown(ai_response)
                    
                    st.session_state.conversation_history.extend(response["messages"])
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()