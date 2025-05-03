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
    temperature=0.2,
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
        backstory="You are a data expert specializing in analyzing and extracting information through Pandas DataFrames.",
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
        You are a Pandas code generation expert. Use this CSV structure:
        {df_structure_main}

        **Rules:**
        1. Always start with `df = pd.read_csv("generated_files/current.csv")`
        2. Never create new DataFrames - only use `df`
        3. For counts: Use vectorized operations like `.sum()` or `len(df)`
        4. For separate results (e.g., RTB/CTB), calculate in one code block
        5. Save results to `output.txt` with this format:
        - First line: "Query: [user's exact query]"
        - Subsequent lines: Results
        6. Handle nulls appropriately (e.g., `.fillna(0)` for numeric columns)
        7. For date columns: Assume MM-DD-YYYY format unless specified

        **Example Query:** "Count stories assigned to Hari"
        **Correct Code:**
        #code start
        import pandas as pd
        df = pd.read_csv("generated_files/current.csv")

        story_count = len(df[(df['issue_type'] == 'Story') & (df['assignee'] == 'Hari')])

        with open("output.txt", "w") as f:
            f.write(f"Query: Count stories assigned to Hari\\n")
            f.write(f"Number of stories assigned to Hari:"+str(story_count))
        #code end

        **Current Query:** "{query}"
            """
    crew = Crew(agents=[pandas_agent], tasks=[query_task],inputs={"prompt2": prompt2})
    result = crew.kickoff()
    with open("outputs/output.py", "w") as f:
        f.write(str(result))


pandas_query_crew("RTB/CTB ratio")