import pandas as pd

# Load current sprint data (multiple sprints in current.csv)
df = pd.read_csv("generated_files/current.csv")

# Load historical data for previous sprints
df_history = pd.read_csv("generated_files/history.csv")

# Calculate average velocity from previous sprints (average of total story points completed per sprint)
if len(df_history) > 0:
    avg_velocity = df_history['story_points'].fillna(0).groupby(df_history['sprint']).sum().mean()
else:
    avg_velocity = 0

# Identify the unique sprint names in the current sprint data
unique_sprints = df['sprint'].unique()

# Define thresholds for overutilization and underutilization (e.g., 20 percent difference from average)
threshold_percentage = 0.2
overutilized_threshold = avg_velocity * (1 + threshold_percentage)
underutilized_threshold = avg_velocity * (1 - threshold_percentage)

# Function to check the utilization status
def check_utilization(sprint_points, avg_velocity, overutilized_threshold, underutilized_threshold):
    if sprint_points >= overutilized_threshold:
        return "Overutilized"
    elif sprint_points <= underutilized_threshold:
        return "Underutilized"
    else:
        return "Healthy"

# Calculate story points for each sprint and determine utilization
utilization_results = {}
for sprint in unique_sprints:
    sprint_points = df[df['sprint'] == sprint]['story_points'].fillna(0).sum()
    utilization_results[sprint] = check_utilization(sprint_points, avg_velocity, overutilized_threshold, underutilized_threshold)

# Output results
with open("outputs/output.txt", "w") as f:
    f.write(f"Query: Backlog health of ABC1 board\n")
    f.write(f"Average velocity from previous sprints: {avg_velocity:.2f}\n")
    
    for sprint, utilization in utilization_results.items():
        sprint_points = df[df['sprint'] == sprint]['story_points'].fillna(0).sum()
        sprint_name = sprint.split(" ", 1)[1]
        f.write(f"Sprint: {sprint_name} - Story points: {sprint_points}\n")
        f.write(f"Backlog status: {utilization}\n")
        f.write("Below you can find low quality acceptance criteria report\n\n")
