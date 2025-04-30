# here is where crewai agents , tasks and crews are defined with their entry functions 

# imports 
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

# Initialize LLM model from sambanova 
llm = LLM(
    model="sambanova/DeepSeek-R1-Distill-Llama-70B",
    temperature=0.1,
    max_tokens=2048
)


# Building tools -- Uma question : Is really tool calling required , cant we do it manually like we dit it for feature readiness ?
# Its a matter we have to think abt 



