from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re
import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title='MindMitra API', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
DATA = Path(__file__).parent / 'checkins.json'

class CheckIn(BaseModel):
    journal: str = Field(min_length=1, max_length=3000)
    mood: int = Field(ge=1, le=5)
    sleep_hours: float | None = Field(default=None, ge=0, le=24)
    energy: int | None = Field(default=None, ge=1, le=5)

NEGATIVE = {'sad','stressed','anxious','lonely','overwhelmed','tired','worried','upset','burnout','hopeless'}
POSITIVE = {'happy','calm','grateful','excited','relaxed','good','hopeful','peaceful'}

def load():
    if not DATA.exists(): return []
    try: return json.loads(DATA.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError): return []

def analyze(journal, mood):
    words = set(re.findall(r"[a-z']+", journal.lower()))
    neg, pos = len(words & NEGATIVE), len(words & POSITIVE)
    if mood <= 2 or neg > pos:
        return {'label':'Difficult day','suggestion':'Consider a short break, a grounding exercise, or talking with someone you trust.'}
    if mood >= 4 and pos >= neg:
        return {'label':'Positive day','suggestion':'Notice what helped today and consider doing it again.'}
    return {'label':'Mixed or neutral day','suggestion':'A short walk, some water, or a few minutes of rest might help.'}

@app.get('/health')
def health(): return {'status':'ok'}

@app.post('/checkins')
def create_checkin(entry: CheckIn):
    records = load()
    record = {'id':len(records)+1, 'created_at':datetime.now(timezone.utc).isoformat(), **entry.model_dump(), **analyze(entry.journal, entry.mood)}
    records.append(record)
    DATA.write_text(json.dumps(records, indent=2), encoding='utf-8')
    return record

@app.get('/checkins')
def list_checkins(): return load()

@app.get('/trends')
def trends():
    records = load()
    values = [r['mood'] for r in records]
    return {'count':len(values),'average_mood':round(sum(values)/len(values),2) if values else None,'recent':records[-7:]}

@app.get('/resources')
def resources(city: str):
    # Integration point only: no simulated TinyFish results.
    # Never transmit journals or voice notes to external services.
    if not city.strip(): raise HTTPException(status_code=400, detail='City is required')
    return {'city':city, 'status':'not_configured', 'message':'TinyFish live resource lookup is not yet connected. Do not label results verified until source checks are implemented.', 'resources':[]}
