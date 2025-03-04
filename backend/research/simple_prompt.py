import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.gemini import init_gemini_model
from evaluator.base_evaluator import BaseEvaluator, main

class SimplePromptReasoningService:
    def __init__(self):
        # Configure the Gemini API
        self.model = init_gemini_model()
        
    def evaluate_reasoning_with_explanation(self, statement, ground_answer=None):
        try:
            prompt = (
                f"For the reasoning problem '{statement}', provide:\n"
                "1. The answer (just the final answer without explanation, e.g., 'Yes', 'No', or a number)\n"
                "2. A detailed step-by-step explanation of how to arrive at this answer\n"
                f"3. Check if your answer '{ground_answer}' is numerically or semantically equivalent to the ground truth answer. Only respond with 'Yes' if they are EXACTLY equivalent, otherwise respond with 'No'.\n\n"
                "Format your response exactly like this:\n"
                "ANSWER: [your answer here]\n"
                "EXPLANATION: [your detailed explanation here]\n"
                "EQUIVALENT: [Yes or No - is your answer equivalent to the provided ground truth?]"
            )
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse response.
            answer_part = response_text.split("ANSWER:", 1)
            if len(answer_part) < 2:
                return "Error: Invalid response format", "Error: Missing ANSWER section", False
            
            remaining = answer_part[1]
            explanation_part = remaining.split("EXPLANATION:", 1)
            if len(explanation_part) < 2:
                return explanation_part[0].strip(), "Error: Missing EXPLANATION section", False
            
            answer = explanation_part[0].strip()
            remaining = explanation_part[1]
            
            is_correct = False
            if ground_answer:
                equivalent_part = remaining.split("EQUIVALENT:", 1)
                if len(equivalent_part) < 2:
                    explanation = equivalent_part[0].strip()
                    is_correct = False
                else:
                    explanation = equivalent_part[0].strip()
                    equivalence_result = equivalent_part[1].strip().lower()
                    is_correct = equivalence_result == "yes"
            else:
                explanation = remaining.strip()
            
            return answer, explanation, is_correct
            
        except Exception as e:
            return f"Error: {str(e)}", "Error: Failed to get response from AI model", False

if __name__ == "__main__":
    reasoning_service = SimplePromptReasoningService()
    evaluator = BaseEvaluator(reasoning_service, eval_method="evaluate_reasoning_with_explanation")
    main(evaluator, dataset_file="reasoning_problems.csv", results_file="reasoning_results.csv")
