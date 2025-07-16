import os
from google import genai
from google.genai import types
import re

class MathSolver:
    def __init__(self):
        """Initialize the Math Solver with Gemini client."""
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=api_key)
        
        # System prompt for the math AI agent
        self.system_prompt = """You are a helpful math AI agent designed to solve mathematical problems step-by-step. 

Your responsibilities:
1. Solve math problems across these topics: algebra, geometry, trigonometry, calculus, arithmetic, and word problems
2. Provide clear, step-by-step explanations in simple, student-friendly language
3. Format mathematical equations using LaTeX notation (wrap in $ for inline or $$ for display)
4. Show your work process clearly for educational value
5. Only solve mathematics-related questions
6. Ask for clarification if a problem is incomplete or unclear

Guidelines:
- Use simple language that students can understand
- Break down complex problems into smaller steps
- Explain the reasoning behind each step
- Use proper mathematical notation with LaTeX formatting
- If the problem is unclear or incomplete, ask specific questions to clarify
- If the question is not math-related, politely decline and ask for a math problem

Format your response with clear sections:
1. Understanding the Problem
2. Step-by-Step Solution
3. Final Answer

Always use LaTeX for mathematical expressions (e.g., $x^2 + 3x = 0$ or $$\\frac{a}{b} = \\frac{c}{d}$$)"""

    def solve_problem(self, problem):
        """
        Solve a mathematical problem using Google's Gemini model.
        
        Args:
            problem (str): The mathematical problem to solve
            
        Returns:
            str: Step-by-step solution with LaTeX formatting
        """
        try:
            # Use Gemini 2.5 Flash for mathematical problem solving
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=f"{self.system_prompt}\n\nPlease solve this math problem: {problem}")])
                ],
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Lower temperature for more consistent mathematical solutions
                    max_output_tokens=2000
                )
            )
            
            solution = response.text or "Unable to generate solution"
            return solution
            
        except Exception as e:
            raise Exception(f"Failed to solve problem: {str(e)}")
    
    def validate_problem_clarity(self, problem):
        """
        Check if a math problem is clear and complete.
        
        Args:
            problem (str): The mathematical problem to validate
            
        Returns:
            tuple: (is_clear, clarification_needed)
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=f"You are a math problem validator. Determine if a math problem is clear and complete enough to solve. If not, suggest what additional information is needed.\n\nIs this math problem clear and complete enough to solve? If not, what clarification is needed?\n\nProblem: {problem}")])
                ],
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=300
                )
            )
            
            validation = response.text or ""
            
            # Simple heuristic to determine if clarification is needed
            clarification_indicators = ["unclear", "incomplete", "need", "missing", "clarification", "specify"]
            needs_clarification = any(indicator in validation.lower() for indicator in clarification_indicators)
            
            return not needs_clarification, validation
            
        except Exception as e:
            # If validation fails, assume the problem is clear enough to attempt
            return True, ""
