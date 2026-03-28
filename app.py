"""
SmartStudy AI — Streamlit Web Application
Full-featured academic AI assistant with personalized study tools.
"""

import os
import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.calculator import Calculator
from phi.storage.agent.sqlite import SqlAgentStorage

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "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")
os.environ["PHI_API_KEY"] = os.getenv("PHIDATA_API_KEY", "phi-PUJOCOMOUtdDdsCGMoTr73s_HrlmfjHyeBf4pAsFbxg")

st.set_page_config(
    page_title="SmartStudy AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-banner {
        background: linear-gradient(135deg, #1a237e, #283593, #3949ab);
        padding: 2rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-banner h1 { margin: 0; font-size: 2rem; }
    .main-banner p  { margin: 0.4rem 0 0; opacity: 0.85; font-size: 1rem; }

    .agent-card {
        background: #f8f9ff;
        border: 1px solid #c5cae9;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
    }
    .agent-card h4 { margin: 0 0 4px; color: #1a237e; font-size: 0.95rem; }
    .agent-card p  { margin: 0; color: #555; font-size: 0.82rem; }

    .mode-active {
        background: #e8eaf6;
        border: 2px solid #3949ab !important;
    }

    .stButton > button {
        background: #3949ab;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #1a237e;
        transform: translateY(-1px);
    }

    div[data-testid="stChatMessage"] {
        border-radius: 10px;
        padding: 4px 8px;
    }

    .subject-pill {
        display: inline-block;
        background: #e8eaf6;
        color: #1a237e;
        border-radius: 20px;
        padding: 3px 10px;
        font-size: 0.78rem;
        margin: 2px;
    }
    .progress-section {
        background: #f3f4f9;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_mode" not in st.session_state:
    st.session_state.session_mode = "General Tutor"
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "topics_covered" not in st.session_state:
    st.session_state.topics_covered = []


@st.cache_resource
def get_agent(mode: str) -> Agent:
    """Return a mode-specific cached agent."""
    mode_configs = {
        "General Tutor": {
            "desc": "You are StudyBot, a versatile AI tutor helping with any subject.",
            "instructions": [
                "Explain concepts clearly with examples and analogies.",
                "Adapt to the student's level automatically.",
                "Use markdown for structure: headers, bullets, code blocks, tables.",
                "Encourage the student throughout the session.",
                "Always ask if clarification is needed.",
            ],
        },
        "Quiz Mode": {
            "desc": "You are QuizMaster, an expert at generating practice questions and flashcards.",
            "instructions": [
                "Generate multiple-choice, true/false, and short-answer questions.",
                "Always include answer explanations after the student responds.",
                "Vary difficulty: easy, medium, hard.",
                "Create Anki-style Q&A flashcards when asked.",
                "Keep score and give performance feedback.",
                "After every 5 questions, summarize strengths and weak areas.",
            ],
        },
        "Study Planner": {
            "desc": "You are PlanBot, an academic scheduler and productivity expert.",
            "instructions": [
                "Create realistic study schedules based on goals and deadlines.",
                "Apply Pomodoro, spaced repetition, and interleaving techniques.",
                "Break subjects into daily micro-tasks.",
                "Calculate exact hours needed per topic.",
                "Build weekly revision timetables.",
                "Recommend focus strategies and study environments.",
            ],
        },
        "Writing Coach": {
            "desc": "You are WriteBot, an academic writing expert and essay coach.",
            "instructions": [
                "Provide detailed essay feedback: structure, arguments, evidence, clarity.",
                "Help develop strong thesis statements.",
                "Improve academic vocabulary and sentence variety.",
                "Assist with APA, MLA, Chicago, Harvard citations.",
                "Generate essay outlines and brainstorm ideas.",
                "Review and improve grammar and coherence.",
            ],
        },
        "STEM Solver": {
            "desc": "You are MathBot, a mathematics and science problem-solving expert.",
            "instructions": [
                "Solve problems step-by-step showing all working.",
                "Use the calculator for precise numerical answers.",
                "Explain the 'why' behind every step.",
                "Generate similar practice problems after solving.",
                "Cover algebra, calculus, statistics, physics, chemistry, biology, CS.",
                "Use ASCII tables and formatted equations where helpful.",
            ],
        },
    }

    cfg = mode_configs.get(mode, mode_configs["General Tutor"])
    return Agent(
        name=f"SmartStudy-{mode.replace(' ', '')}",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[DuckDuckGo(), Calculator()],
        storage=SqlAgentStorage(
            table_name=f"study_{mode.replace(' ', '_').lower()}",
            db_file="smartstudy_web.db",
        ),
        description=cfg["desc"],
        instructions=cfg["instructions"],
        markdown=True,
        show_tool_calls=False,
        add_history_to_messages=True,
        num_history_responses=6,
    )


# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎓 Your Profile")
    student_name = st.text_input("Your name", placeholder="e.g. Alex")
    grade_level = st.selectbox("Grade / Level", [
        "Middle School", "High School", "Undergraduate",
        "Graduate", "Self-learner", "Professional"
    ])
    primary_subject = st.selectbox("Primary Subject", [
        "Mathematics", "Physics", "Chemistry", "Biology",
        "Computer Science", "History", "Literature", "Economics",
        "Psychology", "Philosophy", "Languages", "Other"
    ])
    learning_style = st.selectbox("Learning Style", [
        "Visual (diagrams & charts)", "Conceptual (big picture)",
        "Step-by-step (procedural)", "Example-driven", "Discussion-based"
    ])

    st.markdown("---")
    st.markdown("### 🤖 Study Mode")
    modes = {
        "📖 General Tutor": "General Tutor",
        "🧩 Quiz Mode": "Quiz Mode",
        "📅 Study Planner": "Study Planner",
        "✍️ Writing Coach": "Writing Coach",
        "🔢 STEM Solver": "STEM Solver",
    }
    for label, value in modes.items():
        active = st.session_state.session_mode == value
        if st.button(label, key=f"mode_{value}", use_container_width=True):
            if st.session_state.session_mode != value:
                st.session_state.session_mode = value
                st.session_state.messages = []
                st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    st.metric("Questions Asked", st.session_state.question_count)
    if st.session_state.topics_covered:
        st.markdown("**Topics covered:**")
        for t in st.session_state.topics_covered[-5:]:
            st.markdown(f"<span class='subject-pill'>{t}</span>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.question_count = 0
        st.rerun()


# ── Main UI ────────────────────────────────────────────────
st.markdown(f"""
<div class="main-banner">
    <h1>📚 SmartStudy AI</h1>
    <p>Autonomous Academic Intelligence — Powered by PhiData + Groq</p>
</div>
""", unsafe_allow_html=True)

# Mode info bar
mode_info = {
    "General Tutor":  ("📖", "Explain any concept, summarize notes, answer questions"),
    "Quiz Mode":      ("🧩", "Practice questions, flashcards & active recall"),
    "Study Planner":  ("📅", "Schedules, revision plans & Pomodoro strategies"),
    "Writing Coach":  ("✍️", "Essay feedback, outlines, citations & grammar"),
    "STEM Solver":    ("🔢", "Step-by-step math & science problem solving"),
}
icon, desc = mode_info[st.session_state.session_mode]
st.info(f"{icon} **{st.session_state.session_mode}** — {desc}")

# Quick Actions
st.markdown("**⚡ Quick Actions:**")
quick_cols = st.columns(5)
quick_prompts = {
    "General Tutor": [
        ("Explain a Concept", f"Explain {primary_subject} basics to me clearly"),
        ("Summarize Notes",   "Summarize my notes: [paste text here]"),
        ("Study Tips",        "Give me the best evidence-based study techniques"),
        ("Key Definitions",   f"List the most important terms in {primary_subject}"),
        ("Real World Link",   f"How is {primary_subject} used in the real world?"),
    ],
    "Quiz Mode": [
        ("5 MCQs",       f"Generate 5 multiple-choice questions on {primary_subject}"),
        ("Flashcards",   f"Create 10 flashcards for {primary_subject}"),
        ("True/False",   f"Give me 5 true/false questions on {primary_subject}"),
        ("Hard Quiz",    f"Give me 3 advanced questions on {primary_subject}"),
        ("Mixed Quiz",   f"Mixed difficulty quiz on {primary_subject} (10 questions)"),
    ],
    "Study Planner": [
        ("Week Plan",     "Create a 7-day study plan for my upcoming exams"),
        ("Pomodoro",      "Build a Pomodoro schedule for 3 hours of study today"),
        ("Exam Prep",     f"I have a {primary_subject} exam in 2 weeks. Build a revision plan"),
        ("Daily Routine", "Suggest an optimal daily study routine for a student"),
        ("Beat Burnout",  "How do I study consistently without burning out?"),
    ],
    "Writing Coach": [
        ("Essay Outline",  "Help me outline an essay on a topic in {primary_subject}"),
        ("Thesis Help",    "Help me write a strong thesis statement"),
        ("APA Citation",   "Explain how to cite sources in APA format"),
        ("Intro Hook",     "Write a compelling introduction hook for my essay"),
        ("Improve This",   "Review and improve this paragraph: [paste here]"),
    ],
    "STEM Solver": [
        ("Solve Problem", f"Solve a {primary_subject} problem step by step"),
        ("Explain Formula","Explain the most important formula in {primary_subject}"),
        ("Practice Set",   f"Give me 5 practice problems on {primary_subject}"),
        ("Derivation",     "Derive an important equation in Physics step by step"),
        ("Concept Check",  f"Quiz me on key formulas in {primary_subject}"),
    ],
}

actions = quick_prompts.get(st.session_state.session_mode, quick_prompts["General Tutor"])
for i, (label, prompt) in enumerate(actions):
    with quick_cols[i]:
        if st.button(label, key=f"qa_{i}", use_container_width=True):
            filled = prompt.replace("{primary_subject}", primary_subject)
            st.session_state.messages.append({"role": "user", "content": filled})
            st.session_state.pending = filled
            st.session_state.question_count += 1
            st.rerun()

st.markdown("---")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process pending quick action
if "pending" in st.session_state:
    prompt = st.session_state.pop("pending")
    with st.chat_message("assistant"):
        with st.spinner("StudyBot is thinking..."):
            agent = get_agent(st.session_state.session_mode)
            profile = (
                f"Student: {student_name or 'Student'}, Level: {grade_level}, "
                f"Subject focus: {primary_subject}, Learning style: {learning_style}."
            )
            full_prompt = f"{profile}\n\n{prompt}"
            response = agent.run(full_prompt)
            text = response.content if hasattr(response, "content") else str(response)
            st.markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})
            words = prompt.split()[:3]
            topic = " ".join(words)
            if topic not in st.session_state.topics_covered:
                st.session_state.topics_covered.append(topic)

# Chat input
if user_msg := st.chat_input(f"Ask StudyBot anything about {primary_subject}..."):
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.session_state.question_count += 1
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            agent = get_agent(st.session_state.session_mode)
            profile = (
                f"Student: {student_name or 'Student'}, Level: {grade_level}, "
                f"Subject: {primary_subject}, Learning style: {learning_style}."
            )
            full_prompt = f"{profile}\n\n{user_msg}"
            response = agent.run(full_prompt)
            text = response.content if hasattr(response, "content") else str(response)
            st.markdown(text)
            st.session_state.messages.append({"role": "assistant", "content": text})
            words = user_msg.split()[:3]
            topic = " ".join(words)
            if topic not in st.session_state.topics_covered:
                st.session_state.topics_covered.append(topic)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#888;font-size:0.8rem;'>"
    "SmartStudy AI • PhiData + Groq (LLaMA 3.3 70B) • "
    "Built for students, by AI — always verify critical academic information."
    "</p>",
    unsafe_allow_html=True,
)
