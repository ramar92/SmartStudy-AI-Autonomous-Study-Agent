"""
SmartStudy AI — Multi-Agent Team
Specialized study agents collaborating for comprehensive academic support.
"""

import os
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.calculator import Calculator
from phi.team import Team

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "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")
os.environ["PHI_API_KEY"] = os.getenv("PHIDATA_API_KEY", "phi-PUJOCOMOUtdDdsCGMoTr73s_HrlmfjHyeBf4pAsFbxg")

GROQ_MODEL = Groq(id="llama-3.3-70b-versatile")


def get_tutor_agent() -> Agent:
    """Agent specialized in concept explanation and teaching."""
    return Agent(
        name="ConceptTutor",
        role="Expert subject tutor and concept explainer",
        model=GROQ_MODEL,
        tools=[DuckDuckGo()],
        instructions=[
            "Break down complex concepts into simple, digestible explanations.",
            "Use real-world analogies, examples, and visual descriptions.",
            "Adapt explanation depth: ELI5, intermediate, or advanced based on context.",
            "Cover all major subjects: Math, Science, History, Literature, CS, Economics, etc.",
            "Explain step-by-step for procedural topics (math, coding, chemistry).",
            "Cross-reference with related concepts to build knowledge networks.",
            "Search for latest definitions, discoveries, or updated information.",
        ],
        markdown=True,
    )


def get_quiz_agent() -> Agent:
    """Agent specialized in generating quizzes and flashcards."""
    return Agent(
        name="QuizMaster",
        role="Quiz generator and active recall specialist",
        model=GROQ_MODEL,
        tools=[Calculator()],
        instructions=[
            "Generate high-quality multiple-choice, true/false, and short-answer questions.",
            "Create Anki-style flashcard sets in clear Q&A format.",
            "Design quizzes at varying difficulty levels: easy, medium, hard.",
            "Include answer explanations for every question.",
            "Build topic-specific question banks.",
            "Create fill-in-the-blank and matching exercises.",
            "Generate spaced-repetition review schedules for flashcard sets.",
            "Track which topics need more practice based on quiz performance.",
        ],
        markdown=True,
    )


def get_planner_agent() -> Agent:
    """Agent specialized in study planning and scheduling."""
    return Agent(
        name="StudyPlanner",
        role="Academic scheduler and productivity coach",
        model=GROQ_MODEL,
        tools=[Calculator()],
        instructions=[
            "Create detailed, realistic study schedules based on deadlines and goals.",
            "Apply proven techniques: Pomodoro, spaced repetition, interleaving.",
            "Break large subjects or projects into manageable daily tasks.",
            "Calculate hours needed per topic based on complexity and exam dates.",
            "Suggest optimal study times based on cognitive science research.",
            "Build revision calendars with buffer time for weak areas.",
            "Recommend study environment and focus strategies.",
            "Balance multiple subjects across a week to avoid burnout.",
        ],
        markdown=True,
    )


def get_writing_agent() -> Agent:
    """Agent specialized in essay writing and feedback."""
    return Agent(
        name="WritingCoach",
        role="Academic writing expert and essay coach",
        model=GROQ_MODEL,
        tools=[DuckDuckGo()],
        instructions=[
            "Provide detailed feedback on essays: structure, arguments, evidence, clarity.",
            "Help with thesis statement development and argument construction.",
            "Improve academic vocabulary and sentence variety.",
            "Check for logical flow, cohesion, and coherence.",
            "Assist with citation formats: APA, MLA, Chicago, Harvard.",
            "Generate essay outlines and brainstorm ideas.",
            "Paraphrase and summarize source material effectively.",
            "Help with research reports, lab reports, and case studies.",
        ],
        markdown=True,
    )


def get_math_science_agent() -> Agent:
    """Agent specialized in STEM problem solving."""
    return Agent(
        name="STEMSolver",
        role="Mathematics and science problem-solving expert",
        model=GROQ_MODEL,
        tools=[Calculator(), DuckDuckGo()],
        instructions=[
            "Solve math problems step-by-step: algebra, calculus, statistics, geometry.",
            "Explain physics, chemistry, and biology problems with working.",
            "Show all steps clearly with formulas and substitutions.",
            "Verify answers using the calculator tool.",
            "Explain the 'why' behind each step, not just the 'how'.",
            "Generate similar practice problems after solving.",
            "Visualize solutions with ASCII diagrams or tables where helpful.",
            "Cover CS topics: algorithms, data structures, complexity analysis.",
        ],
        markdown=True,
    )


def create_study_team() -> Team:
    """Create the full SmartStudy multi-agent team."""
    return Team(
        name="SmartStudyTeam",
        mode="coordinate",
        model=GROQ_MODEL,
        members=[
            get_tutor_agent(),
            get_quiz_agent(),
            get_planner_agent(),
            get_writing_agent(),
            get_math_science_agent(),
        ],
        instructions=[
            "Coordinate specialized study agents to deliver comprehensive academic help.",
            "Route concept/explanation questions to ConceptTutor.",
            "Route quiz, flashcard, and practice question requests to QuizMaster.",
            "Route study schedule and planning requests to StudyPlanner.",
            "Route essay writing, feedback, and citation help to WritingCoach.",
            "Route math, science, and coding problems to STEMSolver.",
            "Combine multiple agents for complex requests spanning several domains.",
            "Synthesize all agent outputs into a single coherent, well-structured response.",
            "Always be encouraging, patient, and academically rigorous.",
        ],
        markdown=True,
        show_tool_calls=True,
        description="A team of specialized AI tutors for every academic need.",
    )


def run_team_session():
    """Run an interactive SmartStudy multi-agent session."""
    print("\n" + "="*62)
    print("  🎓 SmartStudy Team — Multi-Agent Academic AI")
    print("  Powered by PhiData + Groq (LLaMA 3.3 70B)")
    print("="*62)
    print("\nSpecialists available:")
    print("  📖  ConceptTutor  — Explain any subject clearly")
    print("  🧩  QuizMaster    — Quizzes, flashcards & practice")
    print("  📅  StudyPlanner  — Schedules & study strategies")
    print("  ✍️   WritingCoach  — Essays, feedback & citations")
    print("  🔢  STEMSolver    — Math & science problem solving")
    print("\nType 'exit' to quit.\n")

    team = create_study_team()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("\nSmartStudy: Keep learning! Goodbye! 🎓")
            break

        print("\nSmartStudy Team: ", end="", flush=True)
        team.print_response(user_input, stream=True)
        print("\n")


if __name__ == "__main__":
    run_team_session()
