import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.gemini import init_gemini_model
from evaluator.base_evaluator import BaseEvaluator, main

class CotAndVerificationReasoningService:
    def __init__(self):
        # Configure the Gemini API
        self.model = init_gemini_model()
    
    def evaluate_with_cot_and_verification(self, statement, ground_answer):
        try:
            cot_prompt = (
                f"Problem: {statement}\n\n"
                "Let's think about this step by step:\n"
                "1. First, understand what the problem is asking\n"
                "2. Break down the information given\n"
                "3. Apply logical reasoning to each component\n"
                "4. Combine insights to determine the answer\n\n"
                "Work through each step carefully before giving your answer."
            )
            cot_response = self.model.generate_content(cot_prompt)
            cot_result = cot_response.text.strip()
            
            verification_prompt = (
                f"You solved this problem:\n'{statement}'\n\n"
                f"Your solution was:\n{cot_result}\n\n"
                "Now, carefully verify your solution:\n"
                "After verification, provide your final answer with confidence:\n"
                "FINAL VERIFIED ANSWER: [your answer]"
            )
            
            verification_response = self.model.generate_content(verification_prompt)
            verification_text = verification_response.text.strip()
            
            if "FINAL VERIFIED ANSWER:" in verification_text:
                parts = verification_text.split("FINAL VERIFIED ANSWER:")
                answer = parts[1].strip()
                explanation = cot_result + "\n\nVERIFICATION:\n" + parts[0].strip()
            else:
                answer = verification_text.split('\n')[-1].strip()
                explanation = cot_result + "\n\nVERIFICATION:\n" + verification_text
                
            is_correct = (str(answer).strip().lower() == str(ground_answer).strip().lower())
            
            return answer, explanation, is_correct
        
        except Exception as e:
            return f"Error: {str(e)}", "Error: Failed to get response from AI model", False

if __name__ == "__main__":
    reasoning_service = CotAndVerificationReasoningService()
    evaluator = BaseEvaluator(reasoning_service, eval_method="evaluate_with_cot_and_verification")
    main(evaluator, dataset_file="reasoning_problems.csv", results_file="cot_verification_results.csv")
