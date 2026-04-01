from crewai_tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

duckduckgosearch= DuckDuckGoSearchRun()  

@tool("web_search")
def web_search(query: str)->str:
    """ Search the web for current information on a topic.
    Use DuckDuckGo- it is completely free and no API key is required.

    Args:
        query: The search query string.
    Returns: 
        Search results as a string.


    """
    try:
        results=duckduckgosearch.run(query)
        return results
    except Exception as e:
        return f"Search failed: {str(e)}. Please try a different query."