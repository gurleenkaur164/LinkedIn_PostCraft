import os
from crewai import Agent
from langchain_groq import ChatGroq
from tools import web_search
from dotenv import load_dotenv

load_dotenv()

llm= ChatGroq(
    model= "llama3-70b-8192",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)
#researcher agent

researcher= Agent(
    role="LinkedIn Content Researcher",
    goal=("Research the latest insights, trends, and data on the given topic to create an engaging LinkedIn post. Find 3-5" \
    "compelling angles and relatable professional pain points with real-world examples to make the post worth sharing."),
    backstory=(
        "You are a senior content strategist with 10+ years of experience studying what makes LinkedIn posts go viral. You have an encyclopedic knowledge of professional trends. You always find the angle nobody else is talking about."
    ),
    llm=llm,
    tools=[web_search], verbose=True,
    allow_delegation= False,
    max_iter=3

)

#writer agent
writer=Agent(
    role="LinkedIn Post Content Writer",
    goal=(
        "Draft an engaging, first-person LinkedIn post based on the researcher's findings. The post should be engaging, concise and properlly formatted. "
    ),
    backstory=(
        "You are a ghostwriter for top LinkedIn creators with 500K+ followers. You have written posts that have generated many impressions. Your secret: you write like a human, not a marketer. You never use corporate jargon, buzzwords or cliches."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

#editor agent
editor=Agent(
    role="LinkedIn Post Editor & Hashtag Specialist",
    goal=(
        "Polish the draft of the writer agent and check for any grammatical errors or formatting issues. Then, add 3-5 relevant hashtags that will increase the visibility of the post without making it look spammy."

    ),
    backstory=(
        "You are a formar top-tier editor for a digital media compan. You have an eye for details and you know that most of the readers dont even click on 'see more'. You are a grammar specialist and you know what drives impactful LinkedIn content."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=3
)

