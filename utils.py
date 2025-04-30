# Here is where our helper function will be present of all kind ....

# ficning whoch L2 board is involved 
def find_present_words_case_insensitive(query):
    # Convert query to lower case for case-insensitive comparison
    query_lower = query.lower()

    word_list=["cdf","ebsnf","tes1","tes2","dis1","dis2"]
    # Collect words that are present in the query (case-insensitive)
    found = [word for word in word_list if word.lower() in query_lower]
    if found:
        return found
    else:
        return None
    
# writing it into checkpoint file for better debugging 
def write_to_checkpoint_file(data, file_path='checkpoint.txt'):
    with open(file_path, 'a') as file:
        file.write(data + '\n')

# function that returns the L1 board id for the given board name -- to be done 
def get_board_id(board_name):
    board_ids = {
        "cdf": 1,
        "ebsnf": 2,
        "tes1": 3,
        "tes2": 4,
        "dis1": 5,
        "dis2": 6
    }
    return board_ids.get(board_name.lower(), None)  # Return None if not found
