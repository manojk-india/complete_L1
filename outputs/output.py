Here's a complete pandas code that reads a CSV file, performs a query based on the user's request, and saves the output to a text file named `output.txt`:

```python
# Import pandas library
import pandas as pd

# Read the CSV file into a DataFrame
def query_csv_and_save_output(csv_file_path, query_params):
    try:
        # Load the data
        df = pd.read_csv(csv_file_path)
        
        # Example query: Filter rows where 'column_name' meets a condition
        # and save the result to output.txt
        filtered_df = df[df['column_name'] > query_params['threshold']]
        
        # Save the filtered results to output.txt
        filtered_df.to_csv('output.txt', index=False, mode='w')
        
        print("Query executed successfully. Results saved to output.txt")
        
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except KeyError:
        print(f"Error: The column {query_params['column']} does not exist in the DataFrame.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    csv_file_path = "your_data.csv"  # Replace with your CSV file path
    query_params = {
        'column': 'your_column_name',  # Replace with your column name
        'threshold': 100  # Replace with your threshold value
    }
    query_csv_and_save_output(csv_file_path, query_params)
```

This code:
1. Imports the pandas library
2. Defines a function `query_csv_and_save_output` that takes the CSV file path and query parameters
3. Reads the CSV file into a DataFrame
4. Performs a query (example: filtering rows based on a threshold)
5. Saves the results to `output.txt`
6. Includes error handling for common issues
7. Provides an example usage section that you can customize

Replace the placeholders (`your_data.csv`, `your_column_name`, and `100`) with your actual data and query parameters to match your specific needs.