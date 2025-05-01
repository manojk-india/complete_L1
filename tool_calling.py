from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from dotenv import load_dotenv
from utils import *
import requests
import json
import os
from requests.auth import HTTPBasicAuth


load_dotenv()

# Initialize LLM model from sambanova 
llm = LLM(
    model="sambanova/DeepSeek-R1-Distill-Llama-70B",
    temperature=0.1,
    max_tokens=2048
)



@tool("API caller")
def get_L1_board_data(board_name:str, previous_data_needed_or_not: bool, sprint: str = " ",person: str=" ") -> None:
    """ pass the board name and the output file , the sprint name and the person name to the tool to get the L1 board data in the output file 
    Args:
        board_name (str): The name of the board. eg:cdf
        sprint (str, optional): The name of the sprint. Not just the number like 5, 6, etc. Defaults to None. eg. sprint 1,sprint 2,sprint 8 etc.
        person (str, optional): The name of the person. Defaults to None. eg. manoj
    """
    write_to_checkpoint_file("function called with parameters "+"board name "+str(board_name)+" sprint name "+str(sprint))
 

    if( sprint==" " or sprint==None  or sprint=="None"):
        sprint_name = get_current_sprint()
        sprint_id = get_sprint_id(board_name, sprint_name)
        write_to_checkpoint_file("sprint id is "+str(sprint_id)+ " sprint name is "+str(sprint_name))
    else:
        sprint_id=get_sprint_id(board_name,sprint)
        write_to_checkpoint_file("sprint id is "+str(sprint_id)+ " sprint name is "+str(sprint))

    if( person!=" "):
        jql=f"assignee={person}"
    else:
        jql=None

    api_helper(sprint_id,jql,"generated_files/current.json")

    # If previous data is needed 
    if previous_data_needed_or_not:
        # getting previous 6 sprint id for the given board name , sprintid
        sprint_ids = get_previous_sprint_ids(board_name, sprint_id)
        for i in sprint_ids:
            api_helper(i,jql,"generated_files/history.json") 


        
   

    
agent = Agent(
    role="L1 Board Data Retriever",
    goal="Extract parameters from user query and call the L1 board data API tool.",
    backstory="You are an expert at understanding queries about boards, sprints, and people, and using tools to fetch data.",
    tools=[get_L1_board_data],
    llm=llm,
    verbose=True
)

task = Task(
    description=(
        """Given a user query {query}, extract the board name, sprint, and person if present
        then call the API caller tool to fetch L1 board data and pass the previous_data_needed_or_not as {flag}."""
    ),
    agent=agent,
    expected_output="L1 board data saved in generated_files/current.json"
)

crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff(inputs={"query":" in sprint 8 tell me the number of story points assigned to Hari","flag":True})	




# inferences .....

# max to max two files to query -- current date( particular) , history ( maybe )