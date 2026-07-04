# LeadSense — AI-Powered Lead Scoring for Smarter Customer Acquisition

**SBI Hackathon @ GFF 2026**

## Problem Statement
Bank websites and apps get thousands of visitors, but most are just browsing while a few are genuinely ready to open an account or apply for a loan. Right now, there's no way to tell them apart, so bank staff either follow up with everyone (wasting time) or miss the truly interested customers who quietly leave without applying.

## Our Solution
LeadSense tracks visitor behavior on the bank's website (pages visited, time spent, incomplete applications) and gives each visitor a real-time "lead score." High-scoring visitors are flagged as hot leads on a dashboard, so bank staff know exactly who to follow up with first — instead of guessing.

## Business Model / Commercial Potential
- **Internal use:** Boosts conversion from SBI's existing website/app traffic — no additional marketing spend required.
- **Long-term:** Can be packaged as a white-label SaaS product and licensed to other banks, NBFCs, and fintech platforms.

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript (React-ready)
- **Backend:** Python (Flask)
- **Database:** SQLite (swappable with Firebase/PostgreSQL)
- **Scoring Logic:** Rule-based weighted formula (upgradeable to ML model)
- **Hosting:** Deployable on Render/Vercel for demo; AWS/Azure for production

## Process Flow / Architecture
1. Visitor lands on the mock bank website (`frontend/`)
2. JS tracking script records page visits, time spent, and form completion
3. Events sent to backend API (`backend/app.py`)
4. Backend calculates a lead score using a weighted formula
5. Score + visitor data stored in database
6. Dashboard (`frontend/dashboard.html`) displays ranked leads (hot → cold)
7. Bank staff prioritize outreach based on the dashboard

## Project Structure
```
leadsense-sbi-hackathon/
├── README.md
├── backend/
│   ├── app.py              # Flask API — tracks events & computes scores
│   ├── scoring.py          # Scoring formula logic
│   └── requirements.txt
└── frontend/
    ├── index.html          # Mock bank website (demo)
    ├── dashboard.html       # Lead scoring dashboard
    ├── style.css
    └── script.js            # Tracking script
```

## How to Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on `http://localhost:5000`

### Frontend
Just open `frontend/index.html` and `frontend/dashboard.html` in your browser.

## Team
- [Your Name] — Role
- [Teammate Name] — Role

## Demo Video
[Add your demo video link here]
