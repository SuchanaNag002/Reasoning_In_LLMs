import pandas as pd

class BaseEvaluator:
    def __init__(self, reasoning_service, eval_method):
        """
        :param reasoning_service: An instance of a reasoning service.
        :param eval_method: The name of the method to call on reasoning_service for evaluation.
                            This method should accept (statement, ground_answer) and return a tuple
                            (ai_answer, ai_explanation, is_correct).
        """
        self.reasoning_service = reasoning_service
        self.eval_method = eval_method

    def evaluate_dataset(self, dataset_file="reasoning_problems.csv"):
        """Evaluate the model's performance on a dataset of reasoning problems."""
        try:
            df = pd.read_csv(dataset_file, encoding="utf-8")
        except UnicodeDecodeError:
            print("Failed to decode file as UTF-8. Trying CP1252...")
            df = pd.read_csv(dataset_file, encoding="cp1252")
        
        results = []
        print("\nStarting evaluation...\n")
        
        for index, row in df.iterrows():
            print(f"Processing problem {index + 1}/{len(df)}")
            statement = row["statement"]
            ground_answer = row["answer"]
            ground_explanation = row.get("explanation", "No ground explanation provided")
            
            # Call the evaluation method on the reasoning service.
            eval_func = getattr(self.reasoning_service, self.eval_method)
            ai_answer, ai_explanation, is_correct = eval_func(statement, ground_answer)
            
            # Store results.
            results.append({
                "problem": statement,
                "ground_answer": ground_answer,
                "ai_answer": ai_answer,
                "ground_explanation": ground_explanation,
                "ai_explanation": ai_explanation,
                "correct": is_correct
            })
            
            # Display current problem details.
            print(f"\nProblem: {statement}")
            print(f"Ground Truth: {ground_answer}")
            print(f"AI Answer: {ai_answer}")
            print(f"Correct: {is_correct}")
            
            print("\n--- AI Explanation ---")
            if len(ai_explanation) > 500:
                print(ai_explanation[:500] + "... (truncated, full explanation in results file)")
            else:
                print(ai_explanation)
                
            print("\n--- Ground Truth Explanation ---")
            print(ground_explanation)
            print("-" * 80 + "\n")
        
        return pd.DataFrame(results)

    def save_results(self, results, output_file="results.csv"):
        """Save evaluation results to a CSV file and also to a readable text file."""
        results.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"\nResults saved to {output_file}")
        readable_output = output_file.replace(".csv", "_readable.txt")
        with open(readable_output, "w", encoding="utf-8") as f:
            for idx, row in results.iterrows():
                f.write(f"Problem {idx+1}: {row['problem']}\n")
                f.write(f"Ground Truth: {row['ground_answer']}\n")
                f.write(f"AI Answer: {row['ai_answer']}\n")
                f.write(f"Correct: {row['correct']}\n\n")
                f.write("--- AI Explanation ---\n")
                f.write(f"{row['ai_explanation']}\n\n")
                f.write("--- Ground Truth Explanation ---\n")
                f.write(f"{row['ground_explanation']}\n\n")
                f.write("=" * 80 + "\n\n")
        print(f"Readable results with full explanations saved to {readable_output}")

def main(evaluator, dataset_file, results_file):
    try:
        results = evaluator.evaluate_dataset(dataset_file)
        evaluator.save_results(results, results_file)
        
        # Print summary statistics.
        print("\nEvaluation Summary:")
        accuracy = results["correct"].mean()
        print(f"Accuracy: {accuracy:.2%}")
        
        print("\nCorrectly solved problems:")
        for idx, row in results[results["correct"]].iterrows():
            print(f"- {row['problem']}")
        
        print("\nIncorrectly solved problems:")
        for idx, row in results[~results["correct"]].iterrows():
            print(f"- {row['problem']}")
            print(f"  Ground truth: {row['ground_answer']}")
            print(f"  AI answer: {row['ai_answer']}\n")
    except KeyboardInterrupt:
        print("\nEvaluation interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nEvaluation complete")
