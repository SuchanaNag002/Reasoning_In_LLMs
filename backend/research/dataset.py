problems = [
    # Logic Puzzle Problems (20)
    # {"statement": "If all cats are mammals and some mammals are black, are all cats black?",
    #  "answer": "No",
    #  "explanation": "While all cats are indeed mammals, the statement only says some mammals are black, not all. Therefore, it's possible for some cats to be black, but not all cats must be black."},

    # Conditional Reasoning Problems (20)
    # {"statement": "If it rains, the ground gets wet. The ground is wet. Did it rain?",
    #  "answer": "Not necessarily",
    #  "explanation": "The statement establishes that rain causes the ground to be wet, but it doesn't mean rain is the only cause. Other factors, like a sprinkler, could also make the ground wet, so we can't conclude it definitely rained."},

    # Syllogism Problems (20)
    # {"statement": "All men are mortal. Socrates is a man. Is Socrates mortal?",
    #  "answer": "Yes",
    #  "explanation": "The first part states that all men are mortal, meaning mortality applies to every man. Since Socrates is identified as a man, he must also be mortal based on the given rule."},
    
    {"statement": "Count the number of occurrences of the letter 'L' in the word -LOLLAPALOOZA",
     "answer": "4",
     "explanation": "To count the 'L's, break down the word '-LOLLAPALOOZA' into individual characters: '-', 'L' (the 1st), 'O', 'L' (the 2nd), 'L' (the 3rd), 'A', 'P', 'A', 'L' (the 4th), 'O', 'O', 'Z', 'A'. Examining each character, the letter 'L' appears four times: once in position 2, twice in positions 4 and 5, and once in position 9. Thus, the total count is 4."},
    
    {"statement": "I have a chair, two potatoes, a cauliflower, a lettuce head, two tables, a cabbage, two onions, and three fridges. How many vegetables do I have?",
     "answer": "7",
     "explanation": "To count the vegetables, I need to identify each vegetable item: potatoes (2), cauliflower (1), lettuce head (1), cabbage (1), and onions (2). The chairs, tables, and fridges are furniture items, not vegetables. Adding up all the vegetables: 2 + 1 + 1 + 1 + 2 = 7 vegetables in total."}
    
    # {
    # "statement": "You have six horses and want to race them to see which is fastest. What is the best way to do this?",
    # "answer": "Race them on a single race track with at least six lanes, and the order in which they cross the finish line determines which is the fastest.",
    # "explanation": "To determine which horse is the fastest among six, the most straightforward and efficient method is to race all six horses at once on a track with at least six lanes, one for each horse. This ensures a fair comparison under identical conditions, such as weather and track surface. By observing the order in which they cross the finish line, you can directly identify the fastest horse as the one that finishes first. This approach avoids the need for multiple races or complex elimination rounds, making it the best way to achieve the goal in a single, conclusive event."},
]

def save_dataset(filename="reasoning_problems.csv"):
    import pandas as pd
    
    # Create DataFrame from problems list
    df = pd.DataFrame(problems)
    
    # Write to CSV file, overwriting any existing file
    df.to_csv(filename, index=False, encoding="utf-8-sig", mode='w')
    
    print(f"Dataset saved to {filename}, replacing any previous version.")

if __name__ == "__main__":
    save_dataset()