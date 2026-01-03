from fastapi import FastAPI
from pydantic import BaseModel, Field
import logging
import os
from datetime import datetime
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

# Configure logging to file
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/salary_calculations.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
app = FastAPI(title="Salary Calculator API")

# API Key security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    # Try to read from Docker secret file first, fallback to env var
    api_key_file = os.getenv("API_KEY_FILE")

    if api_key_file and os.path.exists(api_key_file):
        with open(api_key_file, "r") as f:
            correct_api_key = f.read().strip()
    else:
        correct_api_key = os.getenv("API_KEY", "default-key")

    if api_key == correct_api_key:
        return api_key

    raise HTTPException(
        status_code=403,
        detail="Invalid API Key",
    )


class SalaryRequest(BaseModel):
    gross_salary: float = Field(..., gt=0, description="Gross salary (must be positive)")


class SalaryResponse(BaseModel):
    gross_salary: float
    net_salary: float
    tax_rate: float


@app.get("/")
async def root():
    return {"message": "Welcome to Salary Calculator API. Use POST /calculate-salary to calculate net salary."}


@app.post("/calculate-salary", response_model=SalaryResponse)
async def calculate_salary(salary: SalaryRequest, api_key: str = Security(get_api_key)):
    """
    Calculate net salary from gross salary. test brahim
    Net salary = Gross salary * 0.6
    """
    tax_rate = float(os.getenv('TAX_RATE', '0.6'))
    net_salary = salary.gross_salary * tax_rate

    # Log the calculation
    logger.info(f"Calculation: Gross={salary.gross_salary}, Net={net_salary}, Time={datetime.now()}")

    return SalaryResponse(
        gross_salary=salary.gross_salary,
        net_salary=net_salary,
        tax_rate=tax_rate
    )