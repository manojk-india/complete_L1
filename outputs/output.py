import pandas as pd

# Load data
df = pd.read_csv("generated_files/current.csv")         # current sprint data

# Compute total story points for in df dataframe
current_points = df['story_points'].fillna(0).sum()

# Output
with open("outputs/output.txt", "w") as f:
    f.write("Query: Story points assigned to Hari in L1Board1 in sprint 9 is " + str(current_points))
    f.write("\n")
