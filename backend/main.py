from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from urllib.parse import unquote
from research.simple_prompt import SimplePromptReasoningService
from research.cot_prompt_verification import CotAndVerificationReasoningService
from research.pal import PalReasoningService

app = FastAPI(
    title="Reasoning Methods API",
    description="API for solving reasoning problems using different methods",
    version="1.0.0"
)

# Initialize the reasoning services
simple_service = SimplePromptReasoningService()
cot_service = CotAndVerificationReasoningService()
pal_service = PalReasoningService()

class ReasoningRequest(BaseModel):
    statement: str
    ground_truth: Optional[str] = None

# Simple Reasoning endpoint
@app.post("/reasoning/simple")
async def simple_reasoning(request: ReasoningRequest):
    """
    Solve a reasoning problem using the simple approach with answer and explanation.
    
    Parameters:
    - statement: The reasoning problem statement
    - ground_truth: Optional ground truth answer for verification
    
    Returns:
    - JSON object containing the problem, answer, explanation, and correctness check
    """
    try:
        # Get answer and explanation - note the renaming of ground_truth to ground_answer
        answer, explanation, is_correct = simple_service.evaluate_reasoning_with_explanation(
            statement=request.statement, 
            ground_answer=request.ground_truth 
        )
        
        # Check for errors
        if answer and answer.startswith("Error:"):
            raise HTTPException(status_code=400, detail=answer)
        
        # Return the result
        return {
            "problem": request.statement,
            "answer": answer,
            "explanation": explanation,
            "correct": is_correct if request.ground_truth else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CoT+Verification endpoint
@app.post("/reasoning/cot-verification")
async def cot_verification(request: ReasoningRequest):
    """
    Solve a reasoning problem using Chain-of-Thought with Verification.
    
    Parameters:
    - statement: The reasoning problem statement
    - ground_truth: Optional ground truth answer for verification
    
    Returns:
    - JSON object containing the problem, answer, explanation, and correctness check
    """
    try:
        # Get answer and explanation with CoT+Verification
        answer, explanation, is_correct = cot_service.evaluate_with_cot_and_verification(
            request.statement,
            request.ground_truth
        )
        
        # Check for errors
        if answer and answer.startswith("Error:"):
            raise HTTPException(status_code=400, detail=answer)
        
        # Return the result
        return {
            "problem": request.statement,
            "answer": answer,
            "explanation": explanation,
            "correct": is_correct if request.ground_truth else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Program-Aided endpoint
@app.post("/reasoning/program-aided")
async def program_aided(request: ReasoningRequest):
    """
    Solve a reasoning problem using Program-Aided Language Model approach.
    
    Parameters:
    - statement: The reasoning problem statement
    - ground_truth: Optional ground truth answer for verification
    
    Returns:
    - JSON object containing the problem, answer, explanation, and correctness check
    """
    try:
        # Get answer and explanation with Program-Aided approach
        answer, explanation, is_correct = pal_service.evaluate_with_program_aided(
            request.statement,
            request.ground_truth
        )
        
        # Check for errors
        if answer and answer.startswith("Error:"):
            raise HTTPException(status_code=400, detail=answer)
        
        # Return the result
        return {
            "problem": request.statement,
            "answer": answer,
            "explanation": explanation,
            "correct": is_correct if request.ground_truth else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Generic endpoint that accepts the method as a parameter
@app.get("/reasoning/{method}/{statement}")
async def solve_reasoning_problem(method: str, statement: str, ground_truth: Optional[str] = None):
    """
    Solve a reasoning problem using the specified method.
    
    Parameters:
    - method: The reasoning method to use (simple, cot-verification, or program-aided)
    - statement: The reasoning problem statement (URL encoded)
    - ground_truth: Optional ground truth answer for verification
    
    Returns:
    - JSON object containing the problem, answer, explanation, and correctness check
    """
    try:
        # Decode the URL-encoded strings
        decoded_statement = unquote(statement)
        decoded_ground_truth = unquote(ground_truth) if ground_truth else None
        
        # Choose the appropriate method
        if method.lower() == "simple":
            # Use named parameter to match the method signature
            answer, explanation, is_correct = simple_service.evaluate_reasoning_with_explanation(
                decoded_statement,
                ground_answer=decoded_ground_truth 
            )
        elif method.lower() == "cot-verification":
            answer, explanation, is_correct = cot_service.evaluate_with_cot_and_verification(
                decoded_statement,
                decoded_ground_truth
            )
        elif method.lower() == "program-aided":
            answer, explanation, is_correct = pal_service.evaluate_with_program_aided(
                decoded_statement,
                decoded_ground_truth
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid method: {method}. Please use 'simple', 'cot-verification', or 'program-aided'."
            )
        
        # Check for errors
        if answer and answer.startswith("Error:"):
            raise HTTPException(status_code=400, detail=answer)
        
        # Return the result
        return {
            "problem": decoded_statement,
            "answer": answer,
            "explanation": explanation,
            "correct": is_correct if decoded_ground_truth else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)