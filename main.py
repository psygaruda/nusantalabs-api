from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="NusantaLabs Public Data API",
    description="API for accessing standardized economic and environmental data for Indonesia.",
    version="1.0.0"
)

# --- Data Models ---
class Region(BaseModel):
    code: str
    name: str
    level: str

class Source(BaseModel):
    organization: str
    published_date: str
    validation_status: str

class MetricItem(BaseModel):
    indicator_id: str
    indicator_name: str
    value: float
    unit: str
    period: str
    region: Region
    source: Source

class Metadata(BaseModel):
    timestamp: datetime
    request_id: str

class FiscalResponse(BaseModel):
    meta: Metadata
    data: List[MetricItem]

# --- Mock Database ---
mock_db = [
    {
        "indicator_id": "IDN_DEBT_GDP_EST",
        "indicator_name": "Debt to GDP Ratio (Estimate)",
        "value": 40.51,
        "unit": "percent",
        "period": "2025-FY",
        "region": {"code": "ID", "name": "Indonesia", "level": "national"},
        "source": {"organization": "Ministry of Finance", "published_date": "2025-01-01", "validation_status": "estimate"}
    }
]

# --- Routes ---
@app.get("/", tags=["Health"])
async def root():
    return {"message": "NusantaLabs API is running", "status": "active"}

@app.get("/api/v1/economics/fiscal-metrics", response_model=FiscalResponse, tags=["Economics"])
async def get_fiscal_metrics(
    indicator_id: Optional[str] = Query(None, description="Filter by indicator ID"),
    year: Optional[int] = Query(None, description="Filter by fiscal year")
):
    results = mock_db
    if indicator_id:
        results = [item for item in results if item["indicator_id"] == indicator_id]
    
    if not results:
        raise HTTPException(status_code=404, detail="Data not found")

    return {
        "meta": {
            "timestamp": datetime.now(),
            "request_id": str(uuid.uuid4())
        },
        "data": results
    }
