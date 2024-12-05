from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_excel(io.BytesIO(content)) if file.filename.endswith('.xlsx') \
        else pd.read_csv(io.BytesIO(content))
    
    # Basic financial metrics calculation
    metrics = {
        "total_revenue": float(df["revenue"].sum()),
        "growth_rate": float(((df["revenue"].iloc[-1] / df["revenue"].iloc[0]) - 1) * 100),
        "avg_margin": float((df["revenue"].sum() - df["costs"].sum()) / df["revenue"].sum() * 100)
    }
    
    return {"metrics": metrics}