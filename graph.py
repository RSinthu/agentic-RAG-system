from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import Tool
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import List, Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from langchain_community.document_loaders import WebBaseLoader
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt import ToolNode, tools_condition
from typing import List, Annotated
from langgraph.graph.message import add_messages
from pydantic import BaseModel

load_dotenv()

parser = StrOutputParser()

llm = ChatGroq(model="openai/gpt-oss-120b")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

arxiv_api_wrapper = ArxivAPIWrapper(top_k_results=3,doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=arxiv_api_wrapper)

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=3,doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

docs = WebBaseLoader("https://news.microsoft.com/source/features/ai/ai-agents-what-they-are-and-how-theyll-change-the-way-we-work/").load()
textSplitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunks = textSplitter.split_documents(docs)

vectordb = FAISS.from_documents(chunks,embedding_model)
retriever = vectordb.as_retriever()

retriever_tool = Tool(
    name="document_retriever",
    description="Retrieves relevant documents about AI agents from Microsoft news article",
    func=retriever.invoke
)

tools = [retriever_tool, wiki, arxiv, tavily_search_tool]

react_node = create_react_agent(llm, tools)

class State(BaseModel):
    messages: Annotated[List[AnyMessage],add_messages]

builder = StateGraph(State)

builder.add_node("agentNode",react_node)
builder.add_node("tools",ToolNode(tools))

builder.set_entry_point("agentNode")
builder.add_conditional_edges("agentNode",tools_condition),
builder.add_edge("tools", "agentNode")

graph = builder.compile()


messages = graph.invoke({"messages":HumanMessage("AI agents from Microsoft news article")})

for m in messages["messages"]:
    m.pretty_print()