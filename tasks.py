from crewai import Task
from typing import List

def create_question_task(job_title: str, interviewer, question_number: int, interview_history: List) -> Task:
    """Creates a task for generating Excel-focused interview questions"""
    context = "\n".join([
        f"Q{i+1}: {interaction['question']}\nA{i+1}: {interaction['answer']}"
        for i, interaction in enumerate(interview_history)
    ]) if interview_history else "No previous responses"
    
    print(context)
    return Task(
        description=f"""You are conducting Excel interview question #{question_number} 
        for the {job_title} position.

        Previous conversation context:
        {context}

        Rules for asking questions:
        1. For the first question only (Q1), check if the candidate is willing to start.
        - If the candidate is unwilling to start (explicitly says they do not want to continue), exit gracefully.
        - If the candidate is willing, proceed.
        2. From Q2 onward, always generate the next Excel question regardless of the candidate's short/negative answers.
        - Do NOT interpret “no” or “I don’t know” as refusal to continue.
        - Q1: Start with an introductory question about their background and Excel usage experience.
        - From Q2 onward: Ask **practical Excel questions** relevant to {job_title}.
            Examples:
            - Data Analyst → PivotTables, data cleaning, dashboards, formulas.
            - Financial Analyst → financial modeling, forecasting, sensitivity analysis.
            - Operations Analyst → supply chain data, scenario analysis, scheduling in Excel.
        - Always test *real-world Excel ability*, not just theory.
        - Adapt follow-up questions based on the candidate’s last response.
        - Only generate ONE clear, Excel-focused question at a time.

        Return ONLY the question text, nothing else.""",
        expected_output="A single Excel-focused interview question that is clear, relevant, and practical.",
        agent=interviewer
    )

def create_evaluation_task(job_title: str, interviewer, interview_history: List) -> Task:
    """Creates a task for evaluating the candidate's Excel performance"""
    context = "\n".join([
        f"Q{i+1}: {interaction['question']}\nA{i+1}: {interaction['answer']}"
        for i, interaction in enumerate(interview_history)
    ])
    
    return Task(
        description=f"""Based on the full Excel interview conversation for the {job_title} role:

        {context}

        Provide a structured evaluation including:
        1. Overall Decision (PASS/FAIL)
        2. Score (0-100) → based on correctness, clarity, efficiency, and practicality of answers
        3. Key Strengths in Excel skills (formulas, PivotTables, data handling, analysis)
        4. Areas for Improvement (specific Excel functions or concepts they struggled with)
        5. Specific Tips for improving Excel proficiency for {job_title}
        6. Final Recommendation on hiring suitability

        Format the response clearly with headers and bullet points.""",
        expected_output="A structured evaluation report of the candidate’s Excel skills.",
        agent=interviewer
    )

def create_comparative_analysis_task(job_title: str, interviewer, interview_results: str) -> Task:
    """Creates a task for comparative analysis of all candidates"""
    return Task(
        description=f"""Based on the mock Excel interviews of candidates for the {job_title} position, 
        analyze and compare performance:

        {interview_results}

        Provide:
        1. Comparative scoring and ranking of candidates
        2. Notable differences in Excel problem-solving approaches
        3. Strengths and weaknesses of each candidate
        4. Recommendation of the best-fit candidate for the {job_title} role

        Format the response clearly with headers and bullet points.""",
        expected_output="A detailed comparative analysis of candidates’ Excel interview performance.",
        agent=interviewer
    )
