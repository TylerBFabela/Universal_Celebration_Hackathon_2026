import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables
load_dotenv()

def run_travel_crew(origin="Los Angeles, CA", event="AI Infra Summit in San Francisco, CA", duration="3 days", budget="$700"):
    print(f"\n🚀 Initializing AI Travel Workforce for: {event} (Origin: {origin})...\n")

    # 1. Define Specialized Agents
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
        goal='Recommend hotels or Airbnb options near the event venue that balance proximity and budget.',
        backstory='A travel agent specializing in finding safe, well-located, and cost-efficient stays for attendees.',
        verbose=True
    )

    budget_optimizer = Agent(
        role='Financial Budget Optimizer',
        goal='Aggregate all costs (transit + lodging + event pass) and build an optimized expense breakdown matching the target budget.',
        backstory='A meticulous financial planner who loves finding ways to trim unnecessary travel expenses.',
        verbose=True
    )

    itinerary_writer = Agent(
        role='Executive Itinerary & Action Planner',
        goal='Synthesize all data into a clean, beautifully formatted Markdown travel and conference schedule.',
        backstory='A master technical writer who turns complex logistics into crystal-clear step-by-step travel guides.',
        verbose=True
    )

    # 2. Define Sequential Tasks
    task1 = Task(
        description=f"Research the event '{event}'. Find its typical venue neighborhood in the host city and key dates for a {duration} stay.",
        expected_output="Summary of the event location, dates, and venue context.",
        agent=event_scout
    )

    task2 = Task(
        description=f"Evaluate travel options from {origin} to the event location. Compare flying, driving, or train options, plus local public transit vs. Uber/Lyft.",
        expected_output="A breakdown of transit options with estimated costs and pros/cons.",
        agent=transit_planner
    )

    task3 = Task(
        description=f"Find 3 lodging options (hotels or Airbnbs) near the event venue for a {duration} stay that fit within a total budget of {budget}.",
        expected_output="A curated list of 3 lodging choices with estimated nightly rates and proximity scores.",
        agent=accommodation_scout
    )

    task4 = Task(
        description=f"Take transit estimates and lodging costs, calculate total trip expenses against the strict max budget of {budget}, and suggest cost-saving trade-offs if needed.",
        expected_output="A structured budget table and financial feasibility review.",
        agent=budget_optimizer
    )

    task5 = Task(
        description="Combine all findings from the scout, transit planner, accommodation scout, and budget optimizer into a final, comprehensive Markdown travel plan.",
        expected_output="A polished, ready-to-read Markdown travel dossier for the user.",
        agent=itinerary_writer
    )

    # 3. Assemble Crew
    travel_crew = Crew(
        agents=[event_scout, transit_planner, accommodation_scout, budget_optimizer, itinerary_writer],
        tasks=[task1, task2, task3, task4, task5],
        process=Process.sequential,
        verbose=True
    )

    result = travel_crew.kickoff()
    
    # Save output
    filename = "travel_plan.md"
    with open(filename, "w") as f:
        f.write(str(result))
        
    print(f"\n✅ Success! Travel Dossier saved to {filename}")
    return result

if __name__ == "__main__":
    run_travel_crew()
