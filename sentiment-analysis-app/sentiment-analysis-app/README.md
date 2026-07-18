# 💬 Feedback Sentiment Analyzer

A web app that reads customer feedback and instantly tells you whether it's
**Positive, Negative, or Neutral** — built for the Pinnacle Labs Internship
Program (2026).

## Why this matters
Businesses collect thousands of reviews, survey responses, and support
tickets but rarely have time to read them all. This tool turns raw text
feedback into instant, visual insight — one message at a time, or in bulk
via CSV upload.

## Features
| Feature | Description |
|---|---|
| 🔍 Single-text analysis | Paste any sentence, get an instant sentiment + confidence score |
| 📂 Batch CSV analysis | Upload a file of reviews and analyze them all at once |
| 📊 Distribution chart | Visual breakdown of Positive / Negative / Neutral split |
| ☁️ Word cloud | See the most common words in positive vs. negative feedback |
| ⬇️ CSV export | Download the analyzed results for reporting |

## Tech Stack
- **Python 3**
- **NLTK (VADER)** — rule-based sentiment scoring engine
- **Streamlit** — web interface
- **Pandas** — data handling
- **Plotly** & **WordCloud/Matplotlib** — visualizations

## How It Works
This project uses **VADER** (Valence Aware Dictionary and sEntiment
Reasoner), a sentiment model that:
1. Scores each word's emotional weight using a pre-built lexicon
2. Adjusts for negation (*"not good"*) and intensity (*"VERY good!!"*)
3. Combines everything into one **compound score** from **-1** (very
   negative) to **+1** (very positive)

No machine learning training step is required — it works instantly out of
the box, which makes it easy to explain and easy to trust.

## Project Structure
```
sentiment-analysis-app/
├── .streamlit/
│   └── config.toml        # Custom app theme
├── analyze.py              # Core sentiment logic (testable on its own)
├── app.py                   # Streamlit UI
├── requirements.txt
└── sample_feedback.csv      # Ready-to-use demo data
```

## Setup & Run
```bash
# 1. Clone or download this folder, then enter it
cd sentiment-analysis-app

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```
The app opens automatically at `http://localhost:8501`.

## Try It Instantly
Upload the included `sample_feedback.csv` in the Batch Analysis section to
see every feature in action with zero setup.

## Testing the Core Logic Alone
```bash
python analyze.py
```
Runs a few built-in example sentences and prints their sentiment — useful
for confirming the engine works before touching the UI.

---
*Built by Shivam · Pinnacle Labs Internship Program 2026*
