```python
#code start
import pandas as pd

# Load data
df = pd.read_csv("generated_files/current.csv")

# Compute total story points for Hari in ABC 1 board
story_points = df['story_points'].fillna(0).sum()

# Output the result
with open("outputs/output.txt", "w") as f:
    f.write("Query: story points assigned to Hari in ABC 1 board\n")
    f.write(f"Total story points: {story_points}\n")
#code end
```