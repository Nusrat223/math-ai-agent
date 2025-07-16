import streamlit as st
import re
from math_solver import MathSolver
from utils import is_math_related, format_latex

# Initialize the math solver
if 'math_solver' not in st.session_state:
    st.session_state.math_solver = MathSolver()

st.set_page_config(
    page_title="Math AI Agent",
    page_icon="🧮",
    layout="wide"
)

st.title("🧮 Math AI Agent")
st.markdown("**Solve math problems with step-by-step explanations**")

# Sidebar with supported topics
with st.sidebar:
    st.header("📚 Supported Topics")
    topics = [
        "📐 Algebra",
        "📏 Geometry", 
        "📊 Trigonometry",
        "🔢 Calculus",
        "➕ Arithmetic",
        "📝 Word Problems"
    ]
    for topic in topics:
        st.write(topic)
    
    st.markdown("---")
    st.markdown("**Tips:**")
    st.markdown("- Be specific with your problem")
    st.markdown("- Include all given information")
    st.markdown("- Ask for help if stuck!")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Enter Your Math Problem")
    
    # Text input for the math problem
    problem = st.text_area(
        "Problem:",
        placeholder="Enter your math problem here...\n\nExamples:\n- Solve for x: 2x + 5 = 13\n- Find the area of a circle with radius 7\n- What is the derivative of x² + 3x?",
        height=150
    )
    
    # Solve button
    if st.button("🔍 Solve Problem", type="primary", use_container_width=True):
        if problem.strip():
            # Validate if the input is math-related
            if not is_math_related(problem):
                st.error("⚠️ Please enter a mathematics-related question. I can only help with math problems!")
            else:
                with st.spinner("🤔 Thinking through this problem..."):
                    try:
                        solution = st.session_state.math_solver.solve_problem(problem)
                        
                        if solution:
                            st.success("✅ Problem solved!")
                            
                            # Display the solution
                            st.header("📋 Step-by-Step Solution")
                            
                            # Show the original problem
                            st.subheader("Problem Statement")
                            st.write(problem)
                            
                            # Show the solution with LaTeX formatting
                            st.subheader("Solution")
                            formatted_solution = format_latex(solution)
                            st.markdown(formatted_solution, unsafe_allow_html=True)
                            
                        else:
                            st.error("❌ I couldn't solve this problem. Please check if the problem is complete and clearly stated.")
                            
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.info("💡 Try rephrasing your problem or check if all necessary information is provided.")
        else:
            st.warning("⚠️ Please enter a math problem to solve.")

with col2:
    st.header("💡 Example Problems")
    
    examples = [
        "Solve for x: 3x - 7 = 14",
        "Find the area of a triangle with base 8 and height 6",
        "What is sin(30°)?",
        "Find the derivative of f(x) = x³ + 2x²",
        "Simplify: (x² - 4)/(x - 2)",
        "A train travels 120 miles in 2 hours. What is its speed?"
    ]
    
    for i, example in enumerate(examples):
        if st.button(f"📝 {example}", key=f"example_{i}", use_container_width=True):
            st.session_state.example_problem = example
            st.rerun()

# Handle example problem selection
if 'example_problem' in st.session_state:
    problem = st.session_state.example_problem
    del st.session_state.example_problem
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "**Note:** This AI agent specializes in mathematics. "
    "For best results, provide complete problem statements with all necessary information."
)
