```python
#code start
import pandas as pd

# Load data
df = pd.read_csv("generated_files/current.csv")        # current sprint data
df_history = pd.read_csv("generated_files/history.csv") # previous sprints data

# Calculate total story points for current sprint
current_points = df['story_points'].fillna(0).sum()

# Calculate average story points from previous sprints
if len(df_history) > 0:
    avg_points = df_history['story_points'].fillna(0).groupby(df_history['sprint']).sum().mean()
else:
    avg_points = 0

# Determine capacity utilization status
if avg_points == 0:
    utilization_status = "No historical data available for comparison."
elif current_points > avg_points:
    utilization_status = "Overutilized"
elif current_points < avg_points:
    utilization_status = "Underutilized"
else:
    utilization_status = "Utilization is on par with historical average"

# Save results to output file
with open("outputs/output.txt", "w") as f:
    f.write("Query: Capacity of Hari in L1Board1 in sprint 10\n")
    f.write(f"Current sprint story points: {current_points}\n")
    f.write(f"Average of previous sprints: {avg_points:.2f}\n")
    f.write(f"Capacity utilization status: {utilization_status}\n")
#code end
```