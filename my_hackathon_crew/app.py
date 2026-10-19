import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables (fallback to Streamlit secrets if hosted)
load_dotenv()
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Page Configuration
st.set_page_config(
    page_title="AI Workforce Travel Planner",
    page_icon="🤖",
    layout="wide"
)

st.markdown("## 🤖 Autonomous AI Workforce: Tech Travel Planner")
st.markdown("A collaborative digital organization executing intelligent event logistics, transit planning, and budgeting.")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("🎛️ Workforce Parameters")
user_origin = st.sidebar.text_input("Origin City", "San Jose, CA")
target_event = st.sidebar.text_input("Target Event & City", "AWS Builder Loft in San Francisco, CA")
trip_duration = st.sidebar.selectbox("Trip Duration", ["1 day (Local)", "2 days", "3 days", "5 days"], index=1)
max_budget = st.sidebar.text_input("Maximum Budget", "$400")

# --- EXECUTION FUNCTION ---
def run_crew(origin, event, duration, budget, feedback=""):
    # Smart context check for local travel
    is_local = "1 day" in duration or "San Francisco" in event and "San Francisco" in origin or "San Jose" in origin and "San Francisco" in event # (simplified proximity check)
    
    accommodation_instruction = (
        f"Since the user is traveling locally or staying for a short trip, SKIP hotel/Airbnb recommendations and instead focus on daily parking, commuter rail/BART, or rideshare logistics for a {duration} stay."
        if "1 day" in duration else
        f"Find 3 lodging options (hotels or Airbnbs) near the event venue for a {duration} stay that fit within a total budget of {budget}."
    )

    # 1. Define Agents
    event_scout = Agent(
        role='Tech Event & Convention Specialist',
        goal='Identify event dates, venue locations, and key logistics for target tech conferences or hackathons.',
        backstory='An expert tech community manager who tracks major industry summits, hackathons, and hardware expos.',
        verbose=True
    )

    transit_planner = Agent(
        role='Transportation & Transit Coordinator',
        goal='Compare transit options (flights, driving, Amtrak, rideshare, public transit) from user origin to the event.',
        backstory='A logistics expert who calculates travel times, convenience, and cost-effectiveness for travelers.',
        verbose=True
    )

    accommodation_scout = Agent(
        role='Lodging & Neighborhood Scout',
        goal='Recommend lodging or daily commuter options near the event venue balancing proximity and budget.',
        backstory='A travel agent specializing in finding safe, well-located, and cost-efficient stays or daily transit routines.',
        verbose=True
    )

    budget_optimizer = Agent(
        role='Financial Budget Optimizer',
        goal='Aggregate all costs and build an optimized expense breakdown matching the target budget.',
        backstory='A meticulous financial planner who loves finding ways to trim unnecessary travel expenses.',
        verbose=True
    )

    itinerary_writer = Agent(
        role='Executive Itinerary & Action Planner',
        goal='Synthesize all data into a clean, beautifully formatted Markdown travel and conference schedule.',
        backstory='A master technical writer who turns complex logistics into crystal-clear step-by-step travel guides.',
        verbose=True
    )

    # 2. Define Tasks
    extra_context = f"\nUser Feedback / Revision Request to incorporate: {feedback}" if feedback else ""

    task1 = Task(
        description=f"Research the event '{event}'. Find its typical venue neighborhood in the host city and key dates for a {duration} stay.{extra_context}",
        expected_output="Summary of event location, dates, and venue context.",
        agent=event_scout
    )

    task2 = Task(
        description=f"Evaluate travel options from {origin} to the event location. Compare driving, train options, public transit vs. Uber/Lyft.{extra_context}",
        expected_output="A breakdown of transit options with estimated costs and pros/cons.",
        agent=transit_planner
    )

    task3 = Task(
        description=f"{accommodation_instruction}{extra_context}",
        expected_output="Curated lodging choices or daily commuting strategy.",
        agent=accommodation_scout
    )

    task4 = Task(
        description=f"Take transit estimates and lodging/commuting costs, calculate total expenses against budget of {budget}.{extra_context}",
        expected_output="Structured budget table and financial feasibility review.",
        agent=budget_optimizer
    )

    task5 = Task(
        description=f"Combine all findings into a final, comprehensive Markdown travel plan.{extra_context}",
        expected_output="Polished Markdown travel dossier.",
        agent=itinerary_writer
    )

    travel_crew = Crew(
        agents=[event_scout, transit_planner, accommodation_scout, budget_optimizer, itinerary_writer],
        tasks=[task1, task2, task3, task4, task5],
        process=Process.sequential,
        verbose=True
    )

    return travel_crew.kickoff(), task1, task2, task3, task4, task5

# --- MAIN APP LOGIC ---
if "dossier" not in st.session_state:
    st.session_state.dossier = None

if st.sidebar.button("🚀 Deploy AI Workforce", type="primary"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API Key not found!")
    else:
        with st.spinner("🤖 AI Workforce active: Agents collaborating on research, transit, and budgeting..."):
            result, t1, t2, t3, t4, t5 = run_crew(user_origin, target_event, trip_duration, max_budget)
            st.session_state.dossier = str(result)
            st.session_state.tasks = (t1, t2, t3, t4, t5)
            st.success("🎉 Mission Complete!")

# Display Results if available
if st.session_state.dossier:
    tab_final, tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Executive Travel Dossier", 
        "🗺️ Event Scout", 
        "🚆 Transit Planner", 
        "🏨 Accommodation Scout", 
        "💰 Budget Optimizer",
        "✍️ Itinerary Writer"
    ])

    with tab_final:
        st.markdown(st.session_state.dossier)
        st.download_button("📥 Download Dossier (Markdown)", data=st.session_state.dossier, file_name="travel_plan.md", mime="text/markdown")

        # --- FOLLOW-UP PROMPT / FEEDBACK BOX ---
        st.markdown("---")
        st.subheader("💬 Refine with Workforce Feedback")
        user_feedback = st.text_input("Ask the workforce to adjust the plan (e.g., 'Make it cheaper', 'Focus on public transit only', 'Add coffee shops near the venue'):")
        if st.button("🔄 Update Plan with Feedback"):
            if user_feedback:
                with st.spinner("🤖 Workforce revising plan based on your feedback..."):
                    new_result, t1, t2, t3, t4, t5 = run_crew(user_origin, target_event, trip_duration, max_budget, feedback=user_feedback)
                    st.session_state.dossier = str(new_result)
                    st.session_state.tasks = (t1, t2, t3, t4, t5)
                    st.rerun()

    # Task output tabs
    t1, t2, t3, t4, t5 = st.session_state.tasks
    with tab1:
        st.markdown(t1.output.raw if hasattr(t1, 'output') and t1.output else "Generated.")
    with tab2:
        st.markdown(t2.output.raw if hasattr(t2, 'output') and t2.output else "Generated.")
    with tab3:
        st.markdown(t3.output.raw if hasattr(t3, 'output') and t3.output else "Generated.")
    with tab4:
        st.markdown(t4.output.raw if hasattr(t4, 'output') and t4.output else "Generated.")
    with tab5:
        st.markdown(t5.output.raw if hasattr(t5, 'output') and t5.output else "Generated.")
else:
    st.info("👈 Fill in your trip parameters in the sidebar and click **'Deploy AI Workforce'** to begin.")