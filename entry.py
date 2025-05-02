# This ill be the entry file for the L1 level query 
# Standard imports 
import os
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd

# custom imports 
from utils import *
from crews import *


# # loading the environment variables from the .env file
# load_dotenv()

# # get the user query 
# Query=input("Enter your L1 level query ( please ask for one thing at a time ): ")

# # classify the user query as some predefined categories
# sim_query,sim,idx,previous_needed_or_not=embed_query(Query)

# write_to_checkpoint_file(str(datetime.now()))
# write_to_checkpoint_file("user query is : "+str(Query))
# write_to_checkpoint_file("sim_query is : "+str(sim_query))
# write_to_checkpoint_file("previous_needed_or_not is : "+str(previous_needed_or_not))

# # calling the data getter crew to extract the relevant information from the user query
# result=parameter_extracter_crew(Query)

# # calling the main API function 
# average=get_L1_board_data(result["board_name"],previous_needed_or_not,result["sprint_name"],result["person_name"],idx)

# now we have data in hand -- current.csv , history.csv, variable average 
pd=pd.read_csv("generated_files/current.csv")

add_rtb_ctb_column(pd)



