from fastapi import FastAPI, HTTPException, Body
from typing import List
from services.candidate_scraper import scrape_linkedin_profile
from services.company_scraper import scrape_linkedin_company

app = FastAPI()

@app.post("/profile-data")
async def profile_data(linkedin_ids: List[str] = Body(...)):
    try:
        profile_infos = scrape_linkedin_profile(linkedin_ids)
        return profile_infos
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching profile details")

@app.post("/company-data")
async def company_data(linkedin_ids: List[str] = Body(...)):
    try:
        company_infos = scrape_linkedin_company(linkedin_ids)
        return company_infos
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching company details")