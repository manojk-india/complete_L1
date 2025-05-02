# This ill be the entry file for the L1 level query 
# Standard imports 
import os
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel
from dotenv import load_dotenv

# custom imports 
from utils import *
from crews import *


# loading the environment variables from the .env file
load_dotenv()

# get the user query 
Query=input("Enter your L1 level query ( please ask for one thing at a time ): ")

# classify the user query as some predefined categories
sim_query,sim,idx,previous_needed_or_not=embed_query(Query)

write_to_checkpoint_file(str(datetime.now()))
write_to_checkpoint_file("user query is : "+str(Query))
write_to_checkpoint_file("sim_query is : "+str(sim_query))
write_to_checkpoint_file("previous_needed_or_not is : "+str(previous_needed_or_not))

# calling the data getter crew to extract the relevant information from the user query
result=parameter_extracter_crew(Query)

# calling the main API function 
get_L1_board_data(result["board_name"],previous_needed_or_not,result["sprint_name"],result["person_name"])


























# print(query_info)
# # so here in query we will have board 
# name ( compulsory ), person name ( optional ), and the sprint name ( optional )
# board=find_present_words_case_insensitive(Query)
# print("board name is : "+str(board))
# if board:
#     board_id=get_board_id(board) 
#     write_to_checkpoint_file("board name is : "+str(board))
#     write_to_checkpoint_file("board id is : "+str(board_id))
# else:
#     write_to_checkpoint_file("Error: Board name cannot be None.")

# board name should not be none ...so handle that error in the future






