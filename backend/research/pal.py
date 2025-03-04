import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluator.base_evaluator import BaseEvaluator, main
from model.gemini import init_gemini_model
import contextlib
import io

class PalReasoningService:
    def __init__(self):
        # Configure the Gemini API
        self.model = init_gemini_model()
    
    def evaluate_with_program_aided(self, statement, ground_answer):
        """
        Generate code to solve the problem and execute it.
        """
        try:
            # Ask the model to generate Python code to solve the problem
            code_prompt = (
                f"Problem: {statement}\n\n"
                "Write a Python function that solves this problem. The function should:\n"
                "1. Take any necessary inputs\n"
                "2. Implement a solution to the problem\n"
                "3. Return the answer as the final output\n"
                "4. Include comments explaining your approach\n\n"
                "Name your function 'solve_problem' and make sure it can be executed without additional input.\n"
                "Ensure the output of your function is the direct answer to the question (e.g., a number or a string).\n\n"
                "After writing the code, add a line at the end to execute the function and print the result:\n"
                "print(solve_problem())"
            )
            
            code_response = self.model.generate_content(code_prompt)
            code = code_response.text.strip()
            
            # Clean up the code (remove markdown if present)
            if "```python" in code and "```" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                parts = code.split("```")
                if len(parts) >= 3:  # Proper markdown with opening and closing ticks
                    code = parts[1].strip()
                else:
                    # Try to find any code block
                    for part in parts:
                        if "def solve_problem" in part:
                            code = part.strip()
                            break
            
            # Add defensive programming to catch potential issues
            code_with_explanation = (
                f"# Original problem: {statement}\n\n"
                f"{code}"
            )
            
            # Execute the code in a safe environment with all builtins
            restricted_globals = {"__builtins__": __builtins__}
            local_vars = {}
            output = io.StringIO()
            error_output = io.StringIO()
            result = None
            
            # Execute with captured output
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error_output):
                try:
                    exec(code, restricted_globals, local_vars)
                    execution_output = output.getvalue().strip()
                    error_messages = error_output.getvalue().strip()
                    
                    # Try to extract the result (last line of output)
                    if execution_output:
                        result_lines = execution_output.splitlines()
                        result = result_lines[-1].strip() if result_lines else None
                    
                    # If no result from stdout, try calling the function directly
                    if not result and 'solve_problem' in local_vars:
                        try:
                            result = str(local_vars['solve_problem']())
                        except Exception as func_e:
                            error_messages += f"\nError calling solve_problem(): {str(func_e)}"
                except Exception as e:
                    error_messages = f"{error_output.getvalue().strip()}\nExecution error: {str(e)}"
            
            # If no result found and errors exist, attempt to fix the code
            if (not result or result == "None") and (error_messages or not execution_output):
                fix_prompt = (
                    f"The Python code you generated for this problem had errors:\n\n"
                    f"Problem: {statement}\n\n"
                    f"Original code:\n```python\n{code}\n```\n\n"
                    f"Errors or issues:\n{error_messages if error_messages else 'The code ran but did not produce any output.'}\n\n"
                    "Please fix the code. Make sure it:\n"
                    "1. Correctly solves the problem\n"
                    "2. Prints the final answer explicitly\n"
                    "3. Handles any edge cases\n\n"
                    "Provide the complete corrected code."
                )
                
                fix_response = self.model.generate_content(fix_prompt)
                fixed_code = fix_response.text.strip()
                
                # Clean up the fixed code
                if "```python" in fixed_code and "```" in fixed_code:
                    fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
                elif "```" in fixed_code:
                    fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
                
                # Try executing the fixed code
                output = io.StringIO()
                error_output = io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error_output):
                    try:
                        local_vars = {}
                        exec(fixed_code, restricted_globals, local_vars)
                        execution_output = output.getvalue().strip()
                        result_lines = execution_output.splitlines()
                        result = result_lines[-1].strip() if result_lines else None
                        
                        if not result and 'solve_problem' in local_vars:
                            result = str(local_vars['solve_problem']())
                        
                        # Update code to the fixed version
                        code = fixed_code
                        code_with_explanation += f"\n\n# Fixed code after error:\n{fixed_code}"
                    except Exception as e:
                        error_messages += f"\n\nFixed code also had errors: {str(e)}"
            
            # Prepare explanation including the code and its execution details
            explanation = (
                f"PROGRAM-AIDED REASONING:\n\n"
                f"I approached this problem by writing Python code to solve it systematically:\n\n"
                f"```python\n{code}\n```\n\n"
            )
            if error_messages:
                explanation += f"EXECUTION ERRORS:\n{error_messages}\n\n"
            if execution_output:
                explanation += f"EXECUTION OUTPUT:\n{execution_output}\n\n"
            explanation += f"FINAL ANSWER: {result}"
            
            # Check if the answer matches ground truth
            is_correct = self._check_equivalence(result, ground_answer)
            
            return result, explanation, is_correct
        
        except Exception as e:
            return f"Error: {str(e)}", f"Error generating or executing code: {str(e)}", False
    
    def _check_equivalence(self, model_answer, ground_answer):
        """Helper method to check if the model's answer is equivalent to the ground truth."""
        try:
            if model_answer is None:
                return False
            model_answer_str = str(model_answer).lower().strip()
            ground_answer_str = str(ground_answer).lower().strip()
            if model_answer_str == ground_answer_str:
                return True
            try:
                if float(model_answer_str) == float(ground_answer_str):
                    return True
            except (ValueError, TypeError):
                pass
            if ground_answer_str in model_answer_str:
                return True
            return False
        except Exception as e:
            print(f"Error in equivalence check: {e}")
            return False

if __name__ == "__main__":
    reasoning_service = PalReasoningService()
    evaluator = BaseEvaluator(reasoning_service, eval_method="evaluate_with_program_aided")
    main(evaluator, dataset_file="reasoning_problems.csv", results_file="program_aided_results.csv")