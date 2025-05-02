from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool
from dotenv import load_dotenv
from utils import *
from models import *
from prompts import *
import pandas as pd


load_dotenv()

# Initialize LLM model from sambanova 
llm = LLM(
    model="sambanova/DeepSeek-R1-Distill-Llama-70B",
    temperature=0.9,
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
    description="""Given a user query {query}, extract the board name, sprint, and person if present""",
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
# max to max two files to query -- current date( particular) , history ( maybe ) , avg -- complete done 
    

pandas_agent = Agent(
        role="Pandas Query Agent",
        goal="Generate and execute Pandas queries from user requests.",
        backstory="You are a data expert specializing in analyzing and extracting information from Pandas DataFrames.",
        llm=llm,
        verbose=True,
    )

query_task = Task(
            description="""Convert the user query User Query given in {prompt2} into a pandas code by understanding the csv file structure
            to query out specific need of the user and saving it into a text file named output.txt""",
            agent=pandas_agent,
            expected_output="A pandas code to query out specific need of the user and saving it into a text file named output.txt",
        )

def pandas_query_crew(query:str):
    
    prompt2 = f"""
            You are given a CSV file with structure {df_structure_main}
            Analyze the data and provide a concise pandas code that should run on output.csv file to query the result and also
            to save it in a output.txt file .

            User Query: "{query}"

            output should be in this format there should be code start and code end like given below 
            If they ask you to count anything then dont try to filter the dataframe . use df functions 
            Dont create any new dataframe after df ..assume every needed data is already filtered out in df and use it to calculate
            Dont use any other dataframe name other than df
            eg: df = pd.read_csv("generated_files/output.csv")
            df = pd.read_csv("generated_files/output.csv") always use this 
            eg num_rows = len(df)
            eg column_sum = df["your_column_name"].sum() 
            if user is asking for individual or seperate result then calculate seperately 
            eg:rtb_count = (df["requested_by"] == "RTB").sum()
               tb_count = (df["requested_by"] == "CTB").sum()
            eg code ...
            #code start
            import pandas as pd
            df = pd.read_csv("generated_files/current.csv")

            // your pandas generated code 
            // code for saving it into outputs/output.txt with User Query {df_structure_main} Followed by the output
            #code end 
            """
    crew = Crew(agents=[pandas_agent], tasks=[query_task],inputs={"prompt2": prompt2})
    result = crew.kickoff()
    with open("outputs/output.py", "w") as f:
        f.write(str(result))


pandas_query_crew("FTE/FTC story point ratio")