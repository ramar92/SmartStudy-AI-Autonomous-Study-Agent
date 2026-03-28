"""
SmartStudy AI — Autonomous Study Agent using PhiData + Groq
"""

import os
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.calculator import Calculator
from phi.storage.agent.sqlite import SqlAgentStorage

# API Keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "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")
os.environ["PHI_API_KEY"] = os.getenv("PHIDATA_API_KEY", "phi-PUJOCOMOUtdDdsCGMoTr73s_HrlmfjHyeBf4pAsFbxg")


def create_study_agent() -> Agent:
    """Create the SmartStudy autonomous agent."""
    return Agent(
        name="StudyBot",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo(), Calculator()],
        storage=SqlAgentStorage(
            table_name="study_sessions",
            db_file="smartstudy.db"
        ),
        description=(
            "You are StudyBot, an expert AI tutor and academic coach. "
            "You help students learn faster through personalized explanations, "
            "flashcards, quizzes, study plans, essay feedback, and concept breakdowns."
        ),
        instructions=[
            "Explain concepts clearly using analogies, examples, and step-by-step breakdowns.",
            "Generate practice questions and quizzes tailored to the topic and difficulty level.",
            "Create flashcard sets in Q&A format when asked.",
            "Build personalized study schedules based on deadlines and available time.",
            "Provide detailed essay and writing feedback: structure, arguments, grammar, clarity.",
            "Summarize long texts, textbook chapters, or articles into concise notes.",
            "Use the calculator for math, statistics, and science problem-solving.",
            "Search the web for latest research, definitions, or updated information.",
            "Adapt explanation depth to the student's level: beginner, intermediate, advanced.",
            "Always be encouraging, patient, and motivating.",
            "Use markdown formatting: headers, bullet points, code blocks, tables.",
            "Ask clarifying questions to better tailor your help.",
        ],
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=True,
        num_history_responses=6,
        read_chat_history=True,
    )


def run_study_chat():
    """Run an interactive SmartStudy CLI session."""
    print("\n" + "="*62)
    print("  📚 StudyBot — Autonomous SmartStudy AI Agent")
    print("  Powered by PhiData + Groq (LLaMA 3.3 70B)")
    print("="*62)
    print("\nHello! I'm StudyBot, your personal AI tutor.")
    print("I can help you with:")
    print("  • Concept explanations (any subject)")
    print("  • Practice quizzes & flashcards")
    print("  • Study schedules & plans")
    print("  • Essay writing & feedback")
    print("  • Math & science problem solving")
    print("  • Summarizing notes & articles")
    print("\nType 'exit' to end the session.\n")

    agent = create_study_agent()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nStudyBot: Great session! Keep studying! 📖 Goodbye!")
            break

        print("\nStudyBot: ", end="", flush=True)
        agent.print_response(user_input, stream=True)
        print("\n")


if __name__ == "__main__":
    run_study_chat()
