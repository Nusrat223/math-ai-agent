import re
import streamlit as st

def is_math_related(text):
    """
    Check if the input text is related to mathematics.
    
    Args:
        text (str): Input text to validate
        
    Returns:
        bool: True if the text appears to be math-related, False otherwise
    """
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Math-related keywords and patterns
    math_keywords = [
        # General math terms
        'solve', 'calculate', 'find', 'compute', 'evaluate', 'simplify',
        'derive', 'integrate', 'differentiate', 'factor', 'expand',
        
        # Math topics
        'algebra', 'geometry', 'trigonometry', 'calculus', 'arithmetic',
        'equation', 'function', 'formula', 'expression', 'polynomial',
        
        # Operations
        'add', 'subtract', 'multiply', 'divide', 'square', 'cube', 'power',
        'root', 'logarithm', 'exponential', 'factorial',
        
        # Geometry terms
        'area', 'perimeter', 'volume', 'circle', 'triangle', 'rectangle',
        'sphere', 'cylinder', 'angle', 'radius', 'diameter', 'circumference',
        
        # Trigonometry
        'sin', 'cos', 'tan', 'sine', 'cosine', 'tangent', 'degrees', 'radians',
        
        # Calculus
        'derivative', 'integral', 'limit', 'convergence', 'series',
        
        # Units and measurements
        'meters', 'feet', 'inches', 'centimeters', 'degrees', 'percent'
    ]
    
    # Mathematical symbols and patterns
    math_patterns = [
        r'\d+[\+\-\*/\^]\d+',  # Basic arithmetic operations
        r'[xyz]\s*[\+\-\*/\^=]',  # Variables with operations
        r'\b\d+x\b',  # Terms like 2x, 3x
        r'=\s*\d+',  # Equals something
        r'[fgh]\([xyz]\)',  # Function notation
        r'\b\d+\s*[°%]\b',  # Degrees or percentages
        r'\b[a-z]\s*=\s*\d+',  # Variable assignments
        r'\([^\)]*[\+\-\*/]\)',  # Expressions in parentheses
    ]
    
    # Check for math keywords
    keyword_found = any(keyword in text_lower for keyword in math_keywords)
    
    # Check for mathematical patterns
    pattern_found = any(re.search(pattern, text_lower) for pattern in math_patterns)
    
    # Additional check for common math question patterns
    question_patterns = [
        r'what is.*[\+\-\*/]',
        r'solve.*for.*[xyz]',
        r'find.*[xyz]',
        r'calculate.*',
        r'how.*many.*',
        r'what.*area.*',
        r'what.*volume.*',
        r'derivative.*of',
        r'integral.*of'
    ]
    
    question_pattern_found = any(re.search(pattern, text_lower) for pattern in question_patterns)
    
    return keyword_found or pattern_found or question_pattern_found

def format_latex(text):
    """
    Format text to properly display LaTeX expressions in Streamlit.
    
    Args:
        text (str): Text containing LaTeX expressions
        
    Returns:
        str: Formatted text with proper LaTeX rendering
    """
    # Replace double dollar signs with Streamlit's LaTeX format
    text = re.sub(r'\$\$(.*?)\$\$', r'$$\1$$', text, flags=re.DOTALL)
    
    # Replace single dollar signs with Streamlit's inline LaTeX format
    text = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'$\1$', text)
    
    return text

def extract_math_expressions(text):
    """
    Extract mathematical expressions from text for validation.
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of mathematical expressions found
    """
    # Patterns for mathematical expressions
    patterns = [
        r'\$\$(.*?)\$\$',  # Display math
        r'\$(.*?)\$',      # Inline math
        r'\b\d+[xyz]\b',   # Terms like 2x
        r'[xyz]\s*[\+\-\*/\^=]\s*\d+',  # Variable operations
        r'\b[fgh]\([xyz]\)',  # Function notation
    ]
    
    expressions = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        expressions.extend(matches)
    
    return expressions

def clean_math_input(text):
    """
    Clean and prepare mathematical input for processing.
    
    Args:
        text (str): Raw input text
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Ensure proper spacing around operators
    text = re.sub(r'([+\-*/=])', r' \1 ', text)
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    
    return text.strip()
