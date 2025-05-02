from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from dotenv import load_dotenv
from utils import *
from models import *
import pandas as pd


load_dotenv()

# Initialize LLM model from sambanova 
llm = LLM(
    model="sambanova/DeepSeek-R1-Distill-Llama-70B",
    temperature=0.1,
    max_tokens=2048
)


############################################################################################ code for parameter getter crew and agents


agent = Agent(
    role="Query analysis expert",
    goal="Extract parameters from user query by understanding the users query clearly",
    backstory="You are an expert at understanding queries about boards, sprints, and people",
    llm=llm,
    verbose=True
)

task = Task(
    description=(
        """Given a user query {query}, extract the board name, sprint, and person if present"""
    ),
    agent=agent,
    output_pydantic=info,
    expected_output="""extracted parameters
    1) board_name: eg cdf 
    2) person_name: eg Hari or None
    3) sprint_name: eg sprint 8 or None
    """
)

def parameter_extracter_crew(query:str) -> None:
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff(inputs={"query": query})
    return result

################################################################################################################################################


# inferences .....
# max to max two files to query -- current date( particular) , history ( maybe ) -- complete done 