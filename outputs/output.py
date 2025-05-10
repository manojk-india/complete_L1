import pandas as pd

# Load current sprint data
df = pd.read_csv("generated_files/current.csv")

# Calculate RTB and CTB story points
rtb_points = df[df['requested_by'] == 'RTB']['story_points'].fillna(0).sum()
ctb_points = df[df['requested_by'] == 'CTB']['story_points'].fillna(0).sum()

# Output
with open("outputs/output.txt", "w") as f:
    f.write("Query: RTB/CTB utilization of abc1 board in sprint 9\n")
    f.write(f"RTB story points: {rtb_points}\n")
    f.write(f"CTB story points: {ctb_points}\n")
