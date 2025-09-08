# 🤖 Agentic RAG Chatbot

An intelligent chatbot that combines Retrieval-Augmented Generation (RAG) with multiple AI tools to provide comprehensive answers from various sources.

## 🌟 Features

- **Multi-Source Knowledge**: Combines information from documents, Wikipedia, ArXiv papers, and web search
- **Intelligent Agent**: Uses ReAct (Reasoning + Acting) pattern to choose appropriate tools
- **Vector Search**: FAISS-powered semantic search for document retrieval
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Real-time Responses**: Fast responses with conversation memory

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| 📄 Document Retriever | Searches Microsoft AI agents article |
| 📚 Wikipedia | General knowledge queries |
| 🔬 ArXiv | Academic paper search |
| 🌐 Tavily Search | Real-time web search |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Required API keys (see Environment Setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AgenticRagChatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`


## 🏗️ Project Structure

```
AgenticRagChatbot/
├── graph.py              # Main agent logic and tools setup
├── streamlit_app.py       # Streamlit web interface
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── readme.md             # This file
└── .gitignore           # Git ignore file
```

## 🔧 Configuration

### API Keys Required

1. **Groq API Key**: Get from [Groq Console](https://console.groq.com/)
2. **Tavily API Key**: Get from [Tavily](https://tavily.com/)

### Model Configuration

The chatbot uses:
- **LLM**: ChatGroq with `openai/gpt-oss-120b` model
- **Embeddings**: HuggingFace `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: FAISS for document indexing


## 🔍 How It Works

1. **User Input**: User asks a question through Streamlit interface
2. **Agent Reasoning**: ReAct agent analyzes the query and selects appropriate tools
3. **Tool Execution**: Agent uses selected tools (retriever, Wikipedia, ArXiv, web search)
4. **Response Generation**: LLM synthesizes information from all sources
5. **Output**: Comprehensive answer displayed to user

## 🚨 Troubleshooting

**Common Issues:**

1. **API Key Errors**: Ensure all API keys are set in `.env` file
2. **Model Loading**: First run may take time to download embedding models
3. **Port Issues**: If 8501 is busy, Streamlit will suggest alternative ports

**Debug Mode:**
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the framework
- [LangGraph](https://langgraph-python.readthedocs.io/) for agent orchestration
- [Streamlit](https://streamlit.io/) for the web interface
- [Groq](https://groq.com/) for fast LLM inference
- [HuggingFace](https://huggingface.co/) for embeddings
