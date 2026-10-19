# 🤖 Autonomous AI Workforce: Tech Convention & Travel Planner

> **Universal Hackathon: Create Your Own AI Workforce**  
> Built for the AWS Builder Loft, San Francisco.

---

## 🚀 Overview
The **Tech Convention & Travel Planner** is an autonomous multi-agent AI system designed to solve complex corporate and hackathon travel logistics. Instead of a single monolithic prompt, this project deploys a **5-agent specialized digital workforce** that collaborates sequentially to research venues, map transit, secure lodging, optimize budgets, and generate an executive travel dossier.

---

## 👥 The 5-Agent AI Workforce

1. **🗺️ Event Scout (Tech Event Specialist):** Researches conference dates, keynotes, and venue neighborhoods.
2. **🚆 Transit Planner (Transportation Coordinator):** Evaluates flights, trains, driving, and local transit.
3. **🏨 Accommodation Scout (Lodging Specialist):** Curates hotels/Airbnbs balancing proximity and nightly rates.
4. **💰 Budget Optimizer (Financial Auditor):** Aggregates expenses and checks feasibility against user budgets.
5. **📋 Itinerary Writer (Executive Synthesizer):** Formulates the final polished Markdown travel schedule.

---

## 🛠️ Tech Stack
- **Orchestration:** CrewAI (Sequential Process)
- **AI Model:** OpenAI GPT-4o / GPT-4o-mini
- **Frontend UI:** Streamlit Dashboard with Agent Inspection Tabs
- **Environment & Dependency Management:** Python 3.12 & `uv`

---

## ⚙️ Quickstart Installation

1. **Clone the repository & navigate to project folder:**
   ```bash
   cd my_hackathon_crew
