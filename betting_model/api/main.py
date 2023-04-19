from datetime import date
import json
from fastapi import FastAPI, Query
from typing import Optional
import subprocess
import re
import time
import tensorflow
from moneyline import moneyline
from spread import spread

app = FastAPI()

@app.get("/")
async def my_endpoint(
    query_param: Optional[str] = Query(default=None),
    team1: Optional[str] = Query(default=None),
    team2: Optional[str] = Query(default=None),
    odds1: Optional[float] = Query(default=None),
    odds2: Optional[float] = Query(default=None),
    spread: Optional[float] = Query(default=None),
    ):
    if query_param == "moneyline":
        result = moneyline(team1, team2, odds1, odds2)
        result = f"It is more profitable to bet on {result}"
    elif query_param == "spread":
        result = spread(team1, team2, spread)
        result = f"It is more profitable to bet on {result}"
    else:
        result = {"error": "Invalid query parameter value."}
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)