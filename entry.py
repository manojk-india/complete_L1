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


Query=input("Enter your L1 level query ( you can only ask for one thing at a time ): ")


# so here in query we will have board name ( compulsory ), person name ( optional ), and the sprint name ( optional )
board=find_present_words_case_insensitive(Query)
board_id=get_board_id(board) 

# board name should not be none ...so handle that error in the future
write_to_checkpoint_file("board name is : "+str(board))
write_to_checkpoint_file("board id is : "+str(board_id))






