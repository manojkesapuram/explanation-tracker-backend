from fastapi import FastAPI
from models import Session, Record
from email_reader import fetch_emails
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi.responses import FileResponse

app = FastAPI()   # 👈 THIS LINE IS REQUIRED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def categorize(text):
    text = text.lower()
    if "delay" in text:
        return "Delay"
    elif "quality" in text:
        return "Quality"
    return "Other"

@app.get("/")
def home():
    return {"message": "API running"}

@app.get("/fetch")
def fetch():
    session = Session()
    emails = fetch_emails()

    for e in emails:
        rec = Record(
            name=e["name"],
            email=e["email"],  # ✅ ADD THIS
            explanation=e["explanation"],
            date=datetime.now(),
            category=categorize(e["explanation"])
        )
        session.add(rec)

    session.commit()
    return {"status": "saved"}

from fastapi import Query

@app.get("/data")
def get_data(name: str = Query(None)):
    session = Session()
    query = session.query(Record)

    if name:
        query = query.filter(Record.name == name)

    records = query.all()

    return [
        {
            "name": r.name,
            "email": r.email,
            "date": r.date,
            "category": r.category,
            "explanation": r.explanation

        } for r in records
    ]

@app.get("/export")
def export():
    session = Session()
    records = session.query(Record).all()

    data = [{
        "Name": r.name,
        "email": r.email,
        "Date": r.date,
        "Category": r.category,
        "Explanation": r.explanation
    } for r in records]

    df = pd.DataFrame(data)
    file = "report.xlsx"
    df.to_excel(file, index=False)

    return FileResponse(file, filename="report.xlsx")

@app.get("/insights")
def insights():
    session = Session()
    records = session.query(Record).all()

    from collections import Counter

    categories = [r.category for r in records]
    names = [r.name for r in records]

    return {
        "top_mistake": Counter(categories).most_common(1),
        "top_employee": Counter(names).most_common(1)
    }