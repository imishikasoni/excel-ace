# interview_simulation.py
import os
import json
from typing import List, Dict, Any
from datetime import datetime
from crewai import Crew, Process

from src_crewai.agents import create_interviewer
from src_crewai.tasks import create_question_task, create_evaluation_task

class InterviewSimulation:
    def __init__(self, job_title: str, llm_agent=None):
        """
        InterviewSimulation drives a manual (user-input) interview flow.
        It supports:
         - Console-driven interviews via conduct_single_interview()
         - Programmatic question generation via get_question()
         - Programmatic evaluation via evaluate()
         - Saving results to a timestamped JSON file via save_results()
        """
        self.job_title = job_title
        # Use provided agent or create a new interviewer agent
        self.interviewer = llm_agent or create_interviewer(job_title)
        self.interview_results: Dict[str, Any] = {}

    # -------------------------
    # Console / manual flow
    # -------------------------
    def conduct_single_interview(self, num_questions: int = 5) -> dict:
        """
        Conduct an interview in the console where the user types answers manually.
        Returns a dict containing interview_history and evaluation string.
        """
        print(f"\n=== Starting {self.job_title} Interview ===\n")

        interview_history: List[Dict[str, str]] = []

        for i in range(num_questions):
            # Generate question from LLM interviewer
            question_crew = Crew(
                agents=[self.interviewer],
                tasks=[create_question_task(self.job_title, self.interviewer, i + 1, interview_history)],
                process=Process.sequential
            )
            question = str(question_crew.kickoff()).strip()
            print(f"\nInterviewer: {question}")

            # Manual user input
            answer = input("Your Answer: ").strip()
            print(f"Candidate: {answer}\n")

            interview_history.append({
                "question": question,
                "answer": answer
            })

        # Generate evaluation from LLM interviewer
        print("\n=== Interview Evaluation ===\n")
        evaluation_crew = Crew(
            agents=[self.interviewer],
            tasks=[create_evaluation_task(self.job_title, self.interviewer, interview_history)],
            process=Process.sequential
        )
        evaluation = str(evaluation_crew.kickoff()).strip()
        print(evaluation)

        # Store results and save
        self.interview_results = {
            "interview_history": interview_history,
            "evaluation": evaluation
        }
        # filename = self.save_results()
        # print(f"\nResults saved to: {filename}")

        return self.interview_results

    # -------------------------
    # Programmatic helpers (for Streamlit / UI)
    # -------------------------
    def get_question(self, question_number: int, interview_history: List[Dict[str, str]]) -> str:
        """
        Generate a single Excel-focused question for `question_number` given prior history.
        Suitable for use in Streamlit per-question flow.
        """
        question_crew = Crew(
            agents=[self.interviewer],
            tasks=[create_question_task(self.job_title, self.interviewer, question_number, interview_history)],
            process=Process.sequential
        )
        return str(question_crew.kickoff()).strip()

    def evaluate(self, interview_history: List[Dict[str, str]]) -> str:
        """
        Produce a structured evaluation report (PASS/FAIL, score, strengths, improvements).
        Suitable for displaying in Streamlit or saving after the interview completes.
        """
        evaluation_crew = Crew(
            agents=[self.interviewer],
            tasks=[create_evaluation_task(self.job_title, self.interviewer, interview_history)],
            process=Process.sequential
        )
        evaluation = str(evaluation_crew.kickoff()).strip()

        # Save to internal state for convenience
        self.interview_results = {
            "interview_history": interview_history,
            "evaluation": evaluation
        }
        return evaluation

    # -------------------------
    # Runner wrapper used by non-UI scripts
    # -------------------------
    def run(self, num_questions: int = 5) -> dict:
        """
        Convenience wrapper for console-based run (keeps backward compatibility).
        """
        return self.conduct_single_interview(num_questions=num_questions)

    # -------------------------
    # Persistence
    # -------------------------
    # def save_results(self, path: str = ".", prefix: str = "interview_results") -> str:
    #     """
    #     Save the current interview_results (must be populated via run() or evaluate())
    #     to a JSON file. Returns the filename.
    #     """
    #     if not self.interview_results:
    #         raise ValueError("No interview results to save. Run an interview or call evaluate() first.")

    #     os.makedirs(path, exist_ok=True)
    #     ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     filename = f"interview_results/{prefix}_{self.job_title.replace(' ', '_')}_{ts}.json"
    #     filepath = os.path.join(path, filename)

    #     payload = {
    #         "job_title": self.job_title,
    #         "interview_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #         "results": self.interview_results
    #     }

    #     with open(filepath, "w", encoding="utf-8") as f:
    #         json.dump(payload, f, indent=2, ensure_ascii=False)

    #     return filepath
