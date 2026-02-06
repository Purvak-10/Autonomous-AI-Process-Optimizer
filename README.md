# Autonomous AI Process Optimizer

An explainable AI system that **understands how tickets move inside a company**, finds **where work gets stuck**, tests **what would happen if we change the process**, and finally **recommends the best solution in simple language**.

This project is built to answer one core question:

> “Our tickets are slow — but **why**, **where**, and **what should we do about it**?”

---

## 🧩 The Real-World Problem

In most companies, work happens through **tickets**:
- IT support tickets
- Approval requests
- Service requests
- Internal process tasks

A ticket usually goes through steps like:

Created → Assigned → In Progress → Approved → Closed


### The problem is:
- Managers only see **final delay**
- They don’t know **which step caused it**
- They don’t know **if changing a rule will actually help**
- Changes are made blindly and often fail

This system solves that problem **before real changes are made**.

---

## 🧠 What This Project Demonstrates

This project is designed as a portfolio-level system, not a toy script.
It demonstrates my ability to:
- Design end-to-end AI systems
- Apply process mining concepts
- Use local LLMs responsibly
- Build explainable AI, not black boxes
- Simulate decisions before applying them
- Communicate results clearly to non-technical users

---

## 🧠 What This System Actually Does 

### Step 1: Understand the Process (Process Intelligence)
The system reads ticket event logs and reconstructs:
- Who worked on the ticket
- Which steps it passed through
- How long each step took
- How much it cost

So instead of raw data, it understands the **full journey of every ticket**.

---

### Step 2: Find Where Work Gets Stuck
The system automatically calculates:
- Average time per step
- Slowest steps (bottlenecks)
- SLA violations
- Cost impact

Example insight:
> “The `Approved` step takes 10× longer than any other step.”

---

### Step 3: Ask AI *Why* This Is Happening
A local AI model (LLM) is given:
- Process metrics
- Bottleneck data
- Workflow structure

The AI explains **in simple language**:
- What the main problem is
- Why it is happening
- Whether it’s caused by humans, policy, or system design

Example:
> “The delay is caused by manual approvals and lack of automation.”

---

### Step 4: Generate Possible Improvements
The AI then proposes **realistic process changes**, such as:
- Auto-approval for low-risk tickets
- Faster routing
- Escalation limits

Each proposal is:
- Rule-based
- Practical
- Safe (checked against constraints)

---

### Step 5: Simulate the Changes (Digital Twin)
This is the **most important part**.

Instead of guessing, the system:
- Creates a **digital twin** of the company process
- Replays the same tickets
- Applies each proposed change
- Measures what would happen

This shows:
- Time saved
- Cost saved
- SLA improvement

All without touching real systems.

---

### Step 6: Choose the Best Decision
The system compares:
- Before AI vs After AI
- Multiple possible solutions

It then selects the **best policy** based on:
- Maximum time reduction
- Lower cost
- Fewer SLA violations

---

### Step 7: Explain the Final Decision
The system produces:
- A clear executive summary
- Evidence for the decision
- A full decision trace

Example:
> “Auto-approval reduces ticket cycle time by 55%, cost by 60%, and SLA violations by 27%.”

---

## 📊 What the Dashboard Shows

The dashboard is designed so **even a non-technical person can understand it**.

It shows:
- Current process health
- Where delays occur
- Before vs After AI comparison
- AI’s final recommendation (highlighted clearly)
- Explanation of *why* that decision was chosen

This is not just analytics — it is **decision guidance**.

---

## 🧪 What Data Is Used

- Fully **synthetic ticket data**
- No real company or customer data
- Designed to mimic real enterprise workflows
- Safe to share publicly

---

## 🏗️ Project Structure (High Level)

```bash
autonomous-ai-process-optimizer/
├── config/ # Process rules, SLAs, scenarios (no secrets)
├── data/ # Synthetic event logs (generated)
├── src/
│ ├── generator/ # Synthetic ticket generation
│ ├── storage/ # Trace building and DB handling
│ ├── mining/ # Process mining and bottleneck detection
│ ├── llm_engine/ # AI reasoning (root cause analysis)
│ ├── hypothesis/ # AI-generated improvement ideas
│ ├── simulation/ # Digital twin simulation
│ ├── optimizer/ # Policy scoring and RL
│ ├── explainability/ # Business-level explanations
│ └── dashboard/ # Streamlit UI
└── README.md
```

---

## ⚙️ How to Run

```bash
git clone https://github.com/Purvak-10/Autonomous-AI-Process-Optimizer.git
```

```bash
cd autonomous-ai-process-optimizer
```
```bash
python3 -m venv venv
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
```bash
python3 -m streamlit run src/dashboard/app.py
```

Open:
```bash
http://localhost:8501
```
--- 

## 🤖 AI Model

- Runs locally using Ollama
- Example model: llama3.1:8b
- No internet required once model is installed

---

## 🚀 Why This Project Is Valuable

This project demonstrates:
- End-to-end AI system design
- Process intelligence + Generative AI
- Simulation-based decision making
- Explainable AI for business users
- Production-ready architecture

It goes beyond prediction and answers:
> “What should we do — and why?”

--- 

## 🔮 Future Work

- **Ticket Request Understanding**  
  Extend the system to analyze ticket descriptions using NLP so decisions are based on *what* the request is, not only *how* it moves through the process.

- **Real-Time Processing**  
  Enable live ticket ingestion and real-time AI analysis instead of batch-based evaluation.

- **Human-in-the-Loop Decisions**  
  Allow managers to review, approve, or override AI recommendations to improve trust and safety.

- **Learning From Past Outcomes**  
  Store past decisions and results so the system can continuously improve its recommendations over time.

- **Enterprise Readiness**  
  Add authentication, role-based access, and scalability features for real-world deployment.
