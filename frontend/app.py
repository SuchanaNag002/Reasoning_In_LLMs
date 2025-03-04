import streamlit as st
import requests
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Reasoning Methods Evaluator")
st.markdown("Test different reasoning approaches on logical reasoning problems")

# Add a method selector in the sidebar
st.sidebar.header("Reasoning Method")
method = st.sidebar.radio(
    "Select a reasoning method:",
    ["simple", "cot-verification", "program-aided"]
)

# Display description based on selection
if method == "simple":
    st.sidebar.info("Basic prompting that directly asks for an answer and explanation.")
elif method == "cot-verification":
    st.sidebar.info("Chain-of-Thought with Verification: Step-by-step reasoning followed by self-verification to catch errors.")
elif method == "program-aided":
    st.sidebar.info("Program-Aided: Uses code generation and execution to solve the problem programmatically.")

# Example problems in session state for persistence
if 'problem' not in st.session_state:
    st.session_state.problem = ""

# Sidebar example buttons update the session state
st.sidebar.header("Sample Problems")
example_problems = {
    "CRANBERRY Example": "Count the number of occurrences of the letter 'R' in the word CRANBERRY",
    "Horse Racing Problem": "You have six horses and want to race them to see which is fastest. What is the best way to do this?",
    "Cats Puzzle": "If all cats are mammals and some mammals are black, are all cats black?",
    "Vegetables Count": "I have a chair, two potatoes, a cauliflower, a lettuce head, two tables, a cabbage, two onions, and three fridges. How many vegetables do I have?"
}

st.sidebar.markdown("Click to load an example:")
for name, prob in example_problems.items():
    if st.sidebar.button(name):
        st.session_state.problem = prob

# Input field for the reasoning problem uses the session state
problem = st.text_area(
    "Enter a reasoning problem:",
    height=150,
    value=st.session_state.problem
)

# Update session state if user modifies the text area
if problem != st.session_state.problem:
    st.session_state.problem = problem

# Hidden field for ground truth, populated automatically by examples
ground_truth = ""

if st.button("Solve Problem"):
    if problem:
        try:
            with st.spinner("Thinking..."):
                # Create the API URL with the encoded problem
                encoded_problem = urllib.parse.quote(problem)
                
                # Set ground truth based on the problem if it's one of our examples
                if "CRANBERRY" in problem:
                    ground_truth = "3"
                elif "six horses" in problem:
                    ground_truth = "Race them on a single race track with at least six lanes"
                elif "cats are mammals" in problem:
                    ground_truth = "No"
                elif "potatoes" in problem and "cauliflower" in problem and "vegetables" in problem:
                    ground_truth = "7"
                
                # Try the GET endpoint first (as per original code)
                if ground_truth:
                    url = f"{API_URL}/reasoning/{method}/{encoded_problem}?ground_truth={urllib.parse.quote(ground_truth)}"
                else:
                    url = f"{API_URL}/reasoning/{method}/{encoded_problem}"
                
                try:
                    # Try GET request
                    response = requests.get(url)
                    
                    # If GET fails, fall back to POST
                    if response.status_code >= 400:
                        # Prepare POST data
                        post_url = f"{API_URL}/reasoning/{method}"
                        post_data = {
                            "statement": problem,
                            "ground_truth": ground_truth if ground_truth else None
                        }
                        
                        # Make POST request
                        response = requests.post(post_url, json=post_data)
                except Exception as e:
                    st.error(f"GET request failed: {str(e)}, trying POST...")
                    
                    # Prepare POST data
                    post_url = f"{API_URL}/reasoning/{method}"
                    post_data = {
                        "statement": problem,
                        "ground_truth": ground_truth if ground_truth else None
                    }
                    
                    # Make POST request
                    response = requests.post(post_url, json=post_data)
                
                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display results
                    st.success("Problem solved!")
                    
                    # Problem and answer
                    st.markdown("### Problem")
                    st.write(result['problem'])
                    
                    st.markdown("### AI's Answer")
                    st.write(result['answer'])
                    
                    # Only show ground truth comparison if we have one
                    if ground_truth:
                        st.markdown("### Ground Truth")
                        st.write(ground_truth)
                        
                        if result.get('correct') is not None:
                            if result['correct']:
                                st.success("✓ AI's answer matches ground truth")
                            else:
                                st.error("✗ AI's answer does not match ground truth")
                    
                    # Show the explanation
                    st.markdown("### Explanation")
                    # Use a container with scrolling for long explanations
                    with st.container():
                        st.markdown(f"<div style='height: 300px; overflow-y: scroll;'>{result['explanation']}</div>", unsafe_allow_html=True)
                else:
                    error_msg = response.json().get("detail") if response.headers.get("content-type") == "application/json" else response.text
                    st.error(f"Error {response.status_code}: {error_msg}")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a reasoning problem!")

# Method descriptions
st.sidebar.markdown("---")
st.sidebar.markdown("### Method Descriptions")
st.sidebar.markdown("""
**Simple Reasoning**: Basic prompting that directly asks for an answer and explanation.

**CoT Verification**: Step-by-step reasoning followed by self-verification to catch errors.

**Program-Aided**: Uses code generation and execution to solve the problem programmatically.
""")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Compare how different reasoning methods perform on the same problem.")