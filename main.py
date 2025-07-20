from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import re

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load your sales data once at startup
df = pd.read_json("data/data.json")

# Pre‑compiled regex patterns for each question type
_patterns = {
    "total_sales": re.compile(
        r"^What is the total sales of (?P<product>\w+) in (?P<city>[\w\s]+)\?$",
        re.IGNORECASE
    ),
    "count_reps": re.compile(
        r"^How many sales reps are there in (?P<region>[\w\s]+)\?$",
        re.IGNORECASE
    ),
    "avg_sales": re.compile(
        r"^What is the average sales for (?P<product>\w+) in (?P<region>[\w\s]+)\?$",
        re.IGNORECASE
    ),
    "highest_date": re.compile(
        r"^On what date did (?P<rep>[\w\.\s']+) make the highest sale in (?P<city>[\w\s]+)\?$",
        re.IGNORECASE
    ),
}

@app.get("/query")
def query(q: str = Query(..., description="Natural‑language question")):
    # Try matching each pattern
    for kind, pat in _patterns.items():
        m = pat.match(q.strip())
        if not m:
            continue

        # 1) Total sales of PRODUCT in CITY?
        if kind == "total_sale_
