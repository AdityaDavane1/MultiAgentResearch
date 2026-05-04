from typing import TypedDict
from langgraph.graph import StateGraph, END

from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-3.5-turbo"
)


class ResearchState(TypedDict):
    topic: str
    research: str
    analysis: str
    report: str


def research_node(state: ResearchState):
    print("Researching...") 
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result = client.search(state["topic"])
    state["research"] = str(result)
    return state


def analyze_node(state: ResearchState):
    print("Analyzing...")
    result = llm.invoke(f"Analyze this research and extract key points: {state['research']}")
    state["analysis"] = result.content
    return state

def writer_node(state: ResearchState):
    print("Writing report...")
    result = llm.invoke(f"""
    Based on this analysis, write a clean and well-structured research report.
    
    - Do NOT use numbered lists
    - Write in proper paragraphs
    - Use headings like Introduction, Key Insights, Conclusion
    - Make it easy to read
    
    Analysis: {state['analysis']}
    """)
    state["report"] = result.content
    return state


graph = StateGraph(ResearchState)


graph.add_node("research", research_node)
graph.add_node("analyze", analyze_node)
graph.add_node("writer", writer_node)


graph.set_entry_point("research")
graph.add_edge("research", "analyze")
graph.add_edge("analyze", "writer")
graph.add_edge("writer", END)


research_app = graph.compile()