
---

# Reasoning Methods Evaluator

This project demonstrates multiple methods for solving logical reasoning problems using an AI model. The project is divided into two main components: a **backend** API built with FastAPI and a **frontend** application built with Streamlit. Each component implements various reasoning strategies, including:

- **Simple Reasoning:** Directly prompts the model for an answer with an explanation.
- **Chain-of-Thought (CoT) with Verification:** Encourages step-by-step reasoning followed by a self-verification process.
- **Program-Aided Reasoning:** Generates Python code to solve the problem and executes the code to produce the final answer.

---

## Project Structure

- **backend/**
  - Contains the API logic and reasoning services.
  - **main.py**: Entry point for running the backend API.
  - **requirements.txt**: Lists all dependencies for the backend.
  
- **frontend/**
  - Contains the Streamlit app for interactive testing.
  - **app.py**: Main file for the frontend application.
  - **requirements.txt**: Lists all dependencies for the frontend.

---

## Setup and Running Instructions

### Backend Setup

1. **Change Directory to Backend:**

   ```bash
   cd backend
   ```

2. **Create a Virtual Environment:**

   Create a virtual environment named `venv_backend`:

   ```bash
   python -m venv venv_backend
   ```

3. **Activate the Virtual Environment:**

   - **Windows:**

     ```bash
     venv_backend\Scripts\activate
     ```

   - **Unix/MacOS:**

     ```bash
     source venv_backend/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Backend API:**

   ```bash
   python main.py
   ```

   The API will start running, typically accessible at [http://localhost:8000](http://localhost:8000).

---

### Frontend Setup

1. **Change Directory to Frontend:**

   Open a separate terminal and navigate to the frontend folder:

   ```bash
   cd frontend
   ```

2. **Create a Virtual Environment:**

   Create a virtual environment named `venv_frontend`:

   ```bash
   python -m venv venv_frontend
   ```

3. **Activate the Virtual Environment:**

   - **Windows:**

     ```bash
     venv_frontend\Scripts\activate
     ```

   - **Unix/MacOS:**

     ```bash
     source venv_frontend/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Streamlit App:**

   ```bash
   streamlit run app.py
   ```

   This will launch the Streamlit application in your web browser, where you can interact with the reasoning methods.

---

## How It Works

1. **Reasoning Services:**

   Each reasoning service generates a prompt for the AI model(gemini-1.5-pro) (via the Gemini API) to solve a given problem:
   
   - **Simple Reasoning:**  
     Provides an answer, detailed explanation, and checks equivalence against a ground truth if provided.
   
   - **CoT with Verification:**  
     Uses a step-by-step approach (chain-of-thought) to reason through the problem, then verifies the solution before finalizing the answer.
   
   - **Program-Aided Reasoning:**  
     Generates Python code that solves the problem, executes the code, and uses the output as the final answer. If the code fails or produces errors, it attempts to fix the code and re-run.

2. **API Endpoints:**

   The backend exposes several endpoints:
   
   - `/reasoning/simple`: For simple reasoning.
   - `/reasoning/cot-verification`: For chain-of-thought reasoning with verification.
   - `/reasoning/program-aided`: For program-aided reasoning.
   - `/health`: For a basic health check of the backend service.

3. **Frontend Interface:**

   The Streamlit frontend provides an interactive UI where users can:
   
   - Input custom reasoning problems.
   - Select a reasoning method from the sidebar.
   - View the AI-generated answer, explanation, and, when available, a correctness indicator compared to a provided ground truth.

---

## Conclusion

This project showcases different strategies to approach logical reasoning problems using AI. By running both the backend and frontend, users can experiment with each method and compare their effectiveness interactively. The modular design also allows for future extensions and improvements in reasoning strategies.

---