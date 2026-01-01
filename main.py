 from fastapi import FastAPI
  from pydantic import BaseModel, Field
  import logging
  from datetime import datetime

  # Configure logging to file
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s',
      handlers=[
          logging.FileHandler('/app/logs/salary_calculations.log'),
          logging.StreamHandler()
      ]
  )

  logger = logging.getLogger(__name__)

  app = FastAPI(title="Salary Calculator API")


  class SalaryRequest(BaseModel):
      gross_salary: float = Field(..., gt=0, description="Gross salary (must be positive)")


  class SalaryResponse(BaseModel):
      gross_salary: float
      net_salary: float
      tax_rate: float


  @app.get("/")
  async def root():
      return {"message": "Welcome to Salary Calculator API. Use POST /calculate-salary to calculate net 
  salary."}


  @app.post("/calculate-salary", response_model=SalaryResponse)
  async def calculate_salary(salary: SalaryRequest):
      """
      Calculate net salary from gross salary.
      Net salary = Gross salary * 0.6
      """
      tax_rate = 0.6
      net_salary = salary.gross_salary * tax_rate

      # Log the calculation
      logger.info(f"Calculation: Gross={salary.gross_salary}, Net={net_salary}, Time={datetime.now()}")

      return SalaryResponse(
          gross_salary=salary.gross_salary,
          net_salary=net_salary,
          tax_rate=tax_rate
      )