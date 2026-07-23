from langchain_groq import ChatGroq

from core.config import GROQ_API_KEY

# ChatGroq is LangChain's chat-model wrapper for Groq; Groq is used here for fast,
# low-latency LLM reasoning in routing and conversational response generation.
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=GROQ_API_KEY,
)
