# This ill be the entry file for the L1 level query 
# Standard imports 
import os
from crewai import Agent, Task, Crew, LLM
from pydantic import BaseModel
from dotenv import load_dotenv

# custom imports 
from utils import *


# loading the environment variables from the .env file
load_dotenv()


# Query=input("Enter your L1 level query ( you can only ask for one thing at a time ): ")
# print(get_previous_sprint_ids("cdf", 64))
print(api_helper(71,jql=None,output_file="generated_files/current.json"))
# sim_query,sim,idx=embed_query(Query)

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






