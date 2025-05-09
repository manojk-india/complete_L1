```python
#code start
import pandas as pd

# Load data
df = pd.read_csv("generated_files/current.csv")

# Compute total story points for Hari in abc1 project
story_points = df['story_points'].fillna(0).sum()

# Output the result
with open("outputs/output.txt", "w") as f:
    f.write("Query: No of story points assigned to Hari in abc1 is " + str(story_points))
    f.write("\n")
#code end
```